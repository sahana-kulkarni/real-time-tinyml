# Project Overview

## 1. Project Title

**Real-Time TinyML Inference on STM32**

## 2. Motivation

Machine learning is increasingly being deployed on resource-constrained edge devices where computation must occur locally rather than being continuously transferred to a cloud server.

Microcontrollers provide attractive platforms for edge intelligence because of their low power consumption, low cost, and ability to operate without a continuous network connection. However, their limited computational resources create challenges for machine-learning deployment.

A model that performs well on a desktop or server may not be suitable for a microcontroller because of constraints on:

* Flash memory
* RAM
* CPU cycles
* Energy consumption
* Inference latency
* Timing predictability

This project investigates these constraints through an end-to-end TinyML system implemented on an STM32 microcontroller.

## 3. Research Direction

The project focuses on the interaction between two areas:

1. **Machine-learning model efficiency**
2. **Real-time embedded-system behavior**

Rather than evaluating model compression only through conventional ML metrics such as accuracy, the project will investigate how compression techniques affect actual embedded-system characteristics.

The study will therefore consider both:

### Machine-Learning Metrics

* Classification accuracy
* Confusion matrix
* Model parameters
* Model size

### Embedded-System Metrics

* Flash usage
* RAM usage
* Inference latency
* Timing variability
* CPU utilization

### Real-Time Metrics

* Worst-case execution time (WCET)
* Task execution time
* Deadline misses
* Scheduling behavior
* Timing jitter

## 4. System Concept

The planned system consists of an IMU sensor connected to an STM32F446RE microcontroller.

```text
        LSM6DSOX IMU
              │
              │ I²C
              ▼
       STM32F446RE
              │
       Sensor Acquisition
              │
              ▼
       Preprocessing
              │
              ▼
       TinyML Inference
              │
              ▼
      Activity Prediction
```

The eventual real-time system will extend this architecture:

```text
              LSM6DSOX
                  │
                  ▼
        ┌──────────────────┐
        │ Sensor Acquisition│
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │  Preprocessing   │
        └────────┬─────────┘
                 │
                 ▼
        ┌──────────────────┐
        │ TinyML Inference │
        └────────┬─────────┘
                 │
                 ▼
           Classification


              FreeRTOS
        ┌───────────────────┐
        │ Sensor Task       │
        │ Preprocessing Task│
        │ Inference Task    │
        │ Monitoring Task   │
        └───────────────────┘
```

The exact task architecture will be determined during the real-time implementation phase.

## 5. Hardware Platform

### Microcontroller

**STM32F446RE**

The STM32F446RE provides an ARM Cortex-M4-based embedded platform suitable for investigating machine-learning inference under realistic MCU resource constraints.

### Inertial Sensor

**Adafruit LSM6DSOX**

The LSM6DSOX provides:

* 3-axis accelerometer
* 3-axis gyroscope

The resulting six sensor channels are:

```text
Accelerometer:
Ax
Ay
Az

Gyroscope:
Gx
Gy
Gz
```

The sensor communicates with the STM32 through I²C.

## 6. Machine-Learning Application

The initial application is **Human Activity Recognition (HAR)**.

The model receives a fixed-length sequence of inertial measurements and predicts an activity class.

Conceptually:

```text
Sensor Window
      │
      ▼
┌─────────────────┐
│ Ax Ay Az        │
│ Gx Gy Gz        │
│ ...             │
│ ...             │
└────────┬────────┘
         │
         ▼
   ML Model
         │
         ▼
Activity Class
```

## 7. Experimental Progression

The project will progress through several controlled stages.

### Stage 1 — Baseline

Develop and evaluate a baseline model without compression.

### Stage 2 — Quantization

Apply quantization and measure its effect on model accuracy and embedded resource requirements.

### Stage 3 — Pruning

Investigate parameter reduction through pruning and determine whether the reduction translates into practical embedded-system benefits.

### Stage 4 — Real-Time Integration

Integrate inference with sensor acquisition and other tasks under FreeRTOS.

### Stage 5 — Real-Time Characterization

Measure execution-time behavior and determine whether the system satisfies its intended timing requirements.

## 8. Research Philosophy

The project is designed as an experimental investigation rather than simply a demonstration of TinyML deployment.

Each major modification should therefore follow the pattern:

```text
Baseline
   ↓
Controlled Change
   ↓
Measurement
   ↓
Comparison
   ↓
Interpretation
```

For example:

```text
FP32 Model
   ↓
INT8 Quantization
   ↓
Measure accuracy / RAM / Flash / latency
   ↓
Compare with baseline
   ↓
Interpret trade-off
```

This approach allows the project to produce quantitative evidence rather than relying only on whether the model successfully runs on the microcontroller.

## 9. Current Scope

The current scope is intentionally limited to:

* One MCU platform
* One IMU
* One initial HAR dataset
* One primary ML task
* Model compression
* Embedded deployment
* Real-time scheduling

Additional datasets or hardware platforms may be considered later for validation, but they are not currently part of the core experimental design.

## 10. Current Development Phase

The project is currently in the **experimental-design and preprocessing-definition phase**.

Completed decisions are documented in:

* `docs/experimental-design.md`
* `docs/dataset.md`

The next methodological step is to define the complete preprocessing pipeline before model development begins.
