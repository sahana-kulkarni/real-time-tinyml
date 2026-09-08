
# Research Notes — Real-Time TinyML on STM32

> **Project:** Real-Time TinyML + Embedded Systems + Real-Time Scheduling
> **Research Repository:** `real-time-tinyml`
> **Status:** Initial setup
> **Started:** September 2026
> **Target completion:** October 30, 2026
>
> This document is a living research notebook.
> Record decisions, experiments, measurements, failures, observations, and conclusions as the project develops.

---

# 1. Research Direction

## Primary Research Area

**Edge AI / TinyML + Embedded Systems + Real-Time Systems**

## Secondary Research Area

**Hardware Security**

Hardware security will be explored as a separate research artifact rather than being mixed into the primary TinyML project.

## Project Focus

This project investigates the deployment of a machine-learning model on a resource-constrained STM32 microcontroller and studies how model-compression techniques and real-time scheduling affect:

* inference accuracy
* inference latency
* memory usage
* worst-case execution time (WCET)
* deadline-miss behavior
* overall suitability for real-time embedded inference

---

# 2. Research Question

## Primary Research Question

> **How do model-compression techniques and real-time scheduling strategies affect the accuracy, latency, memory footprint, and timing guarantees of TinyML inference on a resource-constrained STM32 microcontroller?**

## Supporting Questions

1. How does the baseline model perform when deployed directly on the STM32?
2. What accuracy/latency trade-offs result from quantization?
3. What accuracy/latency/memory trade-offs result from pruning?
4. How does model compression affect memory requirements?
5. How does inference execution behave under FreeRTOS?
6. What is the measured worst-case execution time of inference?
7. How does scheduling affect deadline-miss behavior?
8. Is a smaller/faster model necessarily better for a real-time embedded system?
9. What trade-offs emerge between model accuracy and timing predictability?

---

# 3. Motivation

Edge AI systems increasingly need to perform inference locally on devices with limited:

* computational resources
* memory
* energy
* storage
* real-time execution capability

Running inference directly on a microcontroller introduces a different set of constraints from running a model on a desktop, server, or GPU.

For this project, the goal is not simply to make a model run on an STM32.

The goal is to **measure and understand the system-level trade-offs** involved in deploying and scheduling TinyML inference under embedded and real-time constraints.

The project should therefore be treated as an experimental study rather than only an implementation exercise.

---

# 4. Expected Research Contribution

At the end of the project, the intended contribution is a reproducible experimental study showing how different model and scheduling configurations affect embedded real-time inference.

The project should produce:

* a working STM32 TinyML implementation
* baseline measurements
* quantized-model measurements
* pruned-model measurements
* FreeRTOS scheduling experiments
* WCET measurements
* deadline-miss measurements
* comparison tables/plots
* observations about accuracy vs. resource usage vs. timing
* a technical report
* reproducible code and experiment documentation

The objective is to produce evidence and analysis rather than simply claim that one configuration is "better."

---

# 5. Literature Notes

This section will contain notes from papers and other technical references.

## Paper 1

### Citation

David et al., **"TensorFlow Lite Micro: Embedded Machine Learning on TinyML Systems,"** MLSys 2021.

### Why I am reading this

* Understand the TinyML deployment stack.
* Understand constraints involved in microcontroller inference.
* Understand how ML models can be executed on embedded devices.

### Key Concepts

* [ ] Microcontroller ML
* [ ] TensorFlow Lite Micro
* [ ] Memory-constrained inference
* [ ] Embedded deployment

### Important Findings

*To be completed while reading.*

### Relevance to My Project

*To be completed.*

### Questions Raised

*To be completed.*

---

## Paper 2

### Citation

Lai et al., **"CMSIS-NN: Efficient Neural Network Kernels for Arm Cortex-M CPUs."**

### Why I am reading this

* Understand efficient neural-network execution on Arm Cortex-M processors.
* Understand the role of optimized embedded kernels.
* Understand how low-level implementation affects inference performance.

### Key Concepts

* [ ] Cortex-M optimization
* [ ] CMSIS-NN
* [ ] Neural-network kernels
* [ ] Embedded inference performance

### Important Findings

*To be completed.*

### Relevance to My Project

*To be completed.*

### Questions Raised

*To be completed.*

---

## Additional Papers

### Quantization

Gholami et al., **"A Survey of Quantization Methods for Efficient Neural Network Inference."**

Notes:

*To be completed.*

---

### Deep Compression

Han, Mao, and Dally, **"Deep Compression."**

Notes:

*To be completed.*

---

### Pruning

Han, Pool, Tran, and Dally, **"Learning both Weights and Connections for Efficient Neural Networks."**

Notes:

*To be completed.*

---

### Real-Time Scheduling

Ali and Yun, **"RT-Gang: Real-Time Gang Scheduling Framework for Safety-Critical Systems."**

Notes:

*To be completed.*

---

### Timing Guarantees

**"Timing guarantees for inference of AI models in embedded systems."**

Notes:

*To be completed.*

---

# 6. System Architecture

## High-Level System

```text
                    ┌─────────────────────┐
                    │   Sensor / Input    │
                    │       Data          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Preprocessing     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   ML Inference      │
                    │     on STM32        │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
       ┌─────────────────┐          ┌─────────────────┐
       │ Classification /│          │ Timing / System │
       │    Prediction   │          │   Measurement   │
       └─────────────────┘          └─────────────────┘
```

## Target Hardware

**Microcontroller:** STM32F446RE

### Hardware Status

* [x] STM32F446RE board available
* [ ] IMU selected
* [ ] IMU purchased
* [ ] IMU integrated
* [ ] Sensor communication verified
* [ ] Sensor data pipeline verified

### Hardware Notes

*To be completed.*

---

# 7. Software Architecture

## Planned Components

* STM32 firmware
* TinyML inference runtime
* ML model
* preprocessing pipeline
* FreeRTOS
* task scheduling
* timing measurement
* memory measurement
* experiment logging

## Planned Task Structure

Initial conceptual structure:

```text
FreeRTOS
│
├── Sensor Task
│
├── Preprocessing Task
│
├── Inference Task
│
├── Measurement / Monitoring Task
│
└── Communication / Logging Task
```

This structure is preliminary and may change after implementation.

### Architecture Decisions

*Record the reason for every major architecture change.*

---

# 8. Baseline Model

## Model

The initial model will be selected after reviewing the existing model/code and understanding the data pipeline.

The existing implementation may be used as a **reference**, but the project implementation should be rebuilt sufficiently to understand the complete pipeline and make debugging and experimentation easier.

## Model Selection Criteria

The model should:

* be small enough for MCU deployment
* provide meaningful inference results
* allow quantization experiments
* allow pruning experiments
* have measurable latency
* fit within available STM32 memory/resources

## Dataset

*To be determined.*

### Dataset Characteristics

* Number of classes:
* Number of samples:
* Input dimensions:
* Sampling rate:
* Training/validation/test split:

## Baseline Hypothesis

> The baseline model should provide the reference point against which all compressed and scheduled configurations can be compared.

## Baseline Metrics

| Metric                    | Baseline |
| ------------------------- | -------: |
| Accuracy                  |      TBD |
| Model size                |      TBD |
| Flash usage               |      TBD |
| RAM usage                 |      TBD |
| Average inference latency |      TBD |
| Maximum inference latency |      TBD |
| WCET                      |      TBD |
| Deadline                  |      TBD |
| Deadline misses           |      TBD |

---

# 9. Experimental Design

The experiment should change **one major factor at a time** whenever practical so that observed effects can be attributed to the relevant technique.

## Experimental Dimensions

### Model Configuration

1. Baseline
2. Quantized
3. Pruned
4. Quantized + pruned, if feasible

### Scheduling Configuration

1. Baseline/non-RT execution
2. FreeRTOS execution
3. Different task priorities
4. Different scheduling configurations, where appropriate

### Metrics

For every configuration, collect:

* accuracy
* inference latency
* memory usage
* model size
* WCET
* deadline-miss rate

---

# 10. Experiment Matrix

The following matrix will be expanded as experiments are performed.

| Experiment | Model      | Quantization | Pruning | FreeRTOS | Priority/Scheduling | Accuracy | Avg Latency | WCET | RAM | Flash | Deadline Misses |
| ---------- | ---------- | ------------ | ------- | -------- | ------------------- | -------: | ----------: | ---: | --: | ----: | --------------: |
| E0         | Baseline   | No           | No      | No       | N/A                 |      TBD |         TBD |  TBD | TBD |   TBD |             TBD |
| E1         | Baseline   | Yes          | No      | No       | N/A                 |      TBD |         TBD |  TBD | TBD |   TBD |             TBD |
| E2         | Baseline   | No           | Yes     | No       | N/A                 |      TBD |         TBD |  TBD | TBD |   TBD |             TBD |
| E3         | Compressed | Yes          | Yes     | No       | N/A                 |      TBD |         TBD |  TBD | TBD |   TBD |             TBD |
| E4         | Baseline   | No           | No      | Yes      | TBD                 |      TBD |         TBD |  TBD | TBD |   TBD |             TBD |
| E5         | Compressed | Yes          | Yes     | Yes      | TBD                 |      TBD |         TBD |  TBD | TBD |   TBD |             TBD |

Additional experiments will be added as needed.

---

# 11. Experiment Log

Use this section as the primary day-to-day research log.

## Experiment Template

### Experiment ID

`EX-XXX`

### Date

YYYY-MM-DD

### Objective

What am I trying to determine?

### Hypothesis

What do I expect to happen?

### Configuration

* Model:
* Quantization:
* Pruning:
* FreeRTOS:
* Task configuration:
* Compiler/toolchain:
* Hardware:
* Dataset/input:

### Procedure

1.
2.
3.

### Measurements

| Metric          | Result |
| --------------- | -----: |
| Accuracy        |        |
| Average latency |        |
| Maximum latency |        |
| WCET            |        |
| RAM usage       |        |
| Flash usage     |        |
| Deadline misses |        |

### Result

What happened?

### Interpretation

What does the result mean?

### Unexpected Behavior

Did anything unexpected happen?

### Next Action

What experiment should happen next?

---

# 12. Quantization Experiments

## Objective

Investigate how quantization affects:

* model size
* memory usage
* inference latency
* accuracy
* timing behavior

## Questions

1. How much does quantization reduce model size?
2. How much does it reduce memory usage?
3. Does inference become faster?
4. How much accuracy is lost?
5. Does quantization affect WCET?
6. Does quantization improve deadline compliance?

## Quantization Configuration

*To be completed.*

### Experiment Results

| Configuration | Accuracy | Model Size | RAM | Avg Latency | WCET | Deadline Misses |
| ------------- | -------: | ---------: | --: | ----------: | ---: | --------------: |
| Baseline      |          |            |     |             |      |                 |
| Quantized     |          |            |     |             |      |                 |

## Observations

*To be completed.*

---

# 13. Pruning Experiments

## Objective

Investigate how pruning affects:

* model size
* memory usage
* inference latency
* accuracy
* timing behavior

## Questions

1. What pruning level can be tolerated before accuracy degrades significantly?
2. Does pruning actually reduce MCU inference latency?
3. Does pruning reduce memory usage?
4. Does pruning affect WCET?
5. Does pruning improve deadline compliance?

## Pruning Configuration

*To be completed.*

### Experiment Results

| Pruning Level | Accuracy | Model Size | RAM | Avg Latency | WCET | Deadline Misses |
| ------------: | -------: | ---------: | --: | ----------: | ---: | --------------: |
|            0% |          |            |     |             |      |                 |
|           TBD |          |            |     |             |      |                 |
|           TBD |          |            |     |             |      |                 |
|           TBD |          |            |     |             |      |                 |

## Observations

*To be completed.*

---

# 14. FreeRTOS / Scheduling Experiments

## Objective

Study the behavior of ML inference when integrated into a real-time operating-system environment.

## Questions

1. What task structure is appropriate for the application?
2. What priority should inference receive?
3. How does task priority affect inference timing?
4. How does sensor processing interact with inference?
5. What is the WCET of inference?
6. Under what conditions do deadline misses occur?
7. Does model compression improve schedulability?

## Initial Task Model

| Task          | Function               | Period | Deadline | Priority |
| ------------- | ---------------------- | -----: | -------: | -------: |
| Sensor        | Acquire sensor data    |    TBD |      TBD |      TBD |
| Preprocessing | Prepare model input    |    TBD |      TBD |      TBD |
| Inference     | Run ML model           |    TBD |      TBD |      TBD |
| Monitoring    | Collect system metrics |    TBD |      TBD |      TBD |
| Communication | Log/transmit results   |    TBD |      TBD |      TBD |

These values should be determined experimentally and justified rather than chosen arbitrarily.

---

# 15. WCET Measurement

## Objective

Estimate the worst-case execution time of the inference task under the defined experimental conditions.

## Measurement Method

*To be determined.*

## Measurement Assumptions

Document:

* processor frequency
* compiler configuration
* optimization settings
* input conditions
* cache/memory conditions, if relevant
* interrupt behavior
* RTOS configuration
* measurement instrumentation

## Results

| Configuration      | Number of Runs | Average | Maximum | WCET Estimate |
| ------------------ | -------------: | ------: | ------: | ------------: |
| Baseline           |                |         |         |               |
| Quantized          |                |         |         |               |
| Pruned             |                |         |         |               |
| Quantized + Pruned |                |         |         |               |

## Important Note

A single maximum observed execution time should not automatically be treated as a mathematically proven WCET.

Document clearly whether the result represents:

* maximum observed execution time
* estimated WCET
* experimentally bounded WCET
* or a formal WCET guarantee

---

# 16. Deadline-Miss Experiments

## Deadline Definition

Inference deadline:

**TBD**

The deadline must be justified based on the application/task requirements.

## Measurement

For each inference execution:

```text
Execution Time <= Deadline  → Deadline Met
Execution Time >  Deadline  → Deadline Miss
```

## Results

| Configuration     | Total Jobs | Deadline Met | Deadline Missed | Miss Rate |
| ----------------- | ---------: | -----------: | --------------: | --------: |
| Baseline          |            |              |                 |           |
| Quantized         |            |              |                 |           |
| Pruned            |            |              |                 |           |
| Compressed + RTOS |            |              |                 |           |

## Observations

*To be completed.*

---

# 17. Memory Analysis

## Flash Usage

| Configuration | Model Size | Firmware Size | Total Flash Used | Remaining |
| ------------- | ---------: | ------------: | ---------------: | --------: |
| Baseline      |            |               |                  |           |
| Quantized     |            |               |                  |           |
| Pruned        |            |               |                  |           |

## RAM Usage

| Configuration | Static RAM | Heap | Stack | Total RAM | Remaining |
| ------------- | ---------: | ---: | ----: | --------: | --------: |
| Baseline      |            |      |       |           |           |
| Quantized     |            |      |       |           |           |
| Pruned        |            |      |       |           |           |

## Observations

*To be completed.*

---

# 18. Results

This section should contain the final consolidated results rather than individual experiment notes.

## Accuracy

*To be completed.*

## Latency

*To be completed.*

## Memory

*To be completed.*

## WCET

*To be completed.*

## Deadline Behavior

*To be completed.*

## Overall Comparison

| Configuration      | Accuracy | Latency | Memory | WCET | Deadline Miss Rate |
| ------------------ | -------: | ------: | -----: | ---: | -----------------: |
| Baseline           |          |         |        |      |                    |
| Quantized          |          |         |        |      |                    |
| Pruned             |          |         |        |      |                    |
| Quantized + Pruned |          |         |        |      |                    |

---

# 19. Observations and Failures

Research notes should include failed experiments and unexpected behavior.

## Failure / Observation Template

### Date

YYYY-MM-DD

### What I Expected

...

### What Actually Happened

...

### Possible Cause

...

### What I Changed

...

### Result After Change

...

### Lesson Learned

...

### Does This Affect the Research Question?

Yes / No

### Follow-Up Experiment

...

---

# 20. Research Decisions

Keep a chronological record of important decisions.

| Date | Decision | Reason | Alternatives Considered |
| ---- | -------- | ------ | ----------------------- |
|      |          |        |                         |

Examples of decisions to document:

* model selection
* dataset selection
* sensor selection
* quantization method
* pruning strategy
* FreeRTOS task architecture
* priority assignment
* timing measurement method
* evaluation metrics
* experiment exclusions

---

# 21. Unexpected Findings

This section is intentionally separate from planned results.

Record findings such as:

* a compressed model being slower than expected
* pruning reducing model size without reducing latency
* FreeRTOS introducing unexpected timing variation
* accuracy changing more than expected
* memory becoming the primary bottleneck
* scheduling causing deadline misses
* a supposedly optimized configuration performing worse

Unexpected results may become important research observations.

---

# 22. Research Conclusions

Do not write this section prematurely.

At the end of the project, summarize:

## Finding 1

...

## Finding 2

...

## Finding 3

...

## Main Conclusion

...

## Answer to Research Question

> ...

---

# 23. Limitations

Document limitations honestly.

Potential categories:

* limited hardware resources
* limited number of models
* limited datasets
* limited experiment duration
* measurement uncertainty
* limited scheduling scenarios
* lack of formal WCET proof
* limited generalizability beyond the selected STM32 platform

Actual limitations should be added as they become known.

---

# 24. Future Work

Possible future directions should only be added when supported by the results.

Potential directions:

* additional model architectures
* additional MCU platforms
* energy measurements
* additional scheduling policies
* more sophisticated pruning
* mixed-precision quantization
* hardware acceleration
* formal timing analysis
* security implications of edge inference

---

# 25. Reproducibility Checklist

Before considering the project complete:

### Hardware

* [ ] STM32 board identified
* [ ] Sensor/IMU documented
* [ ] Hardware connections documented
* [ ] Processor configuration documented

### Software

* [ ] Toolchain documented
* [ ] Firmware version documented
* [ ] TensorFlow Lite Micro/runtime version documented
* [ ] CMSIS-NN/runtime dependencies documented
* [ ] FreeRTOS version/configuration documented

### Model

* [ ] Model architecture documented
* [ ] Dataset documented
* [ ] Training procedure documented
* [ ] Baseline model saved
* [ ] Quantized model saved
* [ ] Pruned model saved

### Experiments

* [ ] Experimental configurations documented
* [ ] Timing methodology documented
* [ ] Memory measurement methodology documented
* [ ] WCET methodology documented
* [ ] Deadline definition documented
* [ ] Raw results preserved

### Research Artifacts

* [ ] GitHub repository updated
* [ ] README completed
* [ ] Experiment results included
* [ ] Technical report completed
* [ ] Research notes completed
* [ ] Final conclusions written

---

# 26. Research Timeline

## Phase 1 — Foundation

**September 2026**

* [x] Research direction finalized
* [x] Flagship project design confirmed
* [x] Research GitHub repository created
* [ ] Hardware finalized
* [ ] IMU selected/purchased
* [ ] Research notes established
* [ ] Initial papers reviewed
* [ ] Professor list started
* [ ] Resume base rewrite started

## Phase 2 — Implementation

**September–October 2026**

* [ ] Sensor pipeline implemented
* [ ] Baseline model selected
* [ ] Baseline model deployed
* [ ] Baseline measurements collected
* [ ] Quantization implemented
* [ ] Quantization experiments completed
* [ ] Pruning implemented
* [ ] Pruning experiments completed
* [ ] FreeRTOS integration completed
* [ ] Scheduling experiments completed
* [ ] WCET measurements completed
* [ ] Deadline experiments completed

## Phase 3 — Analysis

**October 2026**

* [ ] Results consolidated
* [ ] Results visualized
* [ ] Trade-offs analyzed
* [ ] Research conclusions written
* [ ] Technical report drafted
* [ ] GitHub repository cleaned/documented

## Target

**October 30, 2026**

Working, benchmarked project + GitHub documentation + technical report.

---

# 27. Questions to Investigate

Keep an evolving list of research questions here.

### Current Questions

1. What is the smallest model that still provides acceptable accuracy?
2. How much does quantization reduce inference cost?
3. Does pruning actually improve MCU inference latency?
4. How does model compression affect WCET?
5. How does FreeRTOS scheduling affect inference timing?
6. What task priority configuration provides reliable inference execution?
7. What causes deadline misses?
8. Can compression improve schedulability without unacceptable accuracy loss?
9. Which metric becomes the dominant constraint on the STM32?
10. What conclusions are supported by the measured data?

---

# 28. Ideas for Further Experiments

Use this section as a backlog rather than immediately implementing every idea.

* [ ] Experiment:
* [ ] Experiment:
* [ ] Experiment:
* [ ] Experiment:

For each experiment, create an `EX-XXX` entry in the Experiment Log before running it.

---

# 29. Research Progress Log

## YYYY-MM-DD

### Work Completed

*

### What I Learned

*

### Problems Encountered

*

### Decisions Made

*

### Next Steps

*

---

# 30. Final Research Summary

*To be completed after the experimental phase.*

## Research Question

> ...

## Method

...

## Main Results

...

## Main Trade-Offs

...

## Main Finding

...

## Limitations

...

## Future Work

...

---

# 31. References

1. David et al., "TensorFlow Lite Micro: Embedded Machine Learning on TinyML Systems," MLSys 2021.
2. Lai et al., "CMSIS-NN: Efficient Neural Network Kernels for Arm Cortex-M CPUs."
3. Gholami et al., "A Survey of Quantization Methods for Efficient Neural Network Inference."
4. Han, Mao, and Dally, "Deep Compression."
5. Han, Pool, Tran, and Dally, "Learning both Weights and Connections for Efficient Neural Networks."
6. Ali and Yun, "RT-Gang: Real-Time Gang Scheduling Framework for Safety-Critical Systems."
7. "Timing guarantees for inference of AI models in embedded systems."

---

# 32. Change Log

| Date           | Change                         | Reason                      |
| -------------- | ------------------------------ | --------------------------- |
| September 2026 | Initial research notes created | Establish research notebook |
|                |                                |                             |
|                |                                |                             |
