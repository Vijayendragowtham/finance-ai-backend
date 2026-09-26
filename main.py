import os
from datetime import datetime, timezone

from bson import ObjectId
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from database import transactions_collection

load_dotenv()

app = FastAPI(title="AI Finance Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=200)


@app.get("/")
def home():
    return {"message": "Welcome to AI Finance Assistant API", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/expenses/")
def add_expense(expense: ExpenseCreate):
    document = {
        "amount": expense.amount,
        "category": expense.category,
        "description": expense.description,
        "type": "expense",
        "created_at": datetime.now(timezone.utc),
    }
    result = transactions_collection.insert_one(document)
    return {"message": "Expense added successfully", "id": str(result.inserted_id)}


@app.get("/expenses/")
def get_expenses():
    expenses = []
    for expense in transactions_collection.find().sort("created_at", -1):
        expenses.append({
            "id": str(expense["_id"]),
            "amount": expense["amount"],
            "category": expense["category"],
            "description": expense.get("description"),
            "type": expense.get("type", "expense"),
            "created_at": expense["created_at"],
        })
    return {"data": expenses}


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str):
    try:
        object_id = ObjectId(expense_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid expense ID")

    result = transactions_collection.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {"message": "Expense deleted successfully"}
