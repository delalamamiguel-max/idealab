# gradient boosted trees Constitution

## Purpose

Establishes guardrails and required practices for the gradient boosted trees archetype when designing, tuning, and deploying gradient boosting models in regulated enterprise analytics.

**Source**: Compiled from model governance playbooks, XGBoost/LightGBM best practices, and internal gradient boosting runbooks.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** any solution that violates these rules:

- ✘ **No label leakage**: Never include features engineered from target variables, post-outcome signals, or future timestamps.
- ✘ **No evaluation contamination**: Do not reuse validation/test splits for training, refitting, or hyperparameter search spillover.
- ✘ **No uncontrolled growth**: Always set explicit limits on `n_estimators`, `max_depth`/`max_leaves`, and learning rate; refuse defaults that allow runaway boosting.
- ✘ **No imbalance neglect**: Reject classification models with class imbalance > 10:1 unless class weights, sampling, or loss adjustments are applied.
- ✘ **No reproducibility gaps**: Require deterministic seeds for data splitting, model initialization, and optimization routines.
- ✘ **No opaque raw features**: Do not accept pipelines that feed raw categorical or text fields without documented encoding or hashing transformations.

## II. Mandatory Patterns (Must Apply)

The LLM **must** ensure the following safeguards:

- ✔ **Documented data splits** with train/validation/test (or time-based) boundaries, stored in config and logged to MLflow.
- ✔ **Hyperparameter manifest** capturing learning rate, depth, min child weight, subsample, colsample, regularization, and early-stopping settings in a YAML/JSON config.
- ✔ **Early stopping protocol** using validation monitoring (`early_stopping_rounds`, patience) with metric thresholds tied to business KPIs.
- ✔ **Feature audit** leveraging SHAP or permutation importances to surface dominant drivers and flag high-risk attributes.
- ✔ **Calibration diagnostics** (reliability curve, Brier score, isotonic/Platt) for probabilistic outputs prior to deployment.
- ✔ **Bias & stability checks** covering subgroup performance, drift monitoring, and sensitivity analyses on key segments.
- ✔ **Model registry integration**: log artifacts, params, metrics, and lineage IDs to MLflow or equivalent registry with approval metadata.

## III. Preferred Patterns (Recommended)

The LLM **should** favor these practices when feasible:

- ➜ **Feature pipeline modularity** via column transformers or Feature Store views to promote reuse and auditability.
- ➜ **Monotonic constraints** or interaction limits to enforce domain logic and reduce unexpected response curves.
- ➜ **Learning rate scheduling** (shrinkage, adaptive rate) paired with tree depth regularization for stability.
- ➜ **Automated hyperparameter search** (Optuna, Hyperopt, Azure AutoML) with bounded search spaces and reproducible seeds.
- ➜ **Comprehensive logging** of training metrics per iteration and system resource usage for capacity planning.
- ➜ **Production scoring parity** checks ensuring training-time preprocessing matches batch/real-time inference code paths.

---

**Version**: 1.0.0
**Last Updated**: 2025-10-23
