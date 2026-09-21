import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder


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

TEMPORAL_FEATURES = [
    "transaction_hour",
    "transaction_day_of_week",
]


def extract_temporal_features(df):
    return df[TEMPORAL_FEATURES].copy()

LOCATION_ANOMALY_FEATURES = [
    "is_unusual_location",
]


def extract_location_anomaly_features(df):
    return df[LOCATION_ANOMALY_FEATURES].copy()

def generate_transaction_features(df):
    numerical_features = extract_numerical_features(df)
    categorical_features = extract_categorical_features(df)
    user_behavior_features = extract_user_behavior_features(df)

    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])
    df["transaction_hour"] = df["TransactionDate"].dt.hour
    df["transaction_day_of_week"] = df["TransactionDate"].dt.dayofweek

    temporal_features = extract_temporal_features(df)
    location_features = extract_location_anomaly_features(df)

    return pd.concat(
        [
            numerical_features,
            categorical_features,
            user_behavior_features,
            temporal_features,
            location_features,
        ],
        axis=1,
    )
    
def scale_numerical_features(numerical_features):
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(numerical_features)

    return scaled_features, scaler

def encode_categorical_features(categorical_features):
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    encoded_features = encoder.fit_transform(categorical_features)

    return encoded_features, encoder

def combine_feature_representations(
    scaled_numerical_features,
    encoded_categorical_features
):
    return np.hstack(
        [
            scaled_numerical_features,
            encoded_categorical_features,
        ]
    )

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
    
    df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])

    df["transaction_hour"] = df["TransactionDate"].dt.hour
    df["transaction_day_of_week"] = df["TransactionDate"].dt.dayofweek

    temporal_features = extract_temporal_features(df)

    print("\nTransaction temporal features:")
    print(temporal_features.head())
    print("\nTemporal feature shape:", temporal_features.shape)
    
    location_anomaly_features = extract_location_anomaly_features(df)

    print("\nLocation anomaly features:")
    print(location_anomaly_features.head())
    print(
        "\nLocation anomaly feature shape:",
        location_anomaly_features.shape
    )
    
    transaction_features = generate_transaction_features(df)

    print("\nFinal transaction feature set:")
    print(transaction_features.head())
    print("\nFinal feature shape:", transaction_features.shape)
    
    scaled_numerical_features, scaler = scale_numerical_features(
        numerical_features
    )

    print("\nScaled numerical features:")
    print(scaled_numerical_features[:5])
    print("\nScaled feature shape:", scaled_numerical_features.shape)
    
    encoded_categorical_features, encoder = encode_categorical_features(
        categorical_features
    )

    print("\nEncoded categorical features:")
    print(encoded_categorical_features[:5])
    print(
        "\nEncoded categorical feature shape:",
        encoded_categorical_features.shape
    )
