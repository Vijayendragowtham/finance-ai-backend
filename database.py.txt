from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["finance_db"]
transactions_collection = db["transactions"]
