# Experimental Design

## 1. Research Question

> **How do neural-network compression techniques and real-time task scheduling affect the accuracy, resource utilization, and timing predictability of TinyML inference on resource-constrained embedded systems?**

## 2. Experimental Objective

The objective is to build an end-to-end TinyML system and systematically measure the effects of model compression and real-time scheduling.

The experiment will connect machine-learning metrics with embedded-system metrics rather than evaluating model performance only in terms of classification accuracy.

## 3. Experimental Variables

The primary experimental factors are:

### Model Configuration

* Baseline model
* Quantized model
* Pruned model
* Quantized + pruned model, if technically appropriate

### Runtime Configuration

* Standalone inference
* Inference integrated with sensor-processing tasks
* FreeRTOS scheduling configuration

### Hardware Platform

* STM32F446RE
* LSM6DSOX IMU

## 4. Dependent Measurements

The following measurements will be collected where applicable.

### ML Performance

* Classification accuracy
* Per-class performance
* Confusion matrix

### Model Characteristics

* Number of parameters
* Model size
* Model representation
* Tensor memory requirements

### Embedded Resources

* Flash usage
* Static RAM usage
* Runtime memory usage
* CPU utilization

### Timing

* Average inference latency
* Minimum inference latency
* Maximum observed inference latency
* Timing variability
* WCET estimation/measurement
* Deadline misses
* Scheduling-related delays

The exact measurement methodology will be defined before each experiment.

## 5. Hardware

| Component              | Selection         |
| ---------------------- | ----------------- |
| MCU                    | STM32F446RE       |
| Processor              | ARM Cortex-M4     |
| IMU                    | Adafruit LSM6DSOX |
| Accelerometer channels | X, Y, Z           |
| Gyroscope channels     | X, Y, Z           |
| Sensor interface       | I²C               |

## 6. Machine-Learning Task

The initial ML task is Human Activity Recognition (HAR).

The model will receive six-channel inertial sensor data:

```text
[Ax, Ay, Az, Gx, Gy, Gz]
```

over a fixed temporal window and predict one of six activity classes from the selected dataset.

## 7. Dataset

The initial development dataset is UCI-HAR.

The selected dataset provides:

* 30 subjects
* 6 activities
* Accelerometer measurements
* Gyroscope measurements
* 50 Hz sampling
* Subject identifiers
* Raw inertial signals

The dataset is described in detail in [`dataset.md`](dataset.md).

## 8. Evaluation Principle

The project will use subject-independent evaluation.

The purpose is to prevent the model from being evaluated primarily on data from subjects it has already seen during training.

The exact train/validation/test protocol will be finalized during preprocessing and dataset preparation.

## 9. Baseline

A baseline model will be established before compression techniques are applied.

The baseline should provide measurements for:

```text
Accuracy
   +
Model Size
   +
RAM
   +
Flash
   +
Inference Latency
```

These measurements will serve as the reference point for subsequent experiments.

## 10. Quantization Experiment

Quantization will be evaluated as a controlled modification of the baseline model.

The experiment will investigate:

```text
Baseline
    │
    ▼
Quantized Model
    │
    ├── Accuracy
    ├── Model Size
    ├── RAM
    └── Inference Latency
```

The goal is to characterize the trade-off between numerical representation and embedded-system resource requirements.

## 11. Pruning Experiment

Pruning will be investigated as a separate model-compression technique.

The experiment will examine:

* Parameter reduction
* Model representation
* Accuracy impact
* Memory impact
* Inference latency

An important experimental question is whether reducing the number of parameters necessarily produces a corresponding reduction in actual MCU execution time or memory usage.

## 12. Real-Time Experiment

After establishing the ML deployment baseline, inference will be integrated into a FreeRTOS-based application.

The system may contain tasks such as:

```text
Sensor Acquisition Task
Preprocessing Task
Inference Task
Monitoring/Logging Task
```

The final task architecture and priorities will be determined during implementation.

The experiment will investigate whether ML inference interacts with other real-time tasks in ways that affect timing predictability.

## 13. Timing Analysis

Timing analysis will consider:

### Execution Time

How long does an inference take?

### Variability

How much does inference time vary between executions?

### WCET

What is the largest observed or otherwise justified execution-time bound under the defined experimental conditions?

### Deadline Misses

Does inference or another task fail to complete within its assigned deadline?

### Scheduling Behavior

How does task scheduling affect inference execution and sensor-processing responsiveness?

## 14. Experimental Control

Where possible, experiments should change one major factor at a time.

For example:

```text
Baseline
   │
   ├── Quantization
   │
   ├── Pruning
   │
   └── Scheduling
```

Measurements should be collected using the same:

* Dataset split
* Preprocessing procedure
* Evaluation procedure
* Hardware platform
* Timing measurement methodology

unless the experiment explicitly studies one of those factors.

## 15. Reproducibility

Each experiment should document:

* Dataset version/source
* Dataset split
* Preprocessing parameters
* Model architecture
* Training configuration
* Compression configuration
* Compiler/toolchain configuration where relevant
* Hardware configuration
* RTOS configuration
* Measurement procedure
* Raw measurements
* Derived metrics

Experimental configurations should be separated from source code where practical.

## 16. Current Decisions vs. Open Decisions

### Decided

* STM32F446RE
* LSM6DSOX
* Human Activity Recognition
* Six sensor channels
* UCI-HAR as the initial development dataset
* Raw inertial signals
* Subject-independent evaluation
* Baseline → quantization → pruning → real-time scheduling progression

### Not Yet Decided

* Window duration
* Window stride/overlap
* Normalization method
* Filtering
* Resampling strategy
* Exact train/validation/test split
* Baseline model architecture
* Quantization configuration
* Pruning configuration
* FreeRTOS task periods and priorities
* Real-time deadlines
* Exact timing instrumentation

These decisions will be documented before implementation of the corresponding stage.

## Milestone 4 — FP32 Baseline Model

### Objective

Establish a reproducible floating-point baseline for six-class human activity recognition before evaluating model compression and embedded deployment.

### Model architecture

A compact 1D convolutional neural network (CNN) was implemented in TensorFlow/Keras.

* Input shape: `(128, 6)`
* Convolutional layers: 16 filters and 32 filters, both using kernel size 5
* Batch normalization and ReLU activations
* Max pooling after each convolutional block
* Global average pooling
* Dense layer with 32 units
* Six-class softmax output

The model contains 4,534 parameters: 4,438 trainable and 96 non-trainable.

### Data and training protocol

* Dataset: UCI Human Activity Recognition (UCI-HAR)
* Input: six selected inertial channels, standardized using statistics calculated from training data only
* Training set: 5,270 windows from 15 subjects
* Validation set: 2,082 windows from 6 subjects
* Test set: 2,947 windows from 9 held-out subjects
* Random seed: 42
* Optimizer: Adam
* Loss: sparse categorical cross-entropy
* Batch size: 64
* Training epochs: 30

Activity labels were converted from the dataset's 1–6 encoding to zero-based class indices when supplied to the model. The saved dataset labels remain unchanged.

The epoch-30 model was evaluated on the held-out test set. This checkpoint had the lowest validation loss among the 30 recorded epochs. The test set was not used for model selection.

### Baseline results

| Metric                      |        Result |
| --------------------------- | ------------: |
| Test accuracy               |        91.31% |
| Test loss                   |        0.2917 |
| Parameter count             |         4,534 |
| Serialized Keras model size | 109,707 bytes |

Per-class F1-scores:

| Activity           | F1-score |
| ------------------ | -------: |
| Walking            |     0.95 |
| Walking upstairs   |     0.93 |
| Walking downstairs |     0.91 |
| Sitting            |     0.83 |
| Standing           |     0.86 |
| Laying             |     1.00 |

Sitting and standing had the lowest F1-scores, suggesting that distinguishing these relatively stationary activities is a useful area for further investigation. The confusion matrix should be examined to identify the specific misclassification patterns.

### Artifacts

* Model definition: `src/models/build_baseline_model.py`
* Training script: `src/models/train_baseline.py`
* Evaluation script: `src/models/evaluate_baseline.py`
* Model configuration: `configs/baseline_model.json`
* Training history: `results/baseline/training_history.csv`
* Test metrics: `results/baseline/test_metrics.json`
* Confusion matrix: `results/baseline/confusion_matrix.png`
* Trained checkpoint: `results/baseline/baseline_fp32.keras`

### Interpretation and limitations

This result establishes the initial accuracy and model-size reference for subsequent quantization experiments. The serialized Keras file size is not a measurement of embedded flash or RAM requirements. Inference latency, peak memory use, and real-time behavior have not yet been measured on the STM32 hardware.

Results from later experiments should use the same subject partitions and test protocol to maintain comparability.


## Milestone 5.2 — FP32 TensorFlow Lite Conversion

### Objective

Convert the trained FP32 Keras baseline to TensorFlow Lite and verify that conversion preserves its predictions.

### Results

| Metric                                 |        Result |
| -------------------------------------- | ------------: |
| Keras model file size                  | 109,707 bytes |
| FP32 TensorFlow Lite file size         |  23,772 bytes |
| Serialized file-size reduction         |        78.33% |
| Samples compared                       |           100 |
| Maximum absolute prediction difference |    0.00000024 |
| Mean absolute prediction difference    |    0.00000001 |
| Predicted-class agreement              |          100% |

Both model inputs and outputs use float32. Prediction comparisons were performed on the first 100 examples of the held-out test partition.

### Interpretation

The TensorFlow Lite model closely reproduced the Keras model's predictions for the sampled inputs. The serialized TensorFlow Lite file was approximately 4.6 times smaller than the Keras file.

This reduction is attributable to the difference between model serialization formats and must not be interpreted as an INT8 quantization gain. The measurements do not establish embedded flash usage, peak RAM consumption, or inference latency on the STM32F446RE.

### Artifacts

* Conversion script: `src/models/export_tflite_baseline.py`
* Converted model: `results/quantization/baseline_fp32.tflite`
* Conversion report: `results/quantization/baseline_fp32_conversion.json`

This converted FP32 model will serve as the TensorFlow Lite reference for subsequent quantization experiments.

