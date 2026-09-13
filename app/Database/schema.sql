CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    account_id VARCHAR(255),

    transaction_amount FLOAT,
    customer_age INT,
    transaction_duration FLOAT,
    login_attempts INT,
    account_balance FLOAT,

    is_large_transaction INT,
    log_transaction_amount FLOAT,
    transaction_hour INT,
    transaction_day_of_week INT,
    odd_hour_transaction INT,

    user_transaction_count FLOAT,
    user_avg_transaction_amount FLOAT,
    deviation_from_user_avg FLOAT,

    transaction_type VARCHAR(50),
    location VARCHAR(255),
    channel VARCHAR(50),
    customer_occupation VARCHAR(100),
    user_primary_location VARCHAR(255),

    is_unusual_location INT,

    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fraud_probability FLOAT,
    is_fraud BOOLEAN
);

CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    transaction_id INT REFERENCES transactions(id) ON DELETE CASCADE,
    alert_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);