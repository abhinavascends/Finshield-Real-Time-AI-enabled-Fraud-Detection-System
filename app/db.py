import os

import psycopg2
import redis
from dotenv import load_dotenv


ENV_PATH = os.path.join(
    os.path.dirname(__file__),
    ".env"
)

load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379/0"
)

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")


redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)


def save_transaction(transaction):
    connection = psycopg2.connect(DATABASE_URL)

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO transactions (
                transaction_amount,
                customer_age,
                transaction_duration,
                login_attempts,
                account_balance,
                is_large_transaction,
                log_transaction_amount,
                transaction_hour,
                transaction_day_of_week,
                odd_hour_transaction,
                user_transaction_count,
                user_avg_transaction_amount,
                deviation_from_user_avg,
                transaction_type,
                location,
                channel,
                customer_occupation,
                user_primary_location,
                is_unusual_location
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            RETURNING id
            """,
            (
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
                transaction.TransactionType,
                transaction.Location,
                transaction.Channel,
                transaction.CustomerOccupation,
                transaction.user_primary_location,
                transaction.is_unusual_location
            )
        )

        result = cursor.fetchone()

        if result is None:
            raise RuntimeError(
                "Failed to retrieve the inserted transaction ID"
            )

        transaction_id = result[0]

        connection.commit()

        return transaction_id

    finally:
        connection.close()


def create_alert(transaction_id, score):
    connection = psycopg2.connect(DATABASE_URL)

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO alerts (
                transaction_id,
                alert_type
            )
            VALUES (%s, %s)
            """,
            (
                transaction_id,
                "HIGH_RISK"
            )
        )

        connection.commit()

    finally:
        connection.close()

    redis_client.xadd(
        "alerts",
        {
            "transaction_id": str(transaction_id),
            "score": str(score)
        }
    )