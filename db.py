import os
import pymongo
from dotenv import load_dotenv

load_dotenv()


def get_DB_connection() -> pymongo.MongoClient:
    return pymongo.MongoClient(os.getenv("DB_URL"))
