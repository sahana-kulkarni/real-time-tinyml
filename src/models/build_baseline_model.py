import tensorflow as tf


INPUT_SHAPE = (128, 6)
NUM_CLASSES = 6


def build_baseline_model():
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=INPUT_SHAPE),

            tf.keras.layers.Conv1D(
                filters=16,
                kernel_size=5,
                padding="same",
            ),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.ReLU(),
            tf.keras.layers.MaxPooling1D(pool_size=2),

            tf.keras.layers.Conv1D(
                filters=32,
                kernel_size=5,
                padding="same",
            ),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.ReLU(),
            tf.keras.layers.MaxPooling1D(pool_size=2),

            tf.keras.layers.GlobalAveragePooling1D(),

            tf.keras.layers.Dense(32),
            tf.keras.layers.ReLU(),

            tf.keras.layers.Dense(NUM_CLASSES, activation="softmax"),
        ],
        name="baseline_cnn",
    )

    return model


if __name__ == "__main__":
    model = build_baseline_model()

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    model.summary()