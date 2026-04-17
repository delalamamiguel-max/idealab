# Logistic Regression Specialist Archetype

## Overview
This archetype defines guardrails for logistic regression models with responsible feature governance and calibrated outputs.

## Core Principles
The following hard-stop rules must be strictly followed:
- **Uses an invalid target**: Must be binary or multinomial categorical.
- **Skips feature governance**: Lineage and drift monitoring required.
- **Ignores calibration**: Uncalibrated probabilities are rejected.
- **Bypasses fairness checks**: Fairness metrics required when data allows.
- **Hard-codes thresholds**: Static thresholds need justification.
- **Disregards class imbalance**: Mitigation strategy required when minority < 20%.
- **Circumvents audit logging**: MLflow tracking and approvals are mandatory.

## Standard Pattern
Implementations must demonstrate:
- **Reproducible pipelines**: Seeded RNGs and scripted orchestration.
- **Feature scaling**: Consistent training/inference scaling.
- **Regularization sweeps**: L1/L2 with cross-validation under budget.
- **Robust evaluation suites**: ROC-AUC, PR-AUC, calibration curves.
- **Explainability artifacts**: Coefficients, odds ratios, VIF, SHAP.
- **Model cards**: Intended use, segment performance, retraining triggers.
- **Automated regression tests**: Protect preprocessing and scoring logic.
- **Secure secret management**: Key Vault or managed identity for access.
