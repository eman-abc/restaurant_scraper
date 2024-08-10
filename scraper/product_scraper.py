from common.webdriver_manager import WebDriverManager
from common.config_manager import ConfigManager
from .product_extractor import ProductExtractor
from selenium.common.exceptions import TimeoutException
import csv
import time
import random
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ProductScraper:
    def __init__(self, driver_path, base_url, output_csv, db_manager):
        self.config = ConfigManager(driver_path)
        self.driver_manager = WebDriverManager(self.config)
        self.product_extractor = ProductExtractor(self.driver_manager.driver)
        self.output_csv = output_csv
        self.base_url = base_url
        self.all_products = []  # List to store all product data
        self.db_manager = db_manager

    def run(self):
        try:
            self.scrape_products()
        finally:
            self.driver_manager.close_driver()

    def wait_for_images_to_load(self):
        try:
            images = self.driver_manager.driver.find_elements(By.TAG_NAME, "img")
            WebDriverWait(self.driver_manager.driver, 20).until(
                lambda driver: all(
                    img.get_attribute("complete") == "true" for img in driver.find_elements(By.TAG_NAME, "img")
                )
            )
        except TimeoutException:
            print("Timeout while waiting for images to load.")

    def scrape_products(self):
        try:
            self.driver_manager.load_page(self.base_url)
            last_height = self.driver_manager.driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll to the bottom of the page
                self.driver_manager.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait for new content to load
                time.sleep(random.uniform(3, 6))

                # Wait for all images to load
                self.wait_for_images_to_load()

                # Extract products after scrolling
                products = self.product_extractor.extract_products()

                # If new products were found, process them
                if products:
                    self.all_products.extend(products)
                    write_header = (len(self.all_products) == len(products))  # Write header only for the first set of products
                    self.write_products_to_csv(products, write_header)
                    # self.db_manager.insert_product_data(products)

                # Calculate new scroll height and compare with last height
                new_height = self.driver_manager.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break  # No more new content loaded
                last_height = new_height

        except TimeoutException:
            print("Timeout while loading the page.")
        except Exception as e:
            print(f"Error during scraping: {e}")

    def write_products_to_csv(self, products, write_header):
        # Assuming the correct fieldnames based on the product data
        fieldnames = ['name', 'price', 'description', 'image_url']
        mode = 'a'  # Append mode
        try:
            with open(self.output_csv, mode, newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if write_header:
                    writer.writeheader()
                for product in products:
                    # Map the product data to the correct field names
                    product_data = {
                        'name': product.get('name', ''),
                        'price': product.get('price', ''),
                        'description': product.get('description', ''),
                        'image_url': product.get('image_url', '')  # Ensure this matches the actual key
                    }
                    writer.writerow(product_data)
            print(f"Products saved to {self.output_csv}")
        except IOError as e:
            print(f"Error saving to CSV file: {e}")
