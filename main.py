
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(title="Expense Tracker API")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Expense Tracker API is running!"}


@app.post("/transactions", response_model=schemas.TransactionResponse)
def add_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    new_transaction = models.Transaction(**transaction.model_dump())

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


@app.get("/transactions", response_model=list[schemas.TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    return (
        db.query(models.Transaction)
        .order_by(models.Transaction.date.desc())
        .all()
    )


@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted successfully"}


@app.put(
    "/transactions/{transaction_id}",
    response_model=schemas.TransactionResponse
)
def update_transaction(
    transaction_id: int,
    updated_data: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    transaction.description = updated_data.description
    transaction.amount = updated_data.amount
    transaction.transaction_type = updated_data.transaction_type
    transaction.category = updated_data.category
    transaction.date = updated_data.date

    db.commit()
    db.refresh(transaction)

    return transaction

