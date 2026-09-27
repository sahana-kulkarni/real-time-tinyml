from pathlib import Path
import numpy as np

#Configuration

DATASET_ROOT = Path("data/raw/UCI HAR Dataset")

TRAIN_DIR = DATASET_ROOT / "train"
TEST_DIR = DATASET_ROOT / "test"

SIGNAL_DIR_TRAIN = TRAIN_DIR / "Inertial Signals"
SIGNAL_DIR_TEST = TEST_DIR / "Inertial Signals"

#Helper functions

def load_vector(path):
    """Load a one-column text file"""
    return np.loadtxt(path, dtype=int)

def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

#Dataset existence check

print_section("DATASET CHECK")

if not DATASET_ROOT.exists():
    raise FileNotFoundError(
        f"Dataset not found at: {DATASET_ROOT}"
    )

print(f"Dataset root: {DATASET_ROOT}")
print("Dataset exists: YES")

#Activity labels

print_section("ACTIVITY LABELS")

activity_labels = {}

with open(DATASET_ROOT / "activity_labels.txt", "r") as f:
    for line in f:
        activity_id, activity_name = line.strip().split()
        activity_labels[int(activity_id)] = activity_name
    
for activity_id, activity_name in activity_labels.items():
    print(f"{activity_id}: {activity_name}")

#Subject information

print_section("SUBJECT INFORMATION")

subject_train = load_vector(TRAIN_DIR / "subject_train.txt")
subject_test = load_vector(TEST_DIR / "subject_test.txt")

print(f"Training samples: {len(subject_train)}")
print(f"Test samples: {len(subject_test)}")

train_subjects = np.unique(subject_train)
test_subjects = np.unique(subject_test)

print(f"Training subjects: {train_subjects}")
print(f"Test subjects: {test_subjects}")

overlap = np.intersect1d(train_subjects, test_subjects)

print(f"Subject overlap: {overlap}")

if len(overlap) == 0:
    print("Subject separation check: PASS")
else:
    print("Subject separation check: FAIL")

#Activity distribution

print_section("ACTIVITY DISTRIBUTION")

y_train = load_vector(TRAIN_DIR / "y_train.txt")
y_test = load_vector(TEST_DIR / "y_test.txt")

print("Training distribution:")

for activity_id in sorted(np.unique(y_train)):
    count = np.sum(y_train == activity_id)
    name = activity_labels[activity_id]
    print(f" {activity_id} - {name:20s}: {count}")

print("\nTest distribution:")

for activity_id in sorted(np.unique(y_test)):
    count = np.sum(y_test == activity_id)
    name = activity_labels[activity_id]
    print(f" {activity_id} - {name:20s}: {count}")

#Inertial signal files

print_section("INERTIAL SIGNAAL FILES")

signal_files = sorted(SIGNAL_DIR_TRAIN.glob("*.txt"))

for path in signal_files:
    print(path.name)

#Signal dimensions

print_section("SIGNAL DIMENSIONS")

for path in signal_files:
    data = np.loadtxt(path)

    print(
        f"{path.name:30s}"
        f"shape={data.shape}"
        f"min={data.min():.4f}"
        f"max={data.max():.4f}"
    )

#Expected baseline signals

print_section("BASELINE SIGNAL CANDIDATES")

candidate_signals = [
    "total_acc_x_train.txt",
    "total_acc_y_train.txt",
    "total_acc_z_train.txt",
    "body_gyro_x_train.txt",
    "body_gyro_y_train.txt",
    "body_gyro_z_train.txt",
]

for filename in candidate_signals:
    path = SIGNAL_DIR_TRAIN / filename

    if path.exists():
        print(f"FOUND: {filename}")
    else:
        print(f"MISSING: {filename}")

#Final summary

print_section("SUMMARY")

print(f"Number of training windows: {len(subject_train)}")
print(f"Number of test windows: {len(subject_test)}")
print(f"Number of training subjects: {len(train_subjects)}")
print(f"Number of test subjects: {len(test_subjects)}")
print(f"Number of activities: {len(activity_labels)}")

print("\nDataset inspection complete.")

