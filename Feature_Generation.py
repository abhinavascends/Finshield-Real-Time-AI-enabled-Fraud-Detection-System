
import pandas as pd

DATASET_PATH = "bank_transactions_featured.csv"

NUMERICAL_FEATURES = [
    "TransactionAmount",
    "CustomerAge",
    "TransactionDuration",
    "LoginAttempts",
    "AccountBalance",
]

def extract_numerical_features(df):
    return df[NUMERICAL_FEATURES].copy()



CATEGORICAL_FEATURES = [
    "TransactionType",
    "Channel",
    "CustomerOccupation",
    "Location",
]
def extract_categorical_features(df):
    return df[CATEGORICAL_FEATURES].copy()

USER_BEHAVIOR_FEATURES = [
    "user_transaction_count",
    "user_avg_transaction_amount",
]
def extract_user_behavior_features(df):
    return df[USER_BEHAVIOR_FEATURES].copy()

if __name__ == "__main__":
    df = pd.read_csv(DATASET_PATH)

    numerical_features = extract_numerical_features(df)

    print("Numerical transaction features:")
    print(numerical_features.head())
    print("\nFeature shape:", numerical_features.shape)

    categorical_features = extract_categorical_features(df)

    print("\nCategorical transaction features:")
    print(categorical_features.head())
    print("\nCategorical feature shape:", categorical_features.shape)
    
    user_behavior_features = extract_user_behavior_features(df)

    print("\nUser behavior features:")
    print(user_behavior_features.head())
    print("\nUser behavior feature shape:", user_behavior_features.shape)