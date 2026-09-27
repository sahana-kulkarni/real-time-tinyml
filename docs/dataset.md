## Dataset Inspection Results

The UCI-HAR dataset was inspected locally before model development to verify its structure, subject assignments, activity labels, and inertial signal dimensions.

### Verified Dataset Characteristics

| Property                           | Value |
| ---------------------------------- | ----: |
| Activities                         |     6 |
| Training windows                   | 7,352 |
| Test windows                       | 2,947 |
| Training subjects                  |    21 |
| Test subjects                      |     9 |
| Samples per window                 |   128 |
| Sampling frequency                 | 50 Hz |
| Subject overlap between train/test |  None |

The six activity classes are:

1. WALKING
2. WALKING_UPSTAIRS
3. WALKING_DOWNSTAIRS
4. SITTING
5. STANDING
6. LAYING

### Selected Input Signals

For the baseline neural-network input, six inertial signal channels will be used:

- `total_acc_x`
- `total_acc_y`
- `total_acc_z`
- `body_gyro_x`
- `body_gyro_y`
- `body_gyro_z`

Each sample therefore has the shape:

```text
(128, 6)
```

The complete model input tensor will have the form:

```text
(N, 128, 6)
```

where `N` is the number of windows in the corresponding dataset partition.

### Windowing

UCI-HAR already provides inertial signals segmented into 128-sample windows. Therefore, the baseline pipeline will use the dataset's provided windows rather than applying a second sliding-window operation.

At 50 Hz, each window represents:

```text
128 / 50 = 2.56 seconds
```

The provided windows use the dataset's established 50% overlap.

### Subject Separation

The original UCI-HAR test subjects were verified to be distinct from the training subjects.

The verified training subjects are:

```text
1, 3, 5, 6, 7, 8, 11, 14, 15, 16, 17,
19, 21, 22, 23, 25, 26, 27, 28, 29, 30
```

The verified test subjects are:

```text
2, 4, 9, 10, 12, 13, 18, 20, 24
```

There is no subject overlap between the two groups.

For subsequent baseline experiments, the 21 original training subjects will be divided into separate training and validation subject groups. The original nine test subjects will remain untouched as the final evaluation set.

### Reproducibility

Dataset inspection is performed by:

```text
src/data/inspect_uci_har.py
```

The raw dataset is kept locally under:

```text
data/raw/UCI HAR Dataset/
```

and is excluded from version control. The inspection script and derived research results are version-controlled.
