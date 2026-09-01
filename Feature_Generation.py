
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


if __name__ == "__main__":
    df = pd.read_csv(DATASET_PATH)
    numerical_features = extract_numerical_features(df)

    print("Numerical transaction features:")
    print(numerical_features.head())
    print("\nFeature shape:", numerical_features.shape)