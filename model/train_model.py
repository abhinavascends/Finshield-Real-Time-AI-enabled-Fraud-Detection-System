import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
from xgboost import XGBClassifier


DATA_PATH = "bank_transactions_featured.csv"
OUTPUT_DIR = "model/artifacts"

os.makedirs(OUTPUT_DIR, exist_ok=True)


df = pd.read_csv(
    DATA_PATH,
    parse_dates=["TransactionDate", "PreviousTransactionDate"]
)

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


numeric_cols = X.select_dtypes(
    include=[np.number]
).columns.tolist()

scaler = StandardScaler()

X_numeric = pd.DataFrame(
    scaler.fit_transform(X[numeric_cols]),
    columns=numeric_cols
)

joblib.dump(
    scaler,
    os.path.join(OUTPUT_DIR, "scaler.pkl")
)


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

joblib.dump(
    encoder,
    os.path.join(OUTPUT_DIR, "onehot_encoder.pkl")
)


X_combined = pd.concat(
    [X_numeric, X_cat],
    axis=1
)


iso = IsolationForest(
    n_estimators=100,
    contamination=0.01,
    random_state=42
)

iso.fit(X_combined)

scores = -iso.decision_function(X_combined)

threshold = np.percentile(scores, 95)

df["is_fraud"] = (
    scores >= threshold
).astype(int)


y = df["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X_combined,
    y,
    test_size=0.3,
    stratify=y,
    random_state=42
)


negative_samples = (y_train == 0).sum()
positive_samples = (y_train == 1).sum()

scale_pos_weight = (
    negative_samples / positive_samples
)


xgb = XGBClassifier(
    scale_pos_weight=scale_pos_weight,
    random_state=42
)

xgb.fit(
    X_train,
    y_train
)


xgb_model_path = os.path.join(
    OUTPUT_DIR,
    "xgb_model.pkl"
)

joblib.dump(
    xgb,
    xgb_model_path
)


fraud_probabilities = xgb.predict_proba(
    X_test
)[:, 1]

y_pred = xgb.predict(
    X_test
)


classification_metrics = str(
    classification_report(
        y_test,
        y_pred
    )
)


roc_auc = roc_auc_score(
    y_test,
    fraud_probabilities
)


report_path = os.path.join(
    OUTPUT_DIR,
    "classification_report.txt"
)

with open(report_path, "w") as f:
    f.write(classification_metrics)
    f.write(
        f"\nROC-AUC: {roc_auc:.4f}\n"
    )


fpr, tpr, _ = roc_curve(
    y_test,
    fraud_probabilities
)

plt.plot(
    fpr,
    tpr,
    label=f"XGBoost (AUC = {roc_auc:.4f})"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Fraud Detection ROC Curve")
plt.legend()


roc_curve_path = os.path.join(
    OUTPUT_DIR,
    "roc_curve.png"
)

plt.savefig(
    roc_curve_path
)

plt.close()


if __name__ == "__main__":
    print("Fraud label distribution:")
    print(df["is_fraud"].value_counts())

    print("\nTraining shape:", X_train.shape)
    print("Testing shape:", X_test.shape)

    print(
        "\nscale_pos_weight:",
        scale_pos_weight
    )

    print("\nClassification metrics:")
    print(classification_metrics)

    print("\nROC-AUC:", roc_auc)

    print("\nSaved:", report_path)
    print("Saved:", roc_curve_path)
    print(
        "Saved:",
        os.path.join(
            OUTPUT_DIR,
            "scaler.pkl"
        )
    )
    print(
        "Saved:",
        os.path.join(
            OUTPUT_DIR,
            "onehot_encoder.pkl"
        )
    )