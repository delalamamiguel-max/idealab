# Model Architect Archetype

## Overview
This archetype establishes disciplined model development practices with reproducible training pipelines, MLflow registration, and enterprise-ready documentation.

## Core Principles
The following hard-stop rules must be strictly followed:
- **Skips MLflow tracking**: Every experiment must log parameters/metrics.
- **Ignores reproducibility**: Do not allow non-deterministic training.
- **Trains without feature contracts**: Never build on features lacking definitions.
- **Uploads unmanaged weights**: All artifacts must publish to Model Registry.
- **Violates fairness policies**: Do not deploy without fairness metrics.
- **Uses unsupported runtimes**: Reject training on unapproved environments.
- **Bypasses code review**: No CI/CD pipeline skipping automated testing.

## Standard Pattern
Implementations must demonstrate:
- **Parameterized training scripts**: With CLI/widget inputs.
- **Experiment logging**: Recording dataset version and git commit.
- **Automated hyperparameter tuning**: Constrained by budget controls.
- **Model evaluation**: Capturing train/test metrics.
- **Benchmark baselines**: Training governed benchmarks.
