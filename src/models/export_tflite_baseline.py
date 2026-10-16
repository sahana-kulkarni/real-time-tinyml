
from pathlib import Path
import json

import numpy as np
import tensorflow as tf

MODEL_PATH = Path("results/baseline/baseline_fp32.keras")
OUTPUT_DIR = Path("results/quantization")
TFLITE_PATH = OUTPUT_DIR / "baseline_fp32.tflite"
REPORT_PATH = OUTPUT_DIR / "baseline_fp32_conversion.json"
DATA_PATH = Path("data/processed/X_test.npy")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    model = tf.keras.models.load_model(MODEL_PATH)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    TFLITE_PATH.write_bytes(tflite_model)

    interpreter = tf.lite.Interpreter(model_path=str(TFLITE_PATH))
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    X_test = np.load(DATA_PATH, mmap_mode="r")
    sample_count = min(100, len(X_test))
    X_sample = np.asarray(X_test[:sample_count], dtype=np.float32)

    keras_predictions = model.predict(X_sample, verbose=0)

    tflite_predictions = []
    for sample in X_sample:
        input_tensor = np.expand_dims(sample, axis=0)
        interpreter.set_tensor(input_details[0]["index"], input_tensor)
        interpreter.invoke()
        prediction = interpreter.get_tensor(output_details[0]["index"])
        tflite_predictions.append(prediction[0])

    tflite_predictions = np.asarray(tflite_predictions)

    max_abs_difference = float(
        np.max(np.abs(keras_predictions - tflite_predictions))
    )
    mean_abs_difference = float(
        np.mean(np.abs(keras_predictions - tflite_predictions))
    )

    report = {
        "model_type": "FP32 TensorFlow Lite",
        "source_model": str(MODEL_PATH),
        "test_samples_compared": sample_count,
        "keras_model_size_bytes": MODEL_PATH.stat().st_size,
        "tflite_model_size_bytes": TFLITE_PATH.stat().st_size,
        "tflite_input_shape": input_details[0]["shape"].tolist(),
        "tflite_input_dtype": str(input_details[0]["dtype"]),
        "tflite_output_shape": output_details[0]["shape"].tolist(),
        "tflite_output_dtype": str(output_details[0]["dtype"]),
        "max_absolute_prediction_difference": max_abs_difference,
        "mean_absolute_prediction_difference": mean_abs_difference,
        "predicted_class_agreement": float(
            np.mean(
                np.argmax(keras_predictions, axis=1)
                == np.argmax(tflite_predictions, axis=1)
            )
        ),
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")

    print("FP32 TensorFlow Lite export completed.")
    print(f"Model saved: {TFLITE_PATH}")
    print(f"Report saved: {REPORT_PATH}")
    print(f"Keras model size: {report['keras_model_size_bytes']:,} bytes")
    print(f"TFLite model size: {report['tflite_model_size_bytes']:,} bytes")
    print(f"Input dtype: {input_details[0]['dtype']}")
    print(f"Output dtype: {output_details[0]['dtype']}")
    print(f"Max absolute prediction difference: {max_abs_difference:.8f}")
    print(f"Mean absolute prediction difference: {mean_abs_difference:.8f}")
    print(f"Predicted class agreement: {report['predicted_class_agreement']:.2%}")


if __name__ == "__main__":
    main()