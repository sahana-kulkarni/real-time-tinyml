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
