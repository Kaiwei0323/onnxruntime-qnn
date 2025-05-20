import onnxruntime
import numpy as np
import onnxruntime as ort
print(ort.get_available_providers())
options = onnxruntime.SessionOptions()

# QNN DSP backend options
execution_provider_option = {
    "backend_path": "/home/aim/Documents/v2.26.0.240828/qairt/2.26.0.240828/lib/aarch64-ubuntu-gcc9.4/libQnnHtp.so",
    "enable_htp_fp16_precision": "1",
    "htp_performance_mode": "high_performance"
}

# Create ONNX Runtime session with QNNExecutionProvider
session = onnxruntime.InferenceSession("detr_resnet101_int8.onnx",
                                       sess_options=options,
                                       providers=["QNNExecutionProvider"],
                                       provider_options=[execution_provider_option])

# Generate input tensor in the correct data type (uint8)
input0 = np.ones((1, 3, 640, 640), dtype=np.float32)

# Run inference
result = session.run(None, {"input": input0})

# Print outputs
for i, output in enumerate(result):
    print(f"Output {i} shape: {output.shape}, dtype: {output.dtype}")

