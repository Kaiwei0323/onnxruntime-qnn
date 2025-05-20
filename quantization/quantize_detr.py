import os
import numpy as np
from PIL import Image
from onnxruntime.quantization import quantize_static, CalibrationDataReader, QuantType
from onnxruntime.quantization import QuantType
from onnxruntime.quantization import QuantFormat
print(list(QuantType))


# Confirm the input name (you already told me it's "image")
input_name = "image"

# Define a calibration data reader
class DetrCalibrationDataReader(CalibrationDataReader):
    def __init__(self, image_folder, input_name):
        self.image_folder = image_folder
        self.input_name = input_name
        self.enum_data = None
        self.preprocess()

    def preprocess(self):
        self.data = []
        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(".jpg"):
                image_path = os.path.join(self.image_folder, filename)
                img = Image.open(image_path).convert("RGB").resize((640, 640))
                img_data = np.array(img).astype(np.float32) / 255.0
                img_data = img_data.transpose(2, 0, 1)  # HWC to CHW
                img_data = np.expand_dims(img_data, axis=0)  # Add batch dimension
                self.data.append({self.input_name: img_data})
        self.enum_data = iter(self.data)

    def get_next(self):
        return next(self.enum_data, None)

# Instantiate reader
reader = DetrCalibrationDataReader("test_img", input_name)

# Run quantization
quantize_static(
    model_input="detr_resnet101.onnx",
    model_output="detr_resnet101_int8.onnx",
    calibration_data_reader=reader,
    quant_format=QuantFormat.QDQ,
    activation_type=QuantType.QInt8,
    weight_type=QuantType.QInt8,
    per_channel=True
)

print("✅ Quantization complete. Output: detr_resnet101_int8")

