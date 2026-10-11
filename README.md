# Real-Time TinyML Inference on STM32

A research-oriented embedded machine learning project investigating how **neural-network compression and real-time task scheduling** affect the accuracy, resource requirements, and timing predictability of TinyML inference on resource-constrained microcontrollers.

The project uses a compact human activity recognition (HAR) model, the UCI Human Activity Recognition Using Smartphones Dataset (UCI-HAR), and an STM32F446RE development board as the target platform.

> **Current stage:** FP32 baseline trained and evaluated on held-out subjects. Model compression, STM32 deployment, and real-time measurements are planned next.

## Research Question

How do neural-network compression techniques and real-time task scheduling affect the accuracy, resource utilization, and timing predictability of TinyML inference on resource-constrained embedded systems?

## Research Objectives

The project investigates:

* Establishing a reproducible floating-point baseline for human activity recognition.
* Measuring the accuracy and model-size trade-offs of integer quantization.
* Investigating pruning and whether it produces practical benefits on the target microcontroller.
* Deploying inference on an STM32F446RE.
* Integrating inference with sensor-processing tasks using FreeRTOS.
* Evaluating inference latency, timing variability, worst-case execution time (WCET), memory use, and deadline misses.

## System Overview

### Target Hardware

| Component        | Specification                                       |
| ---------------- | --------------------------------------------------- |
| Microcontroller  | STM32F446RE                                         |
| Processor        | ARM Cortex-M4                                       |
| IMU sensor       | Adafruit LSM6DSOX 6-DoF accelerometer and gyroscope |
| Sensor interface | I²C                                                 |
| Motion channels  | 3-axis accelerometer and 3-axis gyroscope           |

The initial model-development experiments use UCI-HAR. The physical IMU will be used in later hardware-validation experiments.

### Software and Tools

* Python and TensorFlow/Keras for model development
* NumPy, scikit-learn, and Matplotlib for data processing and evaluation
* C/C++ and STM32 development tools for embedded deployment
* TensorFlow Lite for Microcontrollers (TFLM) / LiteRT for on-device inference
* FreeRTOS for real-time task integration

## Machine-Learning Task

The task is to classify six human activities from accelerometer and gyroscope signals:

1. Walking
2. Walking upstairs
3. Walking downstairs
4. Sitting
5. Standing
6. Laying

### Dataset and Preprocessing

The initial experiments use the [UCI Human Activity Recognition Using Smartphones Dataset](https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones).

Key characteristics:

* 30 subjects and six activity classes
* Inertial signals sampled at 50 Hz
* Windows of 128 samples, corresponding to 2.56 seconds
* Six selected channels: three total-acceleration axes and three body-gyroscope axes

The dataset provides preprocessed inertial signals in fixed-length windows; these are not untouched, continuous sensor recordings.

The model uses the six signal channels rather than the dataset's 561-dimensional engineered feature vector. The signals are arranged as tensors of shape `(128, 6)` and standardized using per-channel statistics calculated from the training partition only.

### Subject-Independent Evaluation

To reduce subject leakage, the original training subjects are divided into training and validation partitions, while the original test subjects remain held out.

| Partition  | Windows | Subjects |
| ---------- | ------: | -------: |
| Training   |   5,270 |       15 |
| Validation |   2,082 |        6 |
| Test       |   2,947 |        9 |

The subject partitions and preprocessing configuration are recorded in the repository. The held-out test set is used for final evaluation, not for fitting the model.

## Current Results: FP32 Baseline

The first model is a compact one-dimensional convolutional neural network (1D CNN) implemented in TensorFlow/Keras.

### Model Architecture

* Input shape: `(128, 6)`
* Two 1D convolutional layers with 16 and 32 filters
* Kernel size of 5
* Batch normalization and ReLU activations
* Max pooling after each convolutional block
* Global average pooling
* Dense layer with 32 units
* Six-class softmax output

### Evaluation Results

| Metric                   |        Result |
| ------------------------ | ------------: |
| Held-out test accuracy   |    **91.31%** |
| Test loss                |        0.2917 |
| Total parameters         |         4,534 |
| Trainable parameters     |         4,438 |
| Non-trainable parameters |            96 |
| Saved Keras model size   | 109,707 bytes |
| Training epochs          |            30 |
| Batch size               |            64 |
| Random seed              |            42 |

The saved `.keras` file size is the serialized desktop model size. It is **not** a measurement of embedded flash usage, peak RAM consumption, or deployed inference latency.

### Per-Class F1-Score

| Activity           | F1-score |
| ------------------ | -------: |
| Walking            |     0.95 |
| Walking upstairs   |     0.93 |
| Walking downstairs |     0.91 |
| Sitting            |     0.83 |
| Standing           |     0.86 |
| Laying             |     1.00 |

Sitting and standing are the weakest classes by F1-score in this baseline. The confusion matrix is available for closer examination of the classification errors.

### Baseline Artifacts

| Artifact            | Location                                |
| ------------------- | --------------------------------------- |
| Model definition    | `src/models/build_baseline_model.py`    |
| Training script     | `src/models/train_baseline.py`          |
| Evaluation script   | `src/models/evaluate_baseline.py`       |
| Model configuration | `configs/baseline_model.json`           |
| Training history    | `results/baseline/training_history.csv` |
| Test metrics        | `results/baseline/test_metrics.json`    |
| Confusion matrix    | `results/baseline/confusion_matrix.png` |
| Trained model       | `results/baseline/baseline_fp32.keras`  |

## Experimental Roadmap

| Stage | Experiment                                        | Status   |
| ----- | ------------------------------------------------- | -------- |
| 1     | Dataset verification and preprocessing            | Complete |
| 2     | FP32 baseline training and held-out evaluation    | Complete |
| 3     | Integer quantization and accuracy/size comparison | Next     |
| 4     | Model pruning and evaluation                      | Planned  |
| 5     | Embedded deployment on STM32F446RE                | Planned  |
| 6     | FreeRTOS integration                              | Planned  |
| 7     | Real-time performance and scheduling analysis     | Planned  |
| 8     | Physical-sensor validation and final analysis     | Planned  |

Future comparisons will use consistent data partitions and evaluation procedures wherever applicable.

The embedded experiments will investigate:

* Model storage in flash
* Peak inference RAM usage
* Inference latency and timing variability
* WCET estimation or measurement under a documented test setup
* CPU utilization and task scheduling behavior
* Deadline-miss rate under defined workloads

These hardware and real-time measurements have not yet been established by the current desktop baseline.

## Repository Structure

```text
real-time-tinyml/
├── configs/
│   ├── baseline_preprocessing.json
│   └── baseline_model.json
├── data/
│   ├── raw/                 # Local dataset; not tracked by Git
│   └── processed/           # Generated tensors; not tracked by Git
├── docs/
│   ├── project-overview.md
│   ├── experimental-design.md
│   └── dataset.md
├── results/
│   └── baseline/
│       ├── training_history.csv
│       ├── test_metrics.json
│       ├── confusion_matrix.png
│       └── baseline_fp32.keras
├── src/
│   ├── data/
│   │   └── preprocess_uci_har.py
│   └── models/
│       ├── build_baseline_model.py
│       ├── train_baseline.py
│       └── evaluate_baseline.py
├── .gitignore
├── README.md
├── requirements.txt
└── research-notes.md
```

Generated data files and the Python virtual environment are excluded from version control. Experiment configurations, evaluation metrics, figures, and documentation are tracked to support reproducibility.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sahana-kulkarni/real-time-tinyml.git
cd real-time-tinyml
```

### 2. Create and activate a Python environment

On macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Prepare the dataset

Download and extract the UCI-HAR dataset from the [official dataset page](https://archive.ics.uci.edu/dataset/240/human+activity+recognition+using+smartphones). Place the extracted dataset under the local data directory expected by `src/data/preprocess_uci_har.py`.

Follow [`docs/dataset.md`](docs/dataset.md) for the expected directory structure, preprocessing procedure, and partition details.

### 5. Run the baseline workflow

From the repository root, with the environment activated and processed data generated:

```bash
python src/models/build_baseline_model.py
python src/models/train_baseline.py
python src/models/evaluate_baseline.py
```

The training and evaluation scripts write their artifacts under `results/baseline/`. Running training again will retrain and overwrite the saved baseline artifacts.

## Documentation

* [Project overview](docs/project-overview.md) — research motivation, goals, and system scope.
* [Experimental design](docs/experimental-design.md) — experimental protocol, model details, and baseline results.
* [Dataset and preprocessing](docs/dataset.md) — data organization, subject partitions, and normalization.
* [Research notes](research-notes.md) — ongoing research notes and decisions.

## Reproducibility and Research Practice

The project aims to keep experimental decisions traceable through version-controlled configurations, scripts, documentation, and results. Comparisons will document the model configuration, preprocessing setup, evaluation partition, and relevant runtime conditions.

Reported performance is tied to the specific dataset split and experimental setup. Desktop accuracy alone does not demonstrate that a model meets embedded real-time constraints.

## Project Status

**Research prototype — baseline established; embedded optimization and real-time evaluation remain in progress.**
