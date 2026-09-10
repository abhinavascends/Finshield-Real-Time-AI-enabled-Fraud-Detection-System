import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier


# Paths
DATA_PATH = "bank_transactions_featured.csv"


# Load Dataset
df = pd.read_csv(
    DATA_PATH,
    parse_dates=["TransactionDate", "PreviousTransactionDate"]
)


# Feature Selection
drop_cols = [
    "TransactionID",
    "AccountID",
    "TransactionDate",
    "PreviousTransactionDate",
    "DeviceID",
    "IP Address",
    "MerchantID"
]

X = df.drop(columns=drop_cols)


# Scale numerical features
numeric_cols = X.select_dtypes(
    include=[np.number]
).columns.tolist()

scaler = StandardScaler()

X_numeric = pd.DataFrame(
    scaler.fit_transform(X[numeric_cols]),
    columns=numeric_cols
)


# One-hot encode categorical features
cat_cols = [
    "TransactionType",
    "Location",
    "Channel",
    "CustomerOccupation",
    "user_primary_location"
]

encoder = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)

X_cat = pd.DataFrame(
    encoder.fit_transform(X[cat_cols]),
    columns=encoder.get_feature_names_out(cat_cols)
)


# Combine features
X_combined = pd.concat(
    [X_numeric, X_cat],
    axis=1
)


# Train Isolation Forest
iso = IsolationForest(
    n_estimators=100,
    contamination=0.01,
    random_state=42
)

iso.fit(X_combined)


# Generate anomaly scores
scores = -iso.decision_function(X_combined)


# Generate supervised fraud labels
threshold = np.percentile(scores, 95)

df["is_fraud"] = (
    scores >= threshold
).astype(int)


# Prepare supervised training data
y = df["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X_combined,
    y,
    test_size=0.3,
    stratify=y,
    random_state=42
)


# Handle fraud class imbalance
negative_samples = (y_train == 0).sum()
positive_samples = (y_train == 1).sum()

scale_pos_weight = negative_samples / positive_samples


# Train XGBoost fraud classifier
xgb = XGBClassifier(
    scale_pos_weight=scale_pos_weight,
    random_state=42
)

xgb.fit(X_train, y_train)


if __name__ == "__main__":
    print("Supervised fraud labels generated successfully.")

    print("\nFraud label distribution:")
    print(df["is_fraud"].value_counts())

    print("\nTraining feature shape:", X_train.shape)
    print("Testing feature shape:", X_test.shape)

    print("\nTraining label distribution:")
    print(y_train.value_counts())

    print("\nTesting label distribution:")
    print(y_test.value_counts())

    print("\nClass imbalance configuration:")
    print("Negative samples:", negative_samples)
    print("Positive samples:", positive_samples)
    print("scale_pos_weight:", scale_pos_weight)

    print("\nXGBoost fraud classifier trained successfully.")