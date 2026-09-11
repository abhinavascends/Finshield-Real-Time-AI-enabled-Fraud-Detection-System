from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    TransactionAmount: float = Field(gt=0)
    CustomerAge: int = Field(gt=0)
    TransactionDuration: int = Field(ge=0)
    LoginAttempts: int = Field(ge=0)
    AccountBalance: float = Field(ge=0)

    TransactionType: str
    Channel: str
    CustomerOccupation: str
    Location: str

    user_transaction_count: int = Field(ge=0)
    user_avg_transaction_amount: float = Field(ge=0)

    transaction_hour: int = Field(ge=0, le=23)
    transaction_day_of_week: int = Field(ge=0, le=6)

    is_unusual_location: int = Field(ge=0, le=1)