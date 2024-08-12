from scraper_restaurant.product_scraper import ProductScraper as ProductScraper_restaurant
from common_restaurant.database_manager import DatabaseManager as DatabaseManager_restaurant
from common_trendyol.database_manager import DatabaseManager as DatabaseManager_trendyol
from scraper_trendyol.product_scraper import ProductScraper as ProductScraper_trendyol

# MySQL Connection Configuration
mysql_config = {
    'host': 'localhost',
    'database': 'prod_data',
    'user': 'root',
    'password': 'seecs@123'
}

if __name__ == "__main__":
    driver_path = r"C:\Users\user\OneDrive\Documents\chromedriver-win64\chromedriver.exe"
    restaurant_base_url = "https://www.yemeksepeti.com/restaurant/wfse/konyali-ahmet-usta-wfse"  # Replace with the actual base URL of the product category
    trendyol_base_url="https://www.trendyol.com/sr?mid=105012&os=1" 
    restaurant_output_csv = r"C:\Users\user\OneDrive\Documents\restaurant_scraper\data\food_items.csv"
    trendyol_output_csv = r"C:\Users\user\OneDrive\Documents\restaurant_scraper\data\trendyol_products.csv"
    url_to_scrape=input('Enter the url or website to scrape')
    

    if "trendyol" in url_to_scrape:
        try:
            db_manager = DatabaseManager_trendyol(mysql_config)
            db_manager.connect()
            scraper = ProductScraper_trendyol(driver_path, trendyol_base_url, trendyol_output_csv, db_manager)
            scraper.run()
        finally:
            db_manager.disconnect()
    else:         
        try:
            db_manager = DatabaseManager_restaurant(mysql_config)
            db_manager.connect()
            scraper = ProductScraper_restaurant(driver_path, restaurant_base_url, restaurant_output_csv, db_manager)
            scraper.run()
        finally:
            db_manager.disconnect()
