import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,)

DATA_DIR = Path("data/processed")
RESULTS_DIR = Path("results/baseline")
MODEL_PATH = RESULTS_DIR / "baseline_fp32.keras"

CLASS_NAMES = ["WALKING", "WALKING_UPSTAIRS", "WALKING_DOWNSTAIRS", "SITTING", "STANDING", "LYING"]

def main():
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    X_test = np.load(DATA_DIR / "X_test.npy")
    y_test = np.load(DATA_DIR / "y_test.npy").astype(int) - 1

    model = tf.keras.models.load_model(MODEL_PATH)

    test_loss, test_accuracy = model.evaluate(
        X_test, y_test, verbose=0
    )

    probabilites = model.predict(X_test, verbose=0)
    y_pred = np.argmax(probabilites, axis=1)

    report = classification_report(y_test,y_pred,labels=np.arange(6),target_names=CLASS_NAMES,output_dict=True,zero_division=0)

    matrix = confusion_matrix(y_test, y_pred, labels=np.arange(6))

    model_size_bytes = MODEL_PATH.stat().st_size

    metrics = {
        "evaluation_spilt": "original UCI-HAR test subjects",
        "test_windows" : int(len(y_test)),
        "test_loss": float(test_loss),
        "test_accuracy" : float(accuracy_score(y_test,y_pred)),
        "parameter_count": int(model.count_params()),
        "keras_model_file_size_bytes": int(model_size_bytes),
        "keras_model_file_size_kib": round(
            model_size_bytes / 1024, 2
        ),
        "classification_report": report,
        "confusion_matrix": matrix.tolist(),
        "class_names": CLASS_NAMES,
    }

    metrics_path = RESULTS_DIR / "test_metrics.json"
    with metrics_path.open("w") as f:
        json.dump(metrics, f, indent=2)

    fig, ax = plt.subplots(figsize=(9,7))
    image = ax.imshow(matrix)
    fig.colorbar(image, ax=ax)

    ax.set(
        xticks=np.arange(6),
        yticks=np.arange(6),
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
        xlabel="Predicted activity",
        ylabel="True activity",
        title="FP32 Baseline — UCI-HAR Test Confusion Matrix",
    )

    plt.setp(
        ax.get_xticklabels(),
        rotation=35,
        ha="right",
        rotation_mode="anchor",
    )

    threshold = matrix.max() / 2
    for i in range(6):
        for j in range(6):
            ax.text(
                j, i, str(matrix[i, j]),
                ha="center",
                va="center",
                color="white" if matrix[i, j] > threshold else "black",
            )

    fig.tight_layout()
    figure_path = RESULTS_DIR / "confusion_matrix.png"
    fig.savefig(figure_path, dpi=200)
    plt.close(fig)

    print(f"Test windows: {len(y_test)}")
    print(f"Test loss: {test_loss:.4f}")
    print(f"Test accuracy: {test_accuracy:.4f}")
    print(f"Parameters: {model.count_params():,}")
    print(f"Keras file size: {model_size_bytes:,} bytes")
    print("\nPer-class evaluation:")
    print(
        classification_report(
            y_test,
            y_pred,
            labels=np.arange(6),
            target_names=CLASS_NAMES,
            zero_division=0,
        )
    )
    print(f"Metrics saved to: {metrics_path}")
    print(f"Confusion matrix saved to: {figure_path}")


if __name__ == "__main__":
    main()
    