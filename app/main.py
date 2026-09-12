import joblib
import numpy as np
import onnxruntime as ort

from fastapi import FastAPI

from app.schemas import TransactionRequest


MODEL_PATH = "model/artifacts/fraud_detector_optimized.onnx"
SCALER_PATH = "model/artifacts/scaler.pkl"
ENCODER_PATH = "model/artifacts/onehot_encoder.pkl"


app = FastAPI(
    title="FinShield Fraud Detection API",
    version="1.0.0"
)


onnx_session = ort.InferenceSession(
    MODEL_PATH,
    providers=["CPUExecutionProvider"]
)

scaler = joblib.load(SCALER_PATH)
encoder = joblib.load(ENCODER_PATH)


@app.get("/")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/transactions/ingest")
def ingest_transaction(
    transaction: TransactionRequest
):
    return {
        "message": "Transaction ingested successfully",
        "data": transaction.model_dump()
    }


@app.post("/transactions/score")
def score_transaction(
    transaction: TransactionRequest
):
    numerical_features = np.array([
        [
            transaction.TransactionAmount,
            transaction.CustomerAge,
            transaction.TransactionDuration,
            transaction.LoginAttempts,
            transaction.AccountBalance,
            transaction.is_large_transaction,
            transaction.log_transaction_amount,
            transaction.transaction_hour,
            transaction.transaction_day_of_week,
            transaction.odd_hour_transaction,
            transaction.user_transaction_count,
            transaction.user_avg_transaction_amount,
            transaction.deviation_from_user_avg,
            transaction.is_unusual_location
        ]
    ])

    scaled_features = scaler.transform(
        numerical_features
    )

    categorical_features = encoder.transform([
        [
            transaction.TransactionType,
            transaction.Location,
            transaction.Channel,
            transaction.CustomerOccupation,
            transaction.user_primary_location
        ]
    ])

    features = np.hstack([
        scaled_features,
        categorical_features
    ]).astype(np.float32)

    input_name = onnx_session.get_inputs()[0].name

    outputs = onnx_session.run(
        None,
        {
            input_name: features
        }
    )

    probabilities = outputs[1]

    if isinstance(probabilities, list):
        fraud_probability = float(
            probabilities[0][1]
        )
    else:
        fraud_probability = float(
            np.asarray(probabilities)[0][1]
        )

    is_fraud = fraud_probability >= 0.3

    return {
        "fraud_probability": fraud_probability,
        "is_fraud": is_fraud
    }