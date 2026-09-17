# Real-Time TinyML Inference on STM32

A research-oriented TinyML project investigating neural-network compression and real-time scheduling for machine-learning inference on resource-constrained embedded systems.

The project uses an STM32F446RE microcontroller and an IMU sensor to develop and deploy a Human Activity Recognition (HAR) model. The study will evaluate how model compression techniques and real-time task scheduling affect model accuracy, memory usage, inference latency, and timing predictability.

## Research Question

> **How do neural-network compression techniques and real-time task scheduling affect the accuracy, resource utilization, and timing predictability of TinyML inference on resource-constrained embedded systems?**

## Project Objectives

The project will investigate:

* Baseline neural-network inference on an embedded MCU
* Integer quantization and its effect on model accuracy and resource requirements
* Model pruning and its effect on model size and inference performance
* Integration of ML inference with real-time sensor-processing tasks
* Inference latency and timing variability
* Worst-case execution time (WCET)
* Deadline misses and scheduling behavior
* Memory and computational resource utilization

## System

### Hardware

* **Microcontroller:** STM32F446RE
* **Processor:** ARM Cortex-M4
* **Sensor:** Adafruit LSM6DSOX 6-DoF Accelerometer + Gyroscope
* **Sensor interface:** I²C
* **Sensor channels:**

  * Accelerometer X, Y, Z
  * Gyroscope X, Y, Z

### Software

* C/C++
* Python
* TensorFlow Lite for Microcontrollers / LiteRT
* FreeRTOS
* STM32 development tools

## Machine-Learning Task

The initial machine-learning task is **Human Activity Recognition (HAR)** using inertial sensor data.

The initial dataset is the **UCI Human Activity Recognition Using Smartphones Dataset (UCI-HAR)**.

The dataset contains:

* 30 subjects
* 6 activity classes
* 3-axis accelerometer data
* 3-axis gyroscope data
* 50 Hz sampling
* Subject identifiers
* Raw inertial sensor signals

The project will use the raw inertial signals rather than the dataset's precomputed engineered feature vector as the primary model input.

## Planned Experimental Progression

The project is organized as a sequence of increasingly realistic experiments:

```text
Dataset
   ↓
Preprocessing
   ↓
Baseline ML Model
   ↓
Embedded Deployment
   ↓
Quantization
   ↓
Pruning
   ↓
FreeRTOS Integration
   ↓
Real-Time Evaluation
```

### Experiment 1 — Baseline

Establish baseline measurements for:

* Classification accuracy
* Model size
* Memory usage
* Inference latency

### Experiment 2 — Quantization

Investigate the effect of integer quantization on:

* Accuracy
* Model size
* RAM usage
* Inference latency

### Experiment 3 — Pruning

Investigate whether reducing model parameters through pruning produces measurable benefits on the target embedded system.

### Experiment 4 — Real-Time Scheduling

Integrate inference with sensor-processing tasks under FreeRTOS and examine:

* Task execution time
* Inference latency
* Timing variability
* Scheduling behavior
* Deadline misses

### Experiment 5 — Real-Time Analysis

Characterize the deployed system using real-time metrics such as:

* Inference execution time
* WCET
* CPU utilization
* Memory utilization
* Deadline-miss rate
* Timing jitter

## Repository Structure

The repository is organized to separate project documentation, research notes, experiments, source code, firmware, and experimental results.

```text
real-time-tinyml/
│
├── README.md
│
├── docs/
│   ├── project-overview.md
│   ├── experimental-design.md
│   └── dataset.md
│
├── research/
│   ├── literature/
│   ├── notes/
│   └── references/
│
├── experiments/
│
├── src/
│
├── firmware/
│
├── notebooks/
│
├── results/
│
└── configs/
```

Directories will be introduced incrementally as the corresponding parts of the project are implemented.

## Current Status

### Completed

* [x] Defined project research direction
* [x] Defined research question
* [x] Selected STM32F446RE
* [x] Selected LSM6DSOX IMU
* [x] Defined initial HAR problem
* [x] Reviewed candidate public HAR datasets
* [x] Selected UCI-HAR as the initial development dataset
* [x] Decided to use raw accelerometer and gyroscope signals
* [x] Decided to use subject-independent evaluation

### In Progress

* [ ] Define preprocessing pipeline
* [ ] Determine window size and stride
* [ ] Define normalization strategy
* [ ] Define train/validation/test protocol
* [ ] Develop baseline model
* [ ] Establish baseline measurements

### Planned

* [ ] Quantization experiments
* [ ] Pruning experiments
* [ ] STM32 deployment
* [ ] FreeRTOS integration
* [ ] Real-time performance evaluation
* [ ] Hardware validation using the physical IMU
* [ ] Final experimental analysis
* [ ] Technical report

## Research Documentation

Detailed methodology and experimental decisions are documented under [`docs/`](docs/).

The project is developed incrementally so that experimental decisions, implementation changes, measurements, and conclusions remain traceable through the repository's version history.

## Reproducibility

Reproducibility is a core objective of the project.

Experimental configurations, preprocessing decisions, model configurations, evaluation procedures, and measured results will be documented as the project develops.

## Status

**Research prototype — methodology and implementation in progress.**
