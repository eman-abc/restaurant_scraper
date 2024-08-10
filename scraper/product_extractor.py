from common.product_printer import ProductPrinter
from common.html_parser import HtmlParser
from selenium.webdriver.common.by import By

class ProductExtractor:
    def __init__(self, driver):
        self.driver = driver

    def extract_products(self):
        elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="menu-product"]')
        products = []
        for element in elements:
            try:
                soup = HtmlParser.parse_html(element)
                product_data = self.extract_product_data(soup)
                if product_data:
                    products.append(product_data)
                    ProductPrinter.print_product_data(product_data)
                break #edit here
            except Exception as e:
                print(f"Error extracting product data: {e}")
                continue
        return products

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
