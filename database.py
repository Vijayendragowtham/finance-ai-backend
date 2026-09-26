import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017/"))
db = client[os.getenv("DATABASE_NAME", "finance_db")]
transactions_collection = db["transactions"]
