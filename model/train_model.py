import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, OneHotEncoder


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


if __name__ == "__main__":
    print("Supervised fraud labels generated successfully.")

    print("\nFraud label distribution:")
    print(df["is_fraud"].value_counts())

    print("\nFraud label preview:")
    print(df[["is_fraud"]].head())