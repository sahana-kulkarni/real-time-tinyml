from pathlib import Path
import json

import numpy as np
from sklearn.model_selection import train_test_split

#Configuration

DATASET_ROOT = Path("data/raw/UCI HAR Dataset")

TRAIN_DIR = DATASET_ROOT / "train"
TEST_DIR = DATASET_ROOT / "test"

OUTPUT_DIR = Path("data/processed")

CONFIG_DIR = Path("configs")

RANDOM_SEED = 42

#Number of validation subjects selected from the original
# UCI-HAR training subjects.
NUM_VALIDATION_SUBJECTS = 6

#Six input chanels used by the baseline model.
SIGNAL_NAMES = [
    "total_acc_x", "total_acc_y", "total_acc_z",
    "body_gyro_x", "body_gyro_y", "body_gyro_z",
]

#Utility functions

def load_vector(path):
    """Load a one-column text file."""
    return np.loadtxt(path, dtype=int)

def load_signal_set(directory, split):
    """
    Load the six selected inertial signals.

    Returns
    -------
    np.ndarray
        Shape: (N, 128, 6)
    """

    signals = []

    for signal_name in SIGNAL_NAMES:
        filename = f"{signal_name}_{split}.txt"
        path = directory / "Inertial Signals" / filename

        if not path.exists():
            raise FileNotFoundError(f"Missing signal file: {path}")
    
        data = np.loadtxt(path, dtype=np.float32)

        signals.append(data)

    # Each signal currently has shape:
    # (N, 128)
    # Stack along the chanel dimension:
    # (N, 128, 6)

    X = np.stack(signals, axis=-1)

    return X

def print_split_summary(name, X, y, subjects):
    """Print useful information about a dataset partition."""

    print(f"\n{name}")
    print("-" * 60)

    print(f"Windows: {len(X)}")
    print(f"Shape: {X.shape}")
    print(f"Subjects: {len(np.unique(subjects))}")
    print(f"Subject IDs: {sorted(np.unique(subjects).tolist())}")

    print("Class distribution:")

    for class_id in sorted(np.unique(y)):
        count = np.sum(y == class_id)
        print(f" Class {class_id}: {count}")
    
# Dataset loading

print("=" * 60)
print("UCI-HAR PREPROCESSING")
print("=" * 60)

print("\nLoading training signals...")

X_original_train = load_signal_set(TRAIN_DIR, "train")

y_original_train = load_vector(
    TRAIN_DIR / "y_train.txt"
)

subjects_original_train = load_vector(
    TRAIN_DIR / "subject_train.txt"
)

print(f"Original training shape: {X_original_train.shape}")

print("\nLoading test signals...")

X_test = load_signal_set(TEST_DIR, "test")

y_test = load_vector(
    TEST_DIR / "y_test.txt"
)

subjects_test = load_vector(
    TEST_DIR / "subject_test.txt"
)

print(f"Original test shape: {X_test.shape}")

# Verify dimensions

assert X_original_train.shape[0] == len(y_original_train)
assert X_original_train.shape[0] == len(subjects_original_train)

assert X_test.shape[0] == len(y_test)
assert X_test.shape[0] == len(subjects_test)

assert X_original_train.shape[1:] == (128,6)
assert X_test.shape[1:] == (128,6)

# Subject-level train/validation spilt

all_training_subjects = np.unique(subjects_original_train)

train_subjects, validation_subjects = train_test_split(
    all_training_subjects,
    test_size=NUM_VALIDATION_SUBJECTS,
    random_state=RANDOM_SEED,
    shuffle=True,
)

train_subjects = np.sort(train_subjects)
validation_subjects = np.sort(validation_subjects)

print("\nSubject spilt:")
print(f"Training subjects: {train_subjects}")
print(f"Validation subjects: {validation_subjects}")
print(f"Test subjects: {np.unique(subjects_test)}")

# Verify subject separation

assert len(np.intersect1d(train_subjects, validation_subjects)) == 0
assert len(np.intersect1d(train_subjects, subjects_test)) == 0
assert len(np.intersect1d(validation_subjects, subjects_test)) == 0

print("\nSubject separation: PASS")

# Selct windows by subject

train_mask = np.isin(
    subjects_original_train,
    train_subjects
)

validation_mask = np.isin(
    subjects_original_train,
    validation_subjects
)

X_train = X_original_train[train_mask]
y_train = y_original_train[train_mask]
subjects_train = subjects_original_train[train_mask]

X_validation = X_original_train[validation_mask]
y_validation = y_original_train[validation_mask]
subjects_validation = subjects_original_train[validation_mask]

# Training-only normalization

# Calculate mean and standard deviation across:
#   - all training windows
#   - all 128 time steps
#
# independently for each of the six channels.

channel_mean = X_train.mean(axis=(0,1))
channel_std = X_train.std(axis=(0,1))

# Avoid division by zero.
if np.any(channel_std == 0):
    raise ValueError("At least one channel has zero standard deviation.")

# Apply the SAME training statistics to all partitions.

X_train = (X_train - channel_mean) / channel_std

X_validation = (X_validation - channel_mean) / channel_std

X_test = (X_test - channel_mean) / channel_std

# Verify normlization

train_mean_after = X_train.mean(axis=(0, 1))
train_std_after = X_train.std(axis=(0, 1))

print("\nTraining normalization check:")

for i, signal_name in enumerate(SIGNAL_NAMES):
    print(
        f"{signal_name:15s} "
        f"mean={train_mean_after[i]: .6f} "
        f"std={train_std_after[i]: .6f}"
    )


# ============================================================
# Print dataset summaries
# ============================================================

print_split_summary(
    "TRAINING SET",
    X_train,
    y_train,
    subjects_train,
)

print_split_summary(
    "VALIDATION SET",
    X_validation,
    y_validation,
    subjects_validation,
)

print_split_summary(
    "TEST SET",
    X_test,
    y_test,
    subjects_test,
)


# ============================================================
# Save processed arrays
# ============================================================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

np.save(OUTPUT_DIR / "X_train.npy", X_train.astype(np.float32))
np.save(OUTPUT_DIR / "y_train.npy", y_train.astype(np.int64))

np.save(
    OUTPUT_DIR / "X_validation.npy",
    X_validation.astype(np.float32)
)

np.save(
    OUTPUT_DIR / "y_validation.npy",
    y_validation.astype(np.int64)
)

np.save(OUTPUT_DIR / "X_test.npy", X_test.astype(np.float32))
np.save(OUTPUT_DIR / "y_test.npy", y_test.astype(np.int64))

np.save(
    OUTPUT_DIR / "subjects_train.npy",
    subjects_train.astype(np.int64)
)

np.save(
    OUTPUT_DIR / "subjects_validation.npy",
    subjects_validation.astype(np.int64)
)

np.save(
    OUTPUT_DIR / "subjects_test.npy",
    subjects_test.astype(np.int64)
)


# ============================================================
# Save preprocessing configuration
# ============================================================

preprocessing_config = {
    "random_seed": RANDOM_SEED,
    "input_signals": SIGNAL_NAMES,
    "window_samples": 128,
    "sampling_frequency_hz": 50,
    "input_shape": [128, 6],
    "normalization": "per_channel_standardization",
    "normalization_statistics_source": "training_set_only",
    "channel_mean": channel_mean.tolist(),
    "channel_std": channel_std.tolist(),
    "train_subjects": train_subjects.tolist(),
    "validation_subjects": validation_subjects.tolist(),
    "test_subjects": np.unique(subjects_test).tolist(),
}

CONFIG_DIR.mkdir(parents=True, exist_ok=True)

with open(
    CONFIG_DIR / "baseline_preprocessing.json",
    "w"
) as f:
    json.dump(preprocessing_config, f, indent=2)


# ============================================================
# Final checks
# ============================================================

assert X_train.dtype == np.float32
assert X_validation.dtype == np.float32
assert X_test.dtype == np.float32

assert X_train.shape[1:] == (128, 6)
assert X_validation.shape[1:] == (128, 6)
assert X_test.shape[1:] == (128, 6)

print("\n" + "=" * 60)
print("PREPROCESSING COMPLETE")
print("=" * 60)

print(f"\nProcessed data saved to: {OUTPUT_DIR}")