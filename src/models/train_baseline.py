from pathlib import Path

import numpy as np
import tensorflow as tf

from build_baseline_model import build_baseline_model

DATA_DIR = Path("data/processed")
RESULTS_DIR = Path("results/baseline")

RANDOM_SEED = 42
EPOCHS = 30
BATCH_SIZE = 64

def load_data():
    X_train = np.load(DATA_DIR / "X_train.npy")
    y_train = np.load(DATA_DIR / "y_train.npy")

    X_validation = np.load(DATA_DIR / "X_validation.npy")
    y_validation = np.load(DATA_DIR / "y_validation.npy")

    return X_train, y_train, X_validation, y_validation

def main():
    np.random.seed(RANDOM_SEED)
    tf.random.set_seed(RANDOM_SEED)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    X_train, y_train, X_validation, y_validation = load_data()

    print("Training data:")
    print(f" X_train: {X_train.shape}")
    print(f" y_train: {y_train.shape}")
    print(f" X_validation: {X_validation.shape}")
    print(f" y_validation: {y_validation.shape}")

    model = build_baseline_model()

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.summary()

    history = model.fit(
        X_train,
        y_train - 1,
        validation_data = (X_validation, y_validation - 1),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        shuffle=True,
        verbose=1,
    )

    model.save(RESULTS_DIR / "baseline_fp32.keras")

    history_path = RESULTS_DIR / "training_history.csv"

    history_array = np.column_stack(
        [
            np.arange(1, len(history.history["loss"]) + 1),
            history.history["loss"],
            history.history["accuracy"],
            history.history["val_loss"],
            history.history["val_accuracy"],
        ]
    )

    np.savetxt(history_path, history_array, delimiter=",", header="epoch,loss,accuracy,val_loss,val_accuracy",comments="")

    print(f"\nModel saved to: {RESULTS_DIR / 'baseline_fp32.keras'}")
    print(f"Training history saved to: {history_path}")

if __name__ == "__main__":
    main()