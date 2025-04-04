from fastapi import FastAPI
from database import transactions_collection

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to AI Finance Assistant"}

@app.post("/add-expense/")
def add_expense(amount: float, category: str):
    data = {"amount": amount, "category": category}
    transactions_collection.insert_one(data)
    return {"message": "Expense added successfully!"}

@app.get("/expenses/")
def get_expenses():
    expenses = list(transactions_collection.find({}, {"_id": 0}))
    return {"data": expenses}

