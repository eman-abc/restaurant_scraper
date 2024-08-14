from common_trendyol.webdriver_manager import WebDriverManager
from common_trendyol.config_manager import ConfigManager
from .product_extractor import ProductExtractor
from selenium.common.exceptions import TimeoutException
import csv
import time
import random
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

class ProductScraper:
    def __init__(self, driver_path, base_url, output_csv, num_pages, db_manager):
        self.config = ConfigManager(driver_path)
        self.driver_manager = WebDriverManager(self.config)
        self.product_extractor = ProductExtractor(self.driver_manager.driver)
        self.output_csv = output_csv
        self.base_url = base_url
        self.num_pages = num_pages
        self.all_products = []  # List to store all product data
        self.product_urls=[]
        self.db_manager=db_manager
        self.categories={}

    def run(self):
        try:
            self.get_categories()
            for category in self.categories:
                self.scrape_products(category, self.categories[category])
        finally:
            self.driver_manager.close_driver()
            
    def scroll_to_bottom(self):
        self.driver_manager.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.randint(3, 6))  # Adjust based on the website's loading time
            
    def get_categories(self):
        url = self.base_url
        self.driver_manager.load_page(url)
        html_content = self.driver_manager.driver.find_element(By.CSS_SELECTOR, '[class="fltrs"]')
        inner_html = html_content.get_attribute('innerHTML')
        soup = BeautifulSoup(inner_html, 'html.parser')

        # Initialize an empty dictionary
        self.categories = {}

        # Find all the category links
        category_links = soup.find_all('a', class_='fltr-item-wrppr')

        # Iterate through each link and extract the category name and href value
        for link in category_links:
            category_name = link.find('div', class_='fltr-item-text').text.strip()
            category_href = link['href']
            self.categories[category_name] = category_href

        # Print the resulting dictionary
        print("Extracted categories:", self.categories)
                
    def scrape_products(self, category, category_url):
        url = f"https://www.trendyol.com{category_url}"
        print(f"Scraping URL for category '{category}': {url}")
        self.driver_manager.load_page(url)

        prev_product_count = 0
        total_products_scraped = 0
        max_products_per_category = 100

        while total_products_scraped < max_products_per_category:
            self.scroll_to_bottom()
            products = self.product_extractor.extract_products(category)
            current_product_count = len(self.product_extractor.product_urls)

            print(f"Current product count: {current_product_count}")
            print(f"Previous product count: {prev_product_count}")

            if products:
                count=1
                new_products = [product for product in products if total_products_scraped + len(products) <= max_products_per_category]
                self.all_products.extend(new_products)
                write_header = (total_products_scraped == 0)
                self.write_products_to_csv(new_products, write_header)
                count=count

                total_products_scraped += len(new_products)
            prev_product_count = current_product_count
            if current_product_count >= prev_product_count:
                print(f"No more products to load for category '{category}'.")
                break

            
                
            

        print(f"Scraped {total_products_scraped} products for category '{category}'")


    # def scrape_products(self,category,category_url):
    #     for page in range(1, self.num_pages + 1):
    #         try:
    #             url = f"{self.base_url}{category_url}"
    #             print(f"Scraping URL: {url}")  # Debugging output
    #             self.driver_manager.load_page(url)
    #             products = self.product_extractor.extract_products(category)

    #             if products:
    #                 # Assuming products is a list of dictionaries
    #                 for product in products:
    #                     self.product_urls.append(product['product_url'])  # Access product URL correctly
                    
    #                 self.all_products.extend(products)  # Append products to the list
    #                 write_header = (page == 1)  # Write header only for the first page
    #                 self.write_products_to_csv(products, write_header)
    #                 # self.db_manager.insert_product_data(products)  # Insert extracted product data into the database

    #             time.sleep(random.randint(3, 6))

    #         except TimeoutException:
    #             print(f"Timeout while loading page {page}")
    #         except Exception as e:
    #             print(f"Error scraping page: {e}")


    def write_products_to_csv(self, products, write_header):
        fieldnames = ['title', 'category','brand_name', 'short_description', 'product_url', 'image_url', 'social_proof', 'rating_score', 'review_count', 'price', 'badges']
        mode = 'a'  # Append mode
        try:
            with open(self.output_csv, mode, newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if write_header:
                    writer.writeheader()
                for product in products:
                    writer.writerow(product)
            print(f"Products saved to {self.output_csv}")
        except IOError as e:
            print(f"Error saving to CSV file: {e}")
