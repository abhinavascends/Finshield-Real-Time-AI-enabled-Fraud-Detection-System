import os
import onnxruntime as ort


MODEL_DIR = "model/artifacts"

onnx_model_path = os.path.join(
    MODEL_DIR,
    "fraud_detector.onnx"
)

optimized_model_path = os.path.join(
    MODEL_DIR,
    "fraud_detector_optimized.onnx"
)

session_options = ort.SessionOptions()

session_options.graph_optimization_level = (
    ort.GraphOptimizationLevel.ORT_ENABLE_ALL
)

session_options.optimized_model_filepath = optimized_model_path

ort.InferenceSession(
    onnx_model_path,
    session_options,
    providers=["CPUExecutionProvider"]
)

print(
    "Optimized ONNX model saved to:",
    optimized_model_path
)