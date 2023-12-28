import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os


class Database:
    """Client class for database connection to PostgreSQL instance"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()  # Load environment variables from .env file
            db_host = os.getenv('DB_HOST')
            db_port = os.getenv('DB_PORT')
            db_name = os.getenv('DB_DATABASE')
            db_user = os.getenv('DB_USER')
            db_password = os.getenv('DB_PASSWORD')

            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connection = cls._connect()
        return cls._instance

    @staticmethod
    def _connect():
        try:
            connection = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_DATABASE"),
                user=os.getenv("DB_USERNAME"),
                password=os.getenv("DB_PASSWORD")
            )
            return connection
        except psycopg2.Error as e:
            print(f"Error: Unable to connect to the database: {e}")
            raise

    def get_cursor(self):
        return self._connection.cursor()

    def close_connection(self):
        self._connection.close()

    def save(self, sql_command, params=None):
        cursor = self.get_cursor()
        cursor.execute(sql_command, params)
        self._connection.commit()

    def count(self, sql_command, params=None):
        cursor = self.get_cursor()
        cursor.execute(sql_command, params)
        return cursor.fetchone()[0]

    def fetch_all(self, sql_command, params=None):
        cursor = self.get_cursor()
        cursor.execute(sql_command, params)
        return cursor.fetchall()

    def fetch_one(self, sql_command, params=None):
        cursor = self.get_cursor()
        cursor.execute(sql_command, params)
        return cursor.fetchall()[0]
