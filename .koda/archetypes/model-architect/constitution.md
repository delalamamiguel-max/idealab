# model architect Constitution

## Purpose

Establishes disciplined model development practices with reproducible training pipelines, MLflow registration, and enterprise-ready documentation.

## Lifecycle Guardrails (Metallic Framework)

Model pipelines progress through **Bronze → Silver → Gold** maturity tiers. Bronze supports exploratory builds, Silver enforces guarded pilots, and Gold formalizes production promotion. Hard-stop rules apply at every tier.

- **Bronze (PoC)**: Rapid experimentation in isolated workspaces with documented debt items and provisional governance approvals.
- **Silver (Pilot)**: Limited release requiring cost tracking, provenance surfacing, fairness/robustness evidence, and rollback plans before stakeholder exposure.
- **Gold (Production)**: Enterprise deployment with automated CI/CD gates, audit-ready lineage, resilience rehearsals, and continuous monitoring integrations.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** any approach that:

- ✘ **Skips MLflow tracking**: Every experiment must log parameters, metrics, artifacts, and code snapshot to MLflow.
- ✘ **Uses default experiment**: All runs must use named experiments via `mlflow.set_experiment()` with documented naming convention.
- ✘ **Ignores reproducibility**: Do not allow non-deterministic training without documented seeding and environment capture.
- ✘ **Trains without feature contracts**: Never build models on features lacking version-locked definitions in the feature store.
- ✘ **Skips model-specific feature validation**: Never train models without validating feature types match algorithm requirements. Numeric-only models (logistic regression, linear SVM, gradient boosting with certain implementations) **must** validate features are numeric before training. Training with incompatible feature types will cause ValueError or TypeError exceptions during fit/predict.
- ✘ **Uploads unmanaged weights**: All model artifacts must publish to MLflow Model Registry with appropriate stage—no file-only model storage.
- ✘ **Omits model signatures**: Reject model registration without input/output schema signatures.
- ✘ **Violates fairness policies**: Do not deploy models without fairness metrics on regulated attributes when applicable.
- ✘ **Uses unsupported runtimes**: Reject training on clusters or environments outside approved runtime versions.
- ✘ **Bypasses code review**: No CI/CD pipeline skipping automated testing, linting, or security scans.
- ✘ **Hardcodes credentials**: Never embed service principal secrets, access keys, or personal credentials in code—use Key Vault or managed identities only.
- ✘ **Ignores curse of dimensionality**: Never train models with unconstrained high-cardinality categorical features (>50 unique values without encoding strategy). High-dimensional feature spaces cause overfitting, poor generalization, sparse data problems, and exponential computational costs. All high-cardinality features must have documented encoding or reduction strategy before training.
- ✘ **Trains with insufficient data quality**: Do not proceed with training when (1) all features are null/dropped after preprocessing, (2) >90% of original rows dropped after cleaning, or (3) >90% of original columns dropped. Exit with clear error message and log dropped counts to MLflow before exiting.

## II. Mandatory Patterns (Must Apply)

The LLM **must** ensure:

### Configuration & Parameterization
- ✔ **Parameterized training scripts** with clear CLI or notebook widgets for data version, hyperparameters, and output location.
- ✔ **Configuration sections** at notebook/script top including:
  - **Model Metadata**: `MODEL_NAME`, `MODEL_VERSION`, `MODEL_PURPOSE`, `MODEL_OWNER`
  - **File naming convention**: `BASE_FILE_NAME = f"{MODEL_NAME}_{MODEL_VERSION}_built_{TIMESTAMP}"`
  - **Directory structure**: `ROOT_DIR/{MODEL_VERSION}/{BASE_FILE_NAME}/` for organizing artifacts by version
  - **Output paths**: `OUTPUT_DIR`, `MODEL_OUTPUT_DIR` for raw model artifacts
- ✔ **Timestamp conventions**: Use `YYYY_MM_DD` for dates and `YYYYMMDD_HHMMSS` for run identifiers to ensure sortability

### Data Flow Consistency & Variable Naming

**Principle**: Minimize context switching between data processing frameworks (Spark ↔ Pandas) and use descriptive variable names that reflect data transformation stages.

- ✔ **Consistent framework usage**:
  - **Spark operations**: Keep data in Spark for all distributed operations (filtering, column drops, type casts, joins) until conversion is necessary
  - **Single conversion point**: Convert from Spark to Pandas once when switching to sklearn/local processing
  - **Stay in Pandas**: After conversion, remain in Pandas for all preprocessing, feature engineering, and model training
  - **Avoid back-and-forth**: Never switch between Spark and Pandas multiple times—pick one framework and complete all operations before switching

- ✔ **Descriptive variable naming** (avoid overwriting):
  - **Framework prefix**: Distinguish data by framework (e.g., suffix `_spark` for Spark DataFrames, `_pandas` for Pandas)
  - **Transformation stages**: Use descriptive suffixes that indicate the transformation applied (`_cleaned`, `_validated`, `_processed`)
  - **Data separation**: Maintain distinct variables for features and target throughout pipeline
  - **Split preservation**: Create split variables once and never overwrite them
  - **Preprocessing clarity**: Use suffixes that describe preprocessing operations applied

- ✔ **Variable naming anti-patterns to avoid**:
  - ✘ **Never repeatedly overwrite base variables**: Reassigning the same variable loses transformation context
  - ✘ **Ambiguous names**: Avoid numbered suffixes without meaning—use descriptive transformation names
  - ✘ **Framework confusion**: Don't mix framework naming conventions without clear distinction

- ✔ **Pattern summary**:
  - **Good**: Each transformation stage creates a new descriptively-named variable
  - **Bad**: Repeatedly overwriting the same variable throughout the pipeline

### Feature Validation & Preprocessing
- ✔ **Sample data testing** before implementing transformation logic:
  - Request sample input data from user (minimum 10 rows, ideally without null values)
  - Use sample to validate type formatting, preprocessing logic, and encoding strategies
  - Test full transformation pipeline on sample before applying to production data
  - Document sample data characteristics in MLflow
- ✔ **Feature type validation** before model training:
  - Log feature dtypes to MLflow as artifact: `pd.DataFrame(X_train.dtypes, columns=['dtype']).to_csv('feature_types.csv')`
  - Validate compatibility: For numeric-only models, assert no `object` or `string` types in training data
  - Document preprocessing approach: Log encoding strategy, dropped columns, and transformation pipeline to MLflow
  - Synthetic data testing: Generate synthetic dataset with same schema (including categorical features) and validate preprocessing pipeline handles all feature types correctly
- ✔ **Preprocessing pipeline management**:
  - Use `sklearn.compose.ColumnTransformer` or equivalent for mixed feature types
  - Document categorical encoding strategy (one-hot, ordinal, target encoding) with justification
  - Validate training/inference consistency by testing pipeline on holdout synthetic data
  - Log preprocessing artifacts (encoders, scalers, feature names) for reproducibility

### Dimensionality Management & Curse of Dimensionality

**Understanding the Curse of Dimensionality:**
As feature dimensionality increases, the volume of the feature space grows exponentially, causing:
- **Data sparsity**: Training samples become sparse in high-dimensional space, reducing statistical power
- **Overfitting**: Models memorize noise instead of learning patterns, poor generalization to test data
- **Computational cost**: Training time, memory usage, and inference latency increase exponentially
- **Distance metrics breakdown**: All points become equidistant in high dimensions, weakening similarity-based algorithms
- **Feature interaction explosion**: Number of possible feature interactions grows combinatorially

**Critical Impact Areas:**
- OneHotEncoding a categorical feature with 1,000 unique values creates 1,000 binary features
- Cartesian feature crosses (e.g., `state × product × channel`) can explode to millions of combinations
- Wide feature sets reduce samples-per-feature ratio, violating statistical minimums (aim for ≥10 samples per feature)
- Tree-based models handle high dimensions better than linear models, but still suffer from increased variance

**Mandatory Practices:**

- ✔ **Cardinality profiling** before encoding:
  - Log cardinality analysis to MLflow (feature name, unique_count, cardinality_ratio)
  - Save analysis as CSV artifact: `feature_cardinality_analysis.csv`
  - Document cardinality thresholds in model card: low (<10), medium (10-50), high (50-500), very high (>500)
  - Flag features exceeding thresholds for special handling

- ✔ **High-cardinality categorical feature strategies** (choose based on cardinality and model type):

  **For Low Cardinality (2-10 unique values):**
  - **One-Hot Encoding**: `OneHotEncoder(drop='first', handle_unknown='ignore')`
  - Document: "One-hot encoding justified by low cardinality (n={n_unique}), creating {n_unique-1} features"

  **For Medium Cardinality (10-50 unique values):**
  - **Target Encoding**: `TargetEncoder(smoothing=1.0, min_samples_leaf=20)` - encode by mean target value
  - **Frequency Encoding**: Replace category with occurrence frequency
  - Document: "Target encoding with smoothing=1.0 to prevent overfitting on rare categories"

  **For High Cardinality (50-500 unique values):**
  - **Target Encoding with Cross-Validation**: Higher regularization (smoothing=10.0), out-of-fold encoding to prevent leakage
  - **Grouping Rare Categories**: Keep top N categories (e.g., 20), consolidate long-tail into 'Other' bucket
  - **Feature Hashing**: `FeatureHasher(n_features=32)` for fixed-size hash-based encoding
  - Document: "Grouped rare categories (<1% frequency) into 'Other', retaining top 20 categories (95% coverage)"

  **For Very High Cardinality (>500 unique values):**
  - **Embeddings**: Learn dense representations via neural networks (embedding_dim = min(50, cardinality/2))
  - **Drop feature**: If no viable encoding strategy, document rationale and remove
  - **Feature engineering**: Extract meaningful subcomponents (e.g., email domain from email address)
  - Document: "Extracted email_domain from email (reduced cardinality from 50K to 200 domains)"

- ✔ **Dimensionality reduction** when feature count exceeds samples:
  - **PCA**: `PCA(n_components=0.95)` to retain 95% variance, log n_components and explained_variance to MLflow
  - **Feature selection**: Use `SelectKBest` with mutual_info_classif or chi-square, log selected features
  - **Regularization**: L1 penalty (`LogisticRegression(penalty='l1', solver='saga')`) or ElasticNet to induce sparsity
  - Document: "Applied PCA to reduce 500 numeric features to 50 components (95% variance retained)"

- ✔ **Decision rules for encoding strategy selection**:
  - **Cardinality ≤ 10**: Use 'onehot' (safe for low cardinality)
  - **Cardinality ≤ 50**: Use 'target' (supervised encoding with regularization)
  - **Cardinality ≤ 200**: Use 'group' (group rare categories, then target encode)
  - **Cardinality_ratio > 0.95**: Use 'drop' (near-unique values like IDs have no predictive value)
  - **Cardinality > 200**: Use 'hash' (feature hashing for very high cardinality)
  - Log encoding decisions to MLflow as artifact: `encoding_strategy_decisions.csv` (feature, cardinality, strategy)

- ✔ **Monitoring dimensional impact**:
  - Log before/after feature counts: `mlflow.log_param('features_before_encoding', n_features_raw)`
  - Log effective dimensionality: `mlflow.log_param('features_after_encoding', n_features_encoded)`
  - Log sparsity metrics: `mlflow.log_metric('feature_sparsity', (X_encoded == 0).mean().mean())`
  - Log samples-per-feature ratio: `mlflow.log_metric('samples_per_feature', n_samples / n_features)`
  - **Warning threshold**: Flag if samples-per-feature < 10 (high overfitting risk)

- ✔ **Model-specific considerations**:
  - **Linear models** (Logistic Regression, Linear SVM): Highly sensitive to dimensionality, require aggressive feature selection or regularization
  - **Tree-based models** (Random Forest, XGBoost): More robust to high dimensions via feature subsampling, but still benefit from reduction
  - **Neural networks**: Can handle high dimensions with embeddings, but require more data and regularization (dropout, L2)
  - **Distance-based models** (KNN, K-Means): Extremely sensitive to curse of dimensionality, distances become meaningless in high dimensions
  - Document: "Using XGBoost with colsample_bytree=0.5 to handle 200 features via random subsampling"

- ✔ **Validation against dimensionality issues**:
  - **Synthetic testing**: Generate synthetic high-cardinality features and verify encoding pipeline doesn't explode dimensions
  - **Train/test performance gap**: Large gap indicates overfitting from excessive dimensions
  - **Feature importance analysis**: Identify and prune features with near-zero importance
  - **Memory profiling**: Monitor memory usage during encoding to prevent OOM errors with large categorical expansions

### Experiment Tracking & Lineage
- ✔ **Named experiment organization**: Use `mlflow.set_experiment("{business_unit}/{model_family}/{purpose}")` before training
  - Prompt user for experiment details: business unit, model family, purpose, owner
  - Use configuration section pattern with `MODEL_OWNER`, `MODEL_PURPOSE` variables
  - Validate experiment name follows convention
- ✔ **Experiment logging** that records:
  - Dataset version, feature table hashes, git commit SHA, and environment packages
  - Data source URIs with authentication method (service principal, managed identity)
  - Training/test/OOT date boundaries as tags
  - Filter conditions applied to source data
  - Feature list with data types as artifact JSON
  - Preprocessing pipeline configuration and fitted transformers
- ✔ **Credential management**:
  - Use Key Vault scope + key name pattern: `dbutils.secrets.get(scope=VAULT_SCOPE, key=VAULT_KEY_NAME)`
  - Document service principal configuration requirements (client ID, tenant ID, endpoint)
  - Never log credentials to MLflow tags/params/artifacts

### Hyperparameter Tuning
- ✔ **Automated hyperparameter tuning** (Hyperopt/Optuna) where complexity warrants, constrained by budget controls:
  - **Note**: H2O training may not be available on current cluster configurations due to initialization constraints
  - Pre-trained H2O DriverlessAI models (.mojo format) can be loaded using daimojo library
  - For .mojo loading: retrieve license key from Key Vault, set `DRIVERLESS_AI_LICENSE_KEY` environment variable
  - Reference template: `.cdo-aifc/templates/02-ml-operations-lifecycle/h2o-mojo-loading-template.py`
  - Define search space as dictionary: `hyper_params = {'learn_rate': [0.01, 0.1], 'max_depth': [3, 5, 7]}`
  - Use parent-child run hierarchy: parent run for overall search, child runs for each trial
  - Log grid search configuration as params in parent run
  - Include `GRID_SEARCH = True/False` flag for toggling
- ✔ **Model selection criteria**: Document primary metric for model selection (e.g., `sort_by='auc'`) and log as tag

### Model Evaluation
- ✔ **Model evaluation** capturing train/validation/test metrics with confidence intervals and calibration checks:
  - Use helper functions: `get_metrics(model)` returning standardized dict
  - Include OOT validation as separate dataset with `_oot` metric suffix
  - Log confusion matrix elements as individual metrics for tracking
- ✔ **Benchmark baselines** training governed regression/classification benchmarks (e.g., linear models, gradient boosting) with cross-validated tuning and MLflow comparisons when AutoML services are unavailable.
- ✔ **Visualization artifacts**:
  - Use helper function: `get_graphs(model, output_dir)` generating ROC, PR curves, variable importance
  - Save at 200+ DPI for production documentation
  - Store file paths in dict for organized artifact logging

### Model Registration & Packaging
- ✔ **MLflow Model Registry integration**:
  - Register all production-candidate models: `mlflow.{flavor}.log_model(model, artifact_path, registered_model_name=...)`
  - Use naming convention: `{MODEL_NAME}_{MODEL_VERSION}` or `{business_unit}/{model_family}`
  - Set initial stage to `None` pending validation
  - NEVER deploy models that exist only as file artifacts without registry entry
- ✔ **Artifact packaging** including:
  - Inference signature with input/output schema: `signature = mlflow.models.infer_signature(X_train, predictions)`
  - Conda/pip environment files for reproducibility
  - Model-specific flavor logging (e.g., `mlflow.h2o.log_model`, `mlflow.sklearn.log_model`)
  - Separate model save for deployment: `mlflow.{flavor}.save_model(model, path)` to file system
- ✔ **Deployment artifacts**:
  - Configuration dict: `DEPLOYMENT_PARAMS` with model metadata, target environment, pipeline settings
  - Separation of deployment decision flag: `DEPLOY_MODEL = True/False`
  - Deployment path structure: `{STORAGE_BASE}/{model_family}/{BASE_FILE_NAME}/raw_model/`

### Documentation & Governance
- ✔ **Documentation** summarizing model objective, assumptions, limitations, and acceptance criteria:
  - Log as artifact: experiment design document, model card, training notebook
  - Include bias assessment documentation reference in tags: `bias_doc` field
- ✔ **CI integration** with Azure DevOps pipelines to run unit tests, style checks, and static analysis.
- ✔ **Security scanning** for dependencies (e.g., `pip-audit`, `safety`) prior to registry promotion.
- ✔ **Separation of concerns**:
  - Experiment tracking (MLflow logging) separate from deployment execution
  - Deployment triggered via separate notebook call: `dbutils.notebook.run('/Shared/mlflow/model_deployment', params=...)`
  - Model comparison to prior version controlled by flag: `COMPARE_TO_PREV_MODEL = True/False`

## III. Preferred Patterns (Recommended)

The LLM **should** adopt:

- ➜ **Modular training architecture** separating data prep, training, evaluation, and registration steps.
- ➜ **Benchmark harnesses** maintaining reusable scripts for ablation studies, robustness stress tests, and heuristic or production baselines so bespoke models continually justify promotion.
- ➜ **Distributed training** leveraging Databricks `TorchDistributor` or Spark MLlib when beneficial.
- ➜ **Advanced metrics** such as SHAP-backed feature importance, residual diagnostics, and uplift analysis.
- ➜ **Integration tests** that validate end-to-end training execution inside CI pipelines.
- ➜ **Promotion checklists** requiring sign-off from data owners, security, and business sponsors.

---

**Version**: 1.4.0
**Last Updated**: 2025-11-15
**Changelog**:
- v1.4.0: Added hard-stop for data quality thresholds (>90% row/column drop prevention)
- v1.4.0: Added sample data testing requirement before transformation logic
- v1.4.0: Added MLflow experiment path user input prompting guidance
- v1.4.0: Clarified H2O usage constraints (training unavailable, .mojo loading supported)
- v1.4.0: Added reference to H2O .mojo loading template
- v1.3.0: Added "Data Flow Consistency & Variable Naming" mandatory patterns section
- v1.3.0: Documented framework consistency principles (Spark → Pandas single conversion)
- v1.3.0: Added descriptive variable naming conventions (df_spark, df_pandas, df_cleaned, X_raw, X_validated, etc.)
- v1.3.0: Documented anti-patterns to avoid (repeated overwrites of df and X)
- v1.3.0: Added code clarity examples showing good vs bad data flow patterns
- v1.2.0: Condensed dimensionality management section (removed verbose code examples, maintained technique summaries and requirements)
- v1.2.0: Added hard-stop rule for curse of dimensionality - prohibits unconstrained high-cardinality features (>50 unique values)
- v1.2.0: Added comprehensive "Dimensionality Management & Curse of Dimensionality" mandatory patterns section
- v1.2.0: Documented encoding strategies for low/medium/high/very-high cardinality categorical features (one-hot, target, frequency, hashing, grouping, embeddings)
- v1.2.0: Added cardinality profiling requirements with MLflow logging of cardinality analysis
- v1.2.0: Added decision rules for encoding strategy selection based on cardinality thresholds
- v1.2.0: Added dimensionality reduction techniques (PCA, feature selection, regularization)
- v1.2.0: Added monitoring requirements for dimensional impact (sparsity, samples-per-feature ratio)
- v1.2.0: Added model-specific considerations for handling high-dimensional feature spaces
- v1.1.0: Added hard-stop rule for model-specific feature validation to prevent type incompatibility errors
- v1.1.0: Added mandatory patterns for feature type validation and preprocessing pipeline management
- v1.1.0: Added requirement for synthetic data testing to validate preprocessing before production training
- v1.1.0: Added logging requirements for preprocessing artifacts and feature dtypes
