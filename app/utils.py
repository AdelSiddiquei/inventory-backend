import psycopg
import pandas as pd
import os
from dotenv import load_dotenv

class Utils:
    def __init__(self):
        """Establishes a connection with the database upon instantiation.
        """
        # Load environment variables from .env file
        load_dotenv()

        # Create an instance of a connection to the PostgresSQL db using .env variables
        self.conn = psycopg.connect(
            dbname= os.getenv('POSTGRES_DBNAME'),
            host= os.getenv('POSTGRES_HOST'),
            port= os.getenv('POSTGRES_PORT'),
            user= os.getenv('POSTGRES_USER'),
            password= os.getenv('POSTGRES_PASSWORD')
        )

        # Autocommit so that changes don't need to be committed manually
        self.conn.autocommit = True

        self.cursor = self.conn.cursor()

    def new_stock(self, items: list[str], descriptions: list[str], prices: list[float]):
        if not(len(items)==len(descriptions)==len(prices)):
            return 'Error, arguments must be lists of equal size, even if it is a list of null entries for descriptions'
        for i in len(items):
            insert_query = f"INSERT INTO inventory (item, description, price) VALUES ({items[i]}, {descriptions[i]}, {prices[i]})"
            self.cursor.execute(insert_query)


        
        