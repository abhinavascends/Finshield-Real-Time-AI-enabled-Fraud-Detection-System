import pandas as pd

from Feature_Generation import (
    extract_numerical_features,
    extract_categorical_features,
    scale_numerical_features,
    encode_categorical_features,
    combine_feature_representations,
    train_isolation_forest,
)


DATASET_PATH = "bank_transactions_featured.csv"


def test_isolation_forest_predictions():
    df = pd.read_csv(DATASET_PATH)

    numerical_features = extract_numerical_features(df)
    categorical_features = extract_categorical_features(df)

    scaled_numerical_features, _ = scale_numerical_features(
        numerical_features
    )

    encoded_categorical_features, _ = encode_categorical_features(
        categorical_features
    )

    combined_features = combine_feature_representations(
        scaled_numerical_features,
        encoded_categorical_features
    )

    model = train_isolation_forest(combined_features)

    predictions = model.predict(combined_features)

    assert len(predictions) == len(df)
    assert set(predictions).issubset({-1, 1})