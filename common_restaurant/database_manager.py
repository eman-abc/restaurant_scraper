import mysql.connector


class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def insert_product_data(self, product_data):
        insert_query = """
        INSERT INTO restaurant (
            name, description, image_url, price
        ) VALUES (
            %s, %s, %s, %s
        )
        """
        try:
            for data in product_data:
                
                self.cursor.execute(insert_query, (
                    data['name'],
                    data['description'],
                    data['img_url'],
                    data['price'],
                ))
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting data: {err}")
            self.conn.rollback()
