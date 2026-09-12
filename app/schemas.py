from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    TransactionAmount: float = Field(gt=0)
    CustomerAge: int = Field(gt=0)
    TransactionDuration: float = Field(ge=0)
    LoginAttempts: int = Field(ge=0)
    AccountBalance: float = Field(ge=0)

    is_large_transaction: int = Field(ge=0, le=1)
    log_transaction_amount: float
    transaction_hour: int = Field(ge=0, le=23)
    transaction_day_of_week: int = Field(ge=0, le=6)
    odd_hour_transaction: int = Field(ge=0, le=1)

    user_transaction_count: float = Field(ge=0)
    user_avg_transaction_amount: float = Field(ge=0)
    deviation_from_user_avg: float

    TransactionType: str
    Location: str
    Channel: str
    CustomerOccupation: str
    user_primary_location: str

    is_unusual_location: int = Field(ge=0, le=1)