from common_restaurant.product_printer import ProductPrinter
from common_restaurant.html_parser import HtmlParser
from selenium.webdriver.common.by import By
import csv
class ProductExtractor:
    def __init__(self, driver):
        self.driver = driver

    def extract_products(self):
        categories=self.extract_categories()
        self.append_categories_to_products(categories)
        # elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="menu-product"]')
        # products = []
        # for element in elements:
        #     try:
        #         soup = HtmlParser.parse_html(element)
        #         product_data = self.extract_product_data(soup)
        #         if product_data:
        #             products.append(product_data)
        #             ProductPrinter.print_product_data(product_data)
        #         break #edit here
        #     except Exception as e:
        #         print(f"Error extracting product data: {e}")
        #         continue
        # return products
    

    def extract_product_data(self, soup):
        try:
            # Print the soup to debug and verify HTML structure
            print(soup.prettify())

            # Extract the product title
            title_element = soup.find('span', {'data-testid': 'menu-product-name'})
            name = title_element.get_text(strip=True) if title_element else 'N/A'

            # Extract the product price
            price_element = soup.find('p', {'data-testid': 'menu-product-price'})
            price = price_element.get_text(strip=True) if price_element else 'N/A'

            # Extract the product description
            description_element = soup.find('p', {'data-testid': 'menu-product-description'})
            description = description_element.get_text(strip=True) if description_element else 'N/A'

            # Extract the product URL (assuming it's inside a button or some clickable overlay)
            product_url_element = soup.find('button', {'data-testid': 'menu-product-button-overlay-id'})
            product_url = product_url_element.get('aria-label', '').split('-')[0].strip() if product_url_element else 'N/A'

            # Extract the image URL
            image_div = soup.find('div', {'data-testid': 'menu-product-image'})
            style_attr = image_div.get('style') if image_div else ''
            image_url = style_attr.split('url(')[-1].split(')')[0].strip('"') if 'url(' in style_attr else 'N/A'

            product_data = {
                'name': name,
                'description': description,
                'image_url': image_url,
                'price': price,
            }

            return product_data

        except Exception as e:
            print(f"Error extracting data: {e}")
            return None


    def extract_categories(self):
        # Find the element containing categories
        category_container = self.driver.find_element(By.CSS_SELECTOR, '#tabs__tablist')

        # Initialize BeautifulSoup
        soup = HtmlParser.parse_html(category_container)

        # Find all category items
        category_items = soup.select('li.bds-c-tab > button > span.bds-c-tab__label')

        # Create a dictionary to store categories and their product counts
        categories = {}

        for item in category_items:
            text = item.get_text(strip=True)
            if '(' in text and ')' in text:
                category_name = text.split('(')[0].strip()
                product_count = text.split('(')[1].replace(')', '').strip()
                categories[category_name] = product_count

        return categories
    
    def append_categories_to_products(self, categories):
        # Read the existing CSV file and append categories
        with open('products.csv', 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)
            rows = list(reader)

        # Add the category column to the header
        header.append('Category')

        # Open the CSV file for writing
        with open('products_with_categories.csv', 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)

            # Append the category information to each product
            for row in rows:
                product_name = row[0]  # Assuming the first column is 'name'
                product_category = None

                for category, count in categories.items():
                    if product_name in category:  # Adjust this condition based on how products are matched to categories
                        product_category = category
                        break

                row.append(product_category if product_category else 'Unknown')
                writer.writerow(row)

        print("Categories have been appended to products_with_categories.csv")