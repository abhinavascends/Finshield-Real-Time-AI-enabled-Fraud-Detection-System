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
    raise RuntimeError(
        "DATABASE_URL environment variable is not set"
    )


redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)


def save_transaction(transaction, fraud_probability=None, is_fraud=None):
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
                is_unusual_location,
                fraud_probability,
                is_fraud
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
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
                transaction.is_unusual_location,
                fraud_probability,
                is_fraud
            )
        )

        result = cursor.fetchone()
        if result is None:
            raise RuntimeError("Failed to retrieve transaction ID")

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


def get_transaction_history(limit=50):
    connection = psycopg2.connect(DATABASE_URL)

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                account_id,
                transaction_amount,
                location,
                event_time,
                fraud_probability,
                is_fraud
            FROM transactions
            ORDER BY event_time DESC
            LIMIT %s
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "account_id": row[1],
                "amount": row[2],
                "location": row[3],
                "event_time": row[4].isoformat()
                if row[4]
                else None,
                "fraud_probability": row[5],
                "is_fraud": row[6]
            }
            for row in rows
        ]

    finally:
        connection.close()


def get_alerts(limit=20):
    connection = psycopg2.connect(DATABASE_URL)

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                transaction_id,
                alert_type,
                created_at
            FROM alerts
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "transaction_id": row[1],
                "type": row[2],
                "time": row[3].isoformat()
                if row[3]
                else None
            }
            for row in rows
        ]

    finally:
        connection.close()