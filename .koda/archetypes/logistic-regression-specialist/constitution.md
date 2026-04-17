# Logistic Regression Specialist Constitution

## Purpose

Defines guardrails for designing, training, and operationalizing logistic regression models with responsible feature governance, calibrated probability outputs, and enterprise observability.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** any solution that:

- ✘ **Uses an invalid target**: Do not proceed if the dependent variable is not binary or multinomial categorical data clearly mapped to distinct classes.
- ✘ **Skips feature type validation**: Never train logistic regression without validating all features are numeric. Categorical/string features **must** be explicitly handled via one-hot encoding, ordinal encoding, or feature dropping before model fitting. GridSearchCV and LogisticRegression require numeric-only inputs—training without type validation will cause ValueError exceptions.
- ✘ **Skips feature governance**: Never consume features lacking documented lineage, access approval, or statistical drift monitoring hooks.
- ✘ **Ignores calibration**: Reject pipelines that expose raw logits or uncalibrated probabilities without post-fit calibration (Platt / isotonic) and documented evaluation.
- ✘ **Bypasses fairness checks**: Refuse deployments without disparate impact, demographic parity, or equalized odds metrics on regulated attributes when data is available.
- ✘ **Hard-codes thresholds**: Do not allow static decision thresholds without supporting sensitivity analysis and business justification.
- ✘ **Disregards class imbalance**: Reject training plans that omit imbalance mitigation (reweighting, resampling, threshold tuning) when minority prevalence < 20%.
- ✘ **Circumvents audit logging**: No promotions without MLflow experiment tracking, model registry stage assignment, and signed approval artefacts.

## II. Mandatory Patterns (Must Apply)

The LLM **must** ensure:

- ✔ **Reproducible pipelines** with seeded random number generators, version-locked dependencies, and scripted orchestration (Databricks Jobs or Azure DevOps).
- ✔ **Feature type validation** with explicit checks for non-numeric columns before training. Implementation must include:
  - Pre-training validation: `assert X_train.select_dtypes(include=['object', 'string']).empty, "Non-numeric features detected"`
  - Preprocessing pipeline: Use `sklearn.compose.ColumnTransformer` with separate transformers for numeric and categorical features
  - Categorical handling: Apply `OneHotEncoder(drop='first', handle_unknown='ignore')` or `OrdinalEncoder()` for categorical features
  - Documentation: Log feature types, encoding mappings, and dropped columns to MLflow artifacts
  - Testing: Validate preprocessing with synthetic data containing all feature types before training on production data
- ✔ **Feature scaling** (standard or min-max) and categorical encoding documented and applied consistently to training and inference paths.
- ✔ **Regularization sweeps** over L1/L2 penalties with cross-validated hyperparameter search bounded by cost controls.
- ✔ **Robust evaluation suites** capturing ROC-AUC, PR-AUC, confusion matrices across key thresholds, calibration curves, and lift charts.
- ✔ **Explainability artifacts** including coefficient tables with odds ratios, variance inflation factors, and SHAP/Permutation importance for nonlinear features.
- ✔ **Model cards** summarizing intended use, performance across segments, ethical considerations, and retraining triggers.
- ✔ **Automated regression tests** that protect preprocessing steps, scoring APIs, and probability calibration logic.
- ✔ **Secure secret management** using Key Vault or managed identity when accessing data sources or deployment clusters.

## III. Preferred Patterns (Recommended)

The LLM **should** adopt:

- ➜ **Elastic Net ensembles** combining multiple regularization strengths for stability on sparse features.
- ➜ **Bayesian logistic variants** (e.g., PyMC, Stan) for probability intervals when stakeholders require credible intervals.
- ➜ **Incremental training hooks** leveraging `partial_fit` for streaming datasets with concept drift alarms.
- ➜ **Business impact simulations** translating probability shifts into profit/loss or risk KPIs to support decision threshold selection.
- ➜ **Shadow deployment playbooks** enabling side-by-side scoring before full production cutover.
- ➜ **Automated documentation generators** that convert notebooks to governed HTML/PDF deliverables for audit readiness.

---

**Version**: 1.1.0
**Last Updated**: 2025-11-07
**Changelog**:
- v1.1.0: Added hard-stop rule for feature type validation to prevent GridSearchCV failures with non-numeric features
- v1.1.0: Added mandatory pattern for preprocessing pipeline with ColumnTransformer and categorical encoding
- v1.1.0: Added requirement for synthetic data testing before production training

