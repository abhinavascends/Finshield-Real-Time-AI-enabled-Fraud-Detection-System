from onnxmltools import convert_xgboost
from onnxmltools.convert.common.data_types import FloatTensorType
import joblib
import os


MODEL_DIR = "model/artifacts"

xgb_model_path = os.path.join(
    MODEL_DIR,
    "xgb_model.pkl"
)

onnx_model_path = os.path.join(
    MODEL_DIR,
    "fraud_detector.onnx"
)

xgb = joblib.load(xgb_model_path)

feature_dim = xgb.n_features_in_

booster = xgb.get_booster()
booster.feature_names = [
    f"f{i}" for i in range(feature_dim)
]

initial_type = [
    ("float_input", FloatTensorType([None, feature_dim]))
]

onnx_model = convert_xgboost(
    xgb,
    initial_types=initial_type
)

with open(onnx_model_path, "wb") as f:
    f.write(onnx_model.SerializeToString())

print("ONNX model saved to:", onnx_model_path)