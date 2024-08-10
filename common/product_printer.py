class ProductPrinter:
    @staticmethod
    def print_product_data(product):
        print("Name:", product['name'])
        print("Description:", product['description'])
        print("Image URL:", product['img_url'])
        print("Price:", product['price'])
        print()

