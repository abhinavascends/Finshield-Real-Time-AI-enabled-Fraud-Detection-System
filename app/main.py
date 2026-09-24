import joblib
import numpy as np
import onnxruntime as ort

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import save_transaction, create_alert

from app.auth import (
    LoginRequest,
    authenticate_user,
    create_token,
    get_current_user
)
from app.db import (
    create_alert,
    get_alerts,
    get_transaction_history,
    save_transaction
)
from app.schemas import TransactionRequest


MODEL_PATH = "model/artifacts/fraud_detector_optimized.onnx"
SCALER_PATH = "model/artifacts/scaler.pkl"
ENCODER_PATH = "model/artifacts/onehot_encoder.pkl"


app = FastAPI(
    title="FinShield Fraud Detection API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
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


@app.post("/token")
def login(request: LoginRequest):
    if not authenticate_user(
        request.username,
        request.password
    ):
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    token = create_token(
        {
            "sub": request.username
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.get("/protected")
def protected_route(
    current_user: str = Depends(get_current_user)
):
    return {
        "message": "Authentication successful",
        "user": current_user
    }


@app.post("/transactions/ingest")
def ingest_transaction(
    transaction: TransactionRequest,
    current_user: str = Depends(get_current_user)
):
    transaction_id = save_transaction(
        transaction
    )

    return {
        "message": "Transaction ingested successfully",
        "transaction_id": transaction_id,
        "user": current_user,
        "data": transaction.model_dump()
    }



@app.post("/transactions/score")
def score_transaction(
    transaction: TransactionRequest,
    current_user: str = Depends(get_current_user)
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

    scaled_features = scaler.transform(numerical_features)

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
    outputs = onnx_session.run(None, {input_name: features})
    probabilities = outputs[1]

    if isinstance(probabilities, list):
        fraud_probability = float(probabilities[0][1])
    else:
        fraud_probability = float(np.asarray(probabilities)[0][1])

    is_fraud = fraud_probability >= 0.3

    transaction_id = save_transaction(
    transaction,
    fraud_probability=fraud_probability,
    is_fraud=is_fraud
)

    if is_fraud:
        create_alert(transaction_id, fraud_probability)

    return {
        "transaction_id": transaction_id,
        "fraud_probability": fraud_probability,
        "is_fraud": is_fraud,
        "user": current_user
    }


@app.get("/transactions/history")
def transaction_history(
    current_user: str = Depends(get_current_user)
):
    return get_transaction_history()


@app.get("/alerts")
def alerts(
    current_user: str = Depends(get_current_user)
):
    return get_alerts()