# Random Forest Model Constitution

## Purpose

This constitution defines the foundational principles, hard-stop rules, and mandatory governance patterns for the Random Forest model archetype. It ensures models built under this archetype are reproducible, explainable, fair, resource-efficient, and compliant with data governance and privacy constraints.

**Scope**: Training, evaluation, deployment, monitoring, and retraining of Random Forest classifiers or regressors (including variants like Extremely Randomized Trees) across batch and real-time contexts.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** output that violates these rules:

- ✘ **No data leakage**: Do not allow overlap or future-derived features between train/validation/test splits (including temporal leakage or target-encoded features built without proper out-of-fold strategy)
- ✘ **No unseeded randomness**: Do not omit explicit deterministic seeds (`random_state` + seed for any auxiliary RNG) in training, splitting, and hyperparameter search
- ✘ **No silent class imbalance**: Do not proceed with training if multi-class/imbalanced classification lacks documented strategy (class weights, resampling, threshold tuning) in config
- ✘ **No PII in features/logs**: Do not include direct identifiers (email, SSN, phone, exact address) or quasi-identifiers without approved hashing/tokenization; never log raw PII
- ✘ **No undocumented feature provenance**: Do not introduce engineered features without lineage reference (source dataset id + transformation hash)
- ✘ **No unconstrained hyperparameter sweep**: Do not run unbounded grid/random search lacking max iterations + resource/time budget in config
- ✘ **No excessive tree depth**: Do not allow `max_depth` unset or > configured hard ceiling (e.g., 40) without explicit waiver tag
- ✘ **No baseline omission**: Do not finalize a model without performance comparison to a simple baseline (e.g., stratified dummy or linear model) recorded
- ✘ **No unexplained performance degradation**: Do not push a model with statistically significant decline (> configured delta threshold) versus current production champion without override justification
- ✘ **No plaintext credentials**: Do not embed credentials in model code, config, feature store queries, or logging statements
- ✘ **No unsourced external data**: Do not ingest external enrichment data lacking compliance classification and source metadata

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

- ✔ **Config-driven hyperparameters**: All RF params (n_estimators, max_depth, min_samples_split, min_samples_leaf, max_features, bootstrap, class_weight) loaded from external YAML/JSON config; no literals in code
- ✔ **Deterministic seeds**: Single canonical `random_seed` stored in config, propagated to model, data split, and any sampling routine
- ✔ **Stratified & leakage-audited splits**: Use stratified (classification) or distribution-preserving (regression via quantile binning) splits; produce leakage audit log (list of overlapping keys or temporal anomalies = 0 is expected)
- ✔ **Explainability artifacts**: Persist feature importance (impurity-based + permutation) and SHAP summary (if feasible) with sha256 hash of training dataset feature matrix schema
- ✔ **Fairness metrics**: Compute and log group-level metrics (e.g., demographic parity difference, equal opportunity difference) for configured sensitive attributes; fail build if thresholds exceeded
- ✔ **Class imbalance handling**: Enforce one documented strategy: class_weight, focal-like reweighting (if wrapper), or controlled resampling; record chosen method and parameters
- ✔ **Quality metrics**: Log primary (AUC / RMSE / MAE / F1) and secondary calibration (Brier Score for classification) plus confidence intervals via bootstrap; abort if below minimal thresholds
- ✔ **Drift monitoring hooks**: Emit population stability index (PSI) and KS statistics per feature vs. training reference; schedule retrain trigger if drift > threshold
- ✔ **Governance hashes**: Compute sha256 over concatenated sorted list of feature names + hyperparameter key/value pairs; store as `model_config_hash` and `feature_set_hash`
- ✔ **Model serialization standard**: Persist model via approved format (e.g., joblib with compression or MLflow artifact) and include environment manifest (Python version, library versions)
- ✔ **External configs only**: All thresholds, fairness bounds, drift triggers, resource limits (CPU cores, memory cap) reside in config file — no magic numbers
- ✔ **Logging**: After training, log `record_count_train`, `record_count_valid`, `record_count_test`, and `sha256(concat_ws("|", primary_key_columns))` for each split
- ✔ **Resource bounds**: Enforce `n_estimators` upper limit and memory footprint estimation (approx trees * nodes * structure size) documented; abort if projected > capacity

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Early feature pruning**: Remove low-variance / high-missingness features prior to training to reduce noise and tree depth
- ➜ **Calibration**: Apply probability calibration (Platt / isotonic) post-training when classification threshold selection required
- ➜ **Balanced weighting before resampling**: Prefer class_weight adjustments over synthetic oversampling to avoid overfitting
- ➜ **Portable serialization**: Favor formats compatible with cross-language inference (e.g., Treelite conversion if latency-critical)
- ➜ **Batch inference optimization**: Use vectorized feature access and moderate batch sizes sized by memory profile rather than single-row scoring
- ➜ **Retraining cadence**: Schedule periodic evaluation (e.g., weekly drift check, monthly full retrain) rather than ad hoc
- ➜ **Monotonic constraints (alternative)**: If using gradient-boosted hybrid stack, preserve monotonic constraints for features with regulatory expectations
- ➜ **Parallelism limits**: Set `n_jobs` tuned to cluster slot allocation; avoid saturating all cores if shared environment
- ➜ **Model card generation**: Auto-generate a model card summarizing purpose, data sources, metrics, fairness evaluation, drift status
- ➜ **Sparse feature handling**: Convert high-cardinality categorical indicators to compressed sparse format before fitting to conserve memory
- ➜ **Cost-aware importance**: Weight feature importance interpretation by acquisition cost or latency to guide future pruning

---

**Version**: 1.0.0
**Last Updated**: 2025-10-23
**Source**: `/path/to/internal/governance/specs/model_random_forest_rules` (replace with authoritative path)
