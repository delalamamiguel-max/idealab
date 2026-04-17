# Isolation Forest Model Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the Isolation Forest anomaly detection archetype.

**Source**: Consolidated from internal `ml/anomaly/isolation_forest` guardrails and production retrospectives

## Model Description

Isolation Forest isolates anomalies by recursively partitioning the feature space with randomly drawn cuts. Points that require fewer splits to isolate appear anomalous because they fall in sparse regions. The algorithm depends on hyperparameters `n_estimators`, `max_samples`, `max_features`, and `contamination` to balance model stability, runtime, and the expected outlier rate. Careful feature preprocessing, contamination estimation, and post-fit calibration are required to avoid over-flagging or missing critical anomalies.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** output that violates these rules:

- ✘ **No unscaled numeric features**: Do not fit or score Isolation Forest on continuous features with ranges differing by >10x without applying scaling
- ✘ **No unchecked contamination**: Do not accept default `contamination` or thresholding without documented estimation (e.g., quantile analysis, baseline incident rate)
- ✘ **No blind thresholding**: Do not binarize anomaly scores without logging the decision function distribution and selected cutoff rationale
- ✘ **No mixed raw feature types**: Do not pass raw categorical/text columns without deterministic numeric encoding aligned with the distance metric
- ✘ **No silent null handling**: Do not drop or impute missing values without logging the strategy and affected record counts

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

- ✔ **Feature preprocessing pipeline**: Use a reproducible pipeline (e.g., `ColumnTransformer`) that applies scaling/encoding and persists transformers with the model
- ✔ **Hyperparameter study**: Document a sweep or heuristic notebook covering `n_estimators`, `max_samples`, and `contamination`, storing metrics and plots in object storage
- ✔ **Score diagnostics**: Log score quantiles, false positive baseline, precision/recall (when labels exist), and fail the run when flagged outliers exceed 2x the expected incident rate unless waived
- ✔ **Sampling discipline**: Enforce `max_samples` ≥ `min(256, n_features * 10)` and ensure bootstrap/offline sampling is reproducible via seeded draws
- ✔ **Model card + lineage**: Emit a model card documenting feature set, preprocessing, hyperparameters, calibration strategy, and evaluation artifacts, and persist lineage IDs alongside serialized models

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Robust scaling**: Favor `RobustScaler` or quantile transforms when heavy-tailed or skewed features dominate
- ➜ **Copula calibration**: Apply score calibration (e.g., isotonic regression, empirical CDF) to stabilize alert thresholds over time
- ➜ **Explainability hooks**: Provide SHAP/TreeExplainer outputs or path-based feature contribution summaries for triage dashboards
- ➜ **Adaptive monitoring**: Schedule drift checks on score distributions and update contamination estimates when baseline shifts are detected
- ➜ **Resource-aware inference**: Batch scoring jobs to keep memory usage below 70% of allocation and parallelize estimators with joblib/Dask where available

---

**Version**: 1.0.0
**Last Updated**: 2025-10-24
**Source**: `/Users/yc010e/Documents/Projects/pythonProject/apm0013448-aifc-ds/vibe_cdo-windsurf-integration/.cdo-aifc/memory/archetypes/isolation-forest-model-constitution.md`
