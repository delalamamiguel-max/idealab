# Isolation Forest Model Archetype

## Overview
This archetype defines guardrails for the Isolation Forest anomaly detection model, focusing on safe feature handling, calibrated thresholds, and auditable operations.

## Core Principles
The following hard-stop rules must be strictly followed:
- **No unscaled numeric features**: Scale continuous features before fitting.
- **No unchecked contamination**: Document contamination estimation.
- **No blind thresholding**: Log score distributions and cutoff rationale.
- **No mixed raw feature types**: Encode categorical/text features.
- **No silent null handling**: Log missing-value strategy and counts.

## Standard Pattern
Implementations must demonstrate:
- **Feature preprocessing pipeline**: Reproducible scaling/encoding via transformers.
- **Hyperparameter study**: Sweep n_estimators, max_samples, contamination with stored metrics.
- **Score diagnostics**: Quantiles, false-positive baselines, and guardrails on flagged rates.
- **Sampling discipline**: Enforce max_samples bounds and seeded draws.
