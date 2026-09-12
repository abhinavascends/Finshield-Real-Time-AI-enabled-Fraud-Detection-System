from fastapi import FastAPI

from app.schemas import TransactionRequest


app = FastAPI(
    title="FinShield Fraud Detection API",
    version="1.0.0"
)


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/transactions/ingest")
def ingest_transaction(transaction: TransactionRequest):
    return {
        "message": "Transaction ingested successfully",
        "data": transaction.model_dump()
    }