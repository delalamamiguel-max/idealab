# DBSCAN Model Archetype

## Overview
This archetype defines the foundational principles and hard-stop rules for DBSCAN clustering. It emphasizes density-based clustering with governed hyperparameters and preprocessing.

## Core Principles
The following hard-stop rules must be strictly followed:
- **No unscaled numeric features**: Standardize or normalize continuous features.
- **No arbitrary epsilon**: eps must have documented justification.
- **No under-sized neighborhoods**: min_samples must meet max(3, n_features + 1).
- **No mixed raw feature types**: Encode categorical/text features deterministically.
- **No silent null handling**: Log missing-value strategy and counts.
- **No dark deployments**: Require telemetry for clustering metrics.

## Standard Pattern
Implementations must demonstrate:
- **Feature preprocessing pipeline**: Reproducible scaling/encoding artifacts.
- **Parameter selection workflow**: Rationale and plots for eps/min_samples.
- **Cluster diagnostics**: Log density metrics, cluster sizes, and noise ratio with failure thresholds.
