# Random Forest Model Archetype

## Overview
This archetype defines the foundational principles for Random Forest models, ensuring reproducibility, explainability, fairness, and governance compliance.

## Core Principles
The following hard-stop rules must be strictly followed:
- **No data leakage**: Avoid overlap or future-derived features between splits.
- **No unseeded randomness**: Explicit deterministic seeds required.
- **No silent class imbalance**: Document strategy for imbalance mitigation.
- **No PII in features/logs**: Tokenize identifiers; never log raw PII.
- **No undocumented feature provenance**: Provide lineage references.
- **No unconstrained hyperparameter sweep**: Enforce search budgets.
- **No excessive tree depth**: Apply a hard ceiling on max_depth.
- **No baseline omission**: Compare against simple baselines.
- **No unexplained degradation**: Block promotion on significant metric drops.
- **No plaintext credentials**: Keep secrets out of code/config/logs.
- **No unsourced external data**: Require compliance classification.

## Standard Pattern
Implementations must demonstrate:
- **Config-driven hyperparameters**: Load all params from external config.
- **Deterministic seeds**: Single canonical random_seed.
- **Stratified and leakage-audited splits**: Audit for overlap.
- **Explainability artifacts**: Feature importance and SHAP summaries.
- **Fairness metrics**: Compute group-level metrics with thresholds.
- **Class imbalance handling**: Use documented weighting/resampling.
- **Quality metrics**: Log primary and calibration metrics.
- **Drift monitoring hooks**: Emit PSI/KS and schedule retrain triggers.
- **Governance hashes**: Store model_config_hash and feature_set_hash.
- **Approved serialization**: Persist with environment manifest.
