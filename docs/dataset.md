# Dataset

## 1. Selected Dataset

**UCI Human Activity Recognition Using Smartphones Dataset (UCI-HAR)**

The dataset was selected as the initial development and evaluation dataset for the project.

The purpose of using a public dataset initially is to establish and validate the complete machine-learning pipeline before collecting and validating data using the physical LSM6DSOX sensor.

## 2. Dataset Characteristics

The UCI-HAR dataset contains inertial measurements collected from **30 subjects** performing daily activities.

The dataset contains six activity classes:

1. Walking
2. Walking Upstairs
3. Walking Downstairs
4. Sitting
5. Standing
6. Laying

The sensor configuration includes:

* 3-axis accelerometer
* 3-axis gyroscope

The original dataset sampling frequency is **50 Hz**.

## 3. Sensor Channels

The project will use six raw inertial channels:

```text
Accelerometer
Ax
Ay
Az

Gyroscope
Gx
Gy
Gz
```

Conceptually, each observation can therefore be represented as:

```text
[Ax, Ay, Az, Gx, Gy, Gz]
```

over time.

## 4. Raw Signals vs. Engineered Features

UCI-HAR provides both raw inertial signals and a large set of engineered features.

The project will use the **raw inertial signals** as the primary model input.

The dataset's precomputed 561-feature representation will not be used as the primary input.

### Reason

The objective is to develop the complete signal-to-inference pipeline ourselves:

```text
Raw Sensor Data
      ↓
Preprocessing
      ↓
Windowing
      ↓
ML Model
      ↓
Prediction
```

Using the precomputed feature vector would bypass important parts of this pipeline and would make the eventual embedded deployment less representative of the intended system.

## 5. Subject-Independent Evaluation

Subject identity is an important part of the dataset.

The project will use a subject-independent evaluation strategy so that subjects represented in the evaluation data are not simply treated as additional samples from the training population.

This is intended to provide a more meaningful test of generalization to previously unseen subjects.

The exact split strategy will be defined during dataset preparation.

## 6. Windowing

UCI-HAR's original dataset construction uses fixed-width windows.

However, the original window configuration will **not automatically be adopted as the final project configuration**.

The project will independently determine:

* Window duration
* Number of samples per window
* Stride
* Overlap

These parameters will be selected during the preprocessing stage based on:

* HAR recognition requirements
* Model input dimensions
* Computational cost
* Inference latency
* Real-time responsiveness

## 7. Sampling Rate

The UCI-HAR dataset uses a **50 Hz** sampling rate.

The physical LSM6DSOX-based system may eventually operate at a different sampling rate.

This creates an important experimental consideration:

> Dataset sampling frequency and hardware sampling frequency should not be treated as automatically interchangeable.

If resampling is required, the procedure must be explicitly documented and evaluated.

The project will therefore avoid simply treating resampled data as equivalent to data natively collected at the target hardware sampling frequency.

## 8. Dataset-to-Hardware Considerations

The UCI-HAR dataset was collected using a smartphone-based sensing setup, whereas the eventual embedded system will use an LSM6DSOX IMU connected directly to an STM32.

Therefore, the two systems may differ in:

* Sensor characteristics
* Sensor placement
* Coordinate orientation
* Sampling configuration
* Noise characteristics
* Scale and units
* User behavior
* Data-collection environment

These differences represent a potential source of **domain shift**.

For this reason, the project treats UCI-HAR primarily as the initial model-development and controlled-evaluation dataset.

Later hardware validation using the physical LSM6DSOX can be used to investigate how well the developed pipeline transfers to the target sensing platform.

## 9. Data Leakage Considerations

Care must be taken to prevent information from evaluation subjects from influencing training.

This is especially important for time-series data because adjacent windows can be highly correlated.

The preprocessing pipeline must therefore ensure that:

* Subject separation is maintained
* Training statistics are not computed using test data
* Normalization parameters are derived only from the appropriate training data
* Evaluation data does not influence model development

These issues will be addressed explicitly during preprocessing.

## 10. Dataset Limitations

The selected dataset is useful for developing the initial pipeline, but it does not perfectly reproduce the final embedded sensing environment.

Important limitations include:

* Smartphone-based data collection rather than the target IMU
* 50 Hz dataset sampling
* Potential differences in sensor placement and orientation
* Potential differences between smartphone and LSM6DSOX sensor characteristics
* Controlled activity collection rather than fully representative deployment conditions

These limitations will be considered when interpreting hardware-validation results.

## 11. Role in the Project

The dataset is the first stage of the experimental pipeline:

```text
UCI-HAR
   ↓
Preprocessing
   ↓
Baseline Model
   ↓
Compression
   ↓
Embedded Deployment
   ↓
Real-Time Evaluation
```

The dataset is therefore not the final objective of the project. It provides a controlled and reproducible foundation for studying TinyML model efficiency and real-time embedded behavior.

## 12. Dataset Decision Record

| Parameter                      | Current Decision          |
| ------------------------------ | ------------------------- |
| Dataset                        | UCI-HAR                   |
| Subjects                       | 30                        |
| Activity classes               | 6                         |
| Sensor modalities              | Accelerometer + Gyroscope |
| Input channels                 | 6                         |
| Dataset sampling rate          | 50 Hz                     |
| Raw signals                    | Yes                       |
| Precomputed 561 features       | No                        |
| Subject-independent evaluation | Yes                       |
| Window size                    | Not yet finalized         |
| Stride/overlap                 | Not yet finalized         |
| Normalization                  | Not yet finalized         |
| Train/validation/test split    | Not yet finalized         |
