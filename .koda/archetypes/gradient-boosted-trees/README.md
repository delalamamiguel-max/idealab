# Gradient Boosted Trees Archetype

## Overview
This archetype establishes guardrails for gradient boosted trees, covering design, tuning, and deployment in regulated analytics contexts.

## Core Principles
The following hard-stop rules must be strictly followed:
- **No label leakage**: Exclude target-derived or future-dated features.
- **No evaluation contamination**: Do not reuse validation/test splits for training.
- **No uncontrolled growth**: Set explicit limits on estimators, depth, and learning rate.
- **No imbalance neglect**: Apply mitigation for class imbalance > 10:1.
- **No reproducibility gaps**: Deterministic seeds are required.
- **No opaque raw features**: Encode categorical/text features.

## Standard Pattern
Implementations must demonstrate:
- **Documented data splits**: Boundaries stored and logged (e.g., MLflow).
- **Hyperparameter manifest**: Configured learning rate, depth, regularization, early stopping.
- **Early stopping protocol**: Validation monitoring with thresholds tied to KPIs.
- **Feature audit**: SHAP or permutation importance for dominant drivers.
- **Calibration diagnostics**: Reliability curve/Brier score before deployment.
- **Bias and stability checks**: Subgroup performance, drift monitoring, sensitivity analyses.
- **Model registry integration**: Log artifacts, params, and metrics with approval metadata.
