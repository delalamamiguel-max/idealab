# feature architect Constitution

## Purpose

Defines the guardrails for producing reusable, high-quality features with reproducible lineage across Databricks Feature Store, Feast, and downstream ML consumers.

## Lifecycle Guardrails (Metallic Framework)

Feature pipelines mature through **Bronze → Silver → Gold** tiers. Bronze prototypes may relax certain operational controls, provided a documented path exists to meet the stricter Silver and Gold expectations before promotion. Hard-stop rules remain in force at every tier.

- **Bronze (PoC)**: Fast iteration in isolated dev workspaces. Cost tracking, resilience automation, and governed access can be lightweight, but backlog items must outline the Silver upgrade path.
- **Silver (Pilot)**: Limited production exposure. Enforce baseline cost observability, retention policies, RBAC, and resilient deployment patterns before onboarding downstream consumers.
- **Gold (Production)**: Full enterprise rollout. Fully automated monitoring, budget guardrails, audited retention, and least-privilege access are mandatory with documented SLOs and rollback/runbooks.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** any implementation that:

- ✘ **Skips source validation**: Never engineer features without validating raw input freshness, schema, and quality metrics.
- ✘ **Breaks feature contract**: Do not publish features lacking documented data types, allowed ranges, business definitions, or owners.
- ✘ **Violates temporal integrity**: No target leakage—prevent future data from entering training features via improper joins/windowing.
- ✘ **Bypasses feature store**: Do not deliver features outside the governed feature store or without registration metadata.
- ✘ **Ignores privacy policies**: Do not include PII without tokenization or hashing per compliance rules.
- ✘ **Uses non-deterministic transforms**: Avoid random or non-reproducible operations without seeded randomness.
- ✘ **Fails to version**: Never overwrite feature tables without versioning and change history in MLflow or Delta logs.
- ✘ **Ignores feature engineering sophistication**: Do not deploy simplistic features when advanced techniques (target encoding, polynomial interactions, embeddings) could significantly improve model performance. Features should represent the art and science of extracting maximum signal from raw data.

## II. Mandatory Patterns (Must Apply)

The LLM **must** include these requirements:

### Core Feature Engineering Practices

- ✔ **Point-in-time correctness** enforced via time-travel joins, window clauses, or `as_of_ts` logic.
- ✔ **Feature quality tests** verifying null rates, monotonicity, Drisk metrics, and duplicate checks with automated alerts.
- ✔ **Metadata registration** storing `feature_name`, `description`, `owner`, `data_source`, and `lineage` in Feature Store APIs.
- ✔ **Automated documentation** generating markdown or HTML summaries for each feature group.
- ✔ **Training-serving skew detection** comparing offline vs. online distributions with configured thresholds.
- ✔ **Parameterization** through YAML/JSON to control aggregation windows, filters, and default TTL.
- ✔ **Dependency graph** logging to Purview or Unity Catalog for lineage.
- ✔ **Unit tests** for transformation logic using `pytest` or `chispa` for Spark-specific assertions.
- ✔ **Operational resilience (Silver+)** implementing idempotent writes, retry policies, checkpointing, and tested rollback plans; Bronze builds must document upgrades before promotion.
- ✔ **Cost governance (Silver+)** capturing run-level compute/storage spend, budget guardrails, and alert thresholds; Bronze may use ad hoc tracking but must define Silver instrumentation.
- ✔ **Retention and access controls (Silver+)** enforcing policy-aligned data retention windows, Unity Catalog or Purview RBAC, and access audits for feature tables; Bronze prototypes log intended control owners.

### Advanced Feature Engineering Techniques

**The Art and Science of Feature Engineering:**
Feature engineering is the alchemy that transforms raw data into actionable insights. Advanced practitioners go beyond basic transformations to extract nuanced patterns and create features that enhance model understanding of complex relationships. The following techniques represent sophisticated approaches that distinguish expert-level feature engineering.

#### 1. Target Encoding with Regularization

**Purpose**: Encode high-cardinality categorical features while preventing overfitting on rare categories.

**Techniques**: Bayesian smoothing via `category_encoders.TargetEncoder` (smoothing=1.0), cross-validation encoding to prevent target leakage, higher-order interactions (e.g., state × merchant_type).

**Benefits**: Single numeric feature from high-cardinality categorical, avoids dimension explosion, regularization prevents overfitting, better than one-hot for 10+ unique values.

**Requirements**: Document smoothing parameters, log encoder to MLflow, verify no target leakage, store transformation metadata.

#### 2. Polynomial Feature Generation with Selective Engineering

**Purpose**: Capture non-linear relationships while avoiding curse of dimensionality.

**Techniques**: Selective polynomial generation via `PolynomialFeatures` + `SelectKBest` feature selection, domain-guided interactions (amount × frequency, amount²).

**Benefits**: Captures quadratic effects and interactions, feature selection prevents dimensionality explosion, domain guidance ensures interpretability.

**Requirements**: Apply feature selection after generation, document selected features and rationale, log degree and selection criteria.

#### 3. Intelligent Binning and Discretization

**Purpose**: Transform continuous features into categorical representations respecting data distribution.

**Techniques**: Decision tree-based binning (`DecisionTreeClassifier` for optimal split points), quantile binning (equal-frequency bins via `pd.qcut`).

**Benefits**: Bins respect target variable relationship, handles skewed distributions, captures non-linear patterns in linear models.

**Requirements**: Log binning strategy and thresholds, document bin boundaries, validate bin population balance.

#### 4. Time-Based Feature Extraction

**Purpose**: Capture temporal dynamics, trends, and seasonality in time series data.

**Techniques**: Lag features (shift by 1d/7d/30d/365d), rolling statistics (mean/std/min/max over windows), trend features (MoM/YoY growth, momentum), Fourier transforms (cyclical pattern detection).

**Benefits**: Leverages historical context, captures seasonality and trends, detects cyclical patterns, improves time series forecasting.

**Requirements**: Document lag periods and windows, group by entity ID, handle edge cases (min_periods), log transformation parameters.

#### 5. Feature Interactions

**Purpose**: Create features representing interactions between two or more features.

**Techniques**: Ratio features (transaction/balance, fraud/total), difference features (amount deviation, time since last), tree-extracted interactions (GBM leaf indices as features).

**Benefits**: Captures relative relationships, detects deviations and anomalies, learns complex interactions automatically.

**Requirements**: Document interaction formulas, validate denominator handling (avoid division by zero), log interaction definitions.

#### 6. Embedding Representations for High-Cardinality Categoricals

**Purpose**: Map high-cardinality categorical features to continuous vector spaces.

**Techniques**: Entity embeddings (neural network learned, embedding_dim=min(50, cardinality/2)), pre-trained embeddings (Word2Vec for sequences).

**Benefits**: Reduces dimensionality (1,000 categories → 50 features), learns latent representations, captures category relationships.

**Requirements**: Log embedding model to MLflow, document embedding dimension rationale, validate embedding coverage.

#### 7. Feature Clustering

**Purpose**: Create features representing cluster membership and distances.

**Techniques**: K-Means cluster labels + distance to centroids, DBSCAN for outlier detection (cluster=-1 indicates outlier).

**Benefits**: Reveals natural groupings, provides continuous similarity measures, identifies outliers/anomalies.

**Requirements**: Document clustering algorithm and parameters, log cluster centroids, validate cluster quality metrics.

#### 8. Dimensionality Reduction as Feature Engineering

**Purpose**: Create lower-dimensional representations retaining maximum information.

**Techniques**: PCA (retain 95% variance), t-SNE (visualization and pattern discovery, n_components=2).

**Benefits**: Reduces feature count while preserving variance, reveals hidden structure, improves computational efficiency.

**Requirements**: Log transformation object, document variance explained, validate information retention.

#### 9. Feature Selection with Mutual Information

**Purpose**: Select features based on non-linear dependencies with target.

**Techniques**: Mutual information scoring via `mutual_info_classif`, iterative selection with residuals (add features based on MI with prediction errors).

**Benefits**: Captures non-linear relationships (better than correlation), reduces noise, improves model performance.

**Requirements**: Log MI scores to MLflow, document selection criteria, validate selected features on holdout data.

#### 10. Synthetic Feature Generation

**Purpose**: Generate entirely new features through novel combinations and transformations.

**Techniques**: Feature crossing (state × product), feature hashing (FeatureHasher for high-cardinality crosses), domain-specific ratios (financial, e-commerce), automated synthesis (featuretools deep feature synthesis).

**Benefits**: Creates novel perspectives, captures complex interactions, leverages domain knowledge, automates feature discovery.

**Requirements**: Document synthesis methodology, validate synthetic features improve performance, log generation parameters.

#### 11. Text Preprocessing and Normalization

**Purpose**: Standardize raw text corpora to enable reliable downstream feature extraction.

**Techniques**: Text cleaning (lowercasing, punctuation/HTML stripping, Unicode NFKC), tokenization (word, sentence, or subword), lemmatization/stemming (spaCy, NLTK), stopword management with domain-specific overrides.

**Benefits**: Reduces vocabulary entropy, improves consistency, removes noise, and protects against encoding artifacts.

**Requirements**: Document normalization policy, log tokenizer/model versions, monitor text-quality KPIs (null rate, average length), and persist preprocessing configs in source control.

#### 12. Statistical Text Features

**Purpose**: Derive lightweight numerical descriptors that summarize textual structure.

**Techniques**: Length metrics (character/word/sentence counts, mean word length), lexical diversity (type-token ratio), punctuation density, readability indices (Flesch-Kincaid, Gunning Fog).

**Benefits**: Offers interpretable baselines, captures stylistic signals, and scales efficiently for large corpora.

**Requirements**: Catalog feature formulas, validate robustness across document lengths, and log computation scripts for reproducibility.

#### 13. TF-IDF Vectorization

**Purpose**: Encode token importance while balancing corpus-wide prevalence.

**Techniques**: Configurable n-gram ranges (1–3), max_features thresholds, min/max document frequency filters, sublinear TF scaling (log(1 + tf)).

**Benefits**: Proven baseline for many NLP tasks, balances sparsity with signal, adaptable to streaming updates.

**Requirements**: Register vectorizer artifacts in MLflow/Feature Store, document vocabulary size and n-gram settings, and define OOV handling strategy.

#### 14. Word Embeddings (Static)

**Purpose**: Map words into dense semantic spaces using pre-trained distributional models.

**Techniques**: Word2Vec or GloVe averaging, FastText for subword coverage, TF-IDF weighted pooling, domain-adapted embeddings via continued training.

**Benefits**: Captures synonymy/semantic proximity, reduces dimensionality, bootstraps from external corpora.

**Requirements**: Log embedding source, dimensionality, and coverage rate; track OOV fallback strategy; persist embedding weights alongside feature metadata.

#### 15. Contextual Embeddings (Transformers)

**Purpose**: Produce context-aware sentence or document representations leveraging transformer models.

**Techniques**: BERT/Sentence-BERT mean or CLS pooling, domain-specific checkpoints (FinBERT, BioBERT), adapter fine-tuning for efficiency, batch inference optimizations.

**Benefits**: Handles polysemy, captures long-range dependencies, drives SOTA performance on classification, similarity, and ranking tasks.

**Requirements**: Record model name/version, pooling strategy, and hardware footprint; monitor inference latency; register model artifacts in MLflow with lineage back to training data.

#### 16. Named Entity Recognition Features

**Purpose**: Surface domain entities as categorical and quantitative signals.

**Techniques**: spaCy or transformers-based NER, entity counts by type, entity-pair interactions, custom gazetteers for regulated vocabularies.

**Benefits**: Enhances interpretability, highlights key actors, supports compliance/audit workflows.

**Requirements**: Track NER model provenance, maintain entity taxonomies, validate precision/recall on domain benchmarks, and log entity extraction pipelines.

#### 17. Part-of-Speech and Syntactic Features

**Purpose**: Capture grammatical patterns indicative of intent, sentiment, or author traits.

**Techniques**: POS distribution ratios, dependency tree depth, noun/verb phrase counts, function-word frequency.

**Benefits**: Provides explainable signals, complements semantic embeddings, effective for authorship and sentiment tasks.

**Requirements**: Document parser/tagger versions, assert parsing accuracy on sampled corpora, and persist syntactic feature schemas.

#### 18. Sentiment and Emotion Scoring

**Purpose**: Quantify affective tone for customer feedback, compliance, or experience analytics.

**Techniques**: Rule-based sentiment (VADER), transformer sentiment classifiers, emotion taxonomies (joy/anger/fear/sadness), aspect-based sentiment tied to named entities.

**Benefits**: Links textual tone to business KPIs, supports churn detection, surfaces regulatory risk indicators.

**Requirements**: Register model calibration data, document score interpretation ranges, monitor drift across segments, and enforce audit trails for sentiment overrides.

#### 19. Topic Modeling and Theme Extraction

**Purpose**: Discover latent themes and associate documents with interpretable topics.

**Techniques**: LDA or NMF topic distributions, BERTopic leveraging transformer embeddings, dynamic topic updates for streaming corpora.

**Benefits**: Reduces dimensionality, aids exploratory analysis, supports routing and triage workflows.

**Requirements**: Document topic counts, coherence metrics (C_v), and top-term descriptors; log model refresh cadence.

#### 20. N-gram and Character Sequence Features

**Purpose**: Capture phraseology, term co-occurrence, and orthographic signals.

**Techniques**: Word n-grams with frequency thresholds, character n-grams for typo robustness, skip-grams, collocation scoring (PMI).

**Benefits**: Complements embeddings, detects idioms, resilient to spelling variance.

**Requirements**: Maintain vocabulary registries, validate memory footprint, and monitor rare n-gram sparsity over time.

#### 21. Text Similarity and Distance Metrics

**Purpose**: Measure semantic or lexical proximity across textual entities.

**Techniques**: Cosine similarity (TF-IDF or embeddings), Jaccard overlap, Levenshtein edit distance, semantic search via Sentence-BERT.

**Benefits**: Enables deduplication, recommendation, case routing, and anomaly detection.

**Requirements**: Document reference corpora, persist similarity thresholds, validate computational scalability, and expose lineage for stored embeddings.

### Feature Engineering Documentation Requirements

- ✔ **Feature metadata catalog**: Document technique applied, transformation parameters, source features, business rationale, expected range, training/inference considerations, performance impact, computational cost.

- ✔ **Feature importance tracking**: Train model (RandomForest/XGBoost), extract importances, log to MLflow, flag low-importance features (<0.001) for removal.

- ✔ **A/B testing for feature impact**: Baseline vs. new features, document lift in metrics (AUC, precision, recall), validate in production.

- ✔ **Language asset governance**: Record language, tokenizer, and embedding/transformer versions; track OOV rate, vocabulary drift, and multilingual coverage.

- ✔ **NLP compute observability**: Monitor inference latency, GPU/CPU utilization, and model footprint for vectorization/embedding stages with alerting on regressions.

- ✔ **Explainability for text features**: Generate token-level attributions (e.g., SHAP, LIME), archive highlighted text snippets, and provide steward-facing interpretation guides.

## III. Preferred Patterns (Recommended)

The LLM **should** aim for:

- ➜ **Reusable transformation libraries** modularized into shared packages with semantic versioning.
- ➜ **Automated schema evolution** workflows with approvals via Azure DevOps pipelines.
- ➜ **Scalable aggregation patterns** using window functions, incremental ETL, and Delta Live Tables when available.
- ➜ **Performance metrics** capturing compute cost, materialization duration, and job lineage metrics.
- ➜ **Business glossary integration** linking feature documentation to business KPIs and definitions.
- ➜ **Interactive notebooks** for feature explainability and data steward review prior to promotion.
- ➜ **Advanced validation suites** expanding feature tests to cover source freshness, schema drift, leakage/skew detection, and regression baselines with parameterized thresholds and automated alerting.
- ➜ **Lifecycle exit reviews** using stage-gate checklists to confirm Bronze debt items are resolved before Silver promotion and that Silver controls pass chaos/cost rehearsals prior to Gold.

---

**Version**: 2.1.0
**Last Updated**: 2025-11-17
**Changelog**:
- v2.1.0: Added Advanced NLP Feature Engineering section covering preprocessing, embeddings, sentiment, topics, similarity, and governance requirements
- v2.1.0: Expanded documentation controls to govern language assets, compute observability, and text explainability
- v2.0.0: Added hard-stop rule requiring advanced feature engineering sophistication (target encoding, polynomial interactions, embeddings)
- v2.0.0: Added comprehensive "Advanced Feature Engineering Techniques" section with 10 sophisticated methods
- v2.0.0: Condensed technique descriptions (removed verbose code examples, maintained technique summaries and benefits)
- v2.0.0: Added Target Encoding with Bayesian smoothing and regularization (prevents overfitting on rare categories)
- v2.0.0: Added Polynomial Feature Generation with selective feature engineering (avoids curse of dimensionality)
- v2.0.0: Added Intelligent Binning/Discretization (decision tree-based, quantile binning)
- v2.0.0: Added Time-Based Feature Extraction (lag features, rolling statistics, trend features, Fourier transforms)
- v2.0.0: Added Feature Interactions (ratio features, difference features, tree-extracted interactions)
- v2.0.0: Added Embedding Representations for high-cardinality categoricals (entity embeddings, pre-trained embeddings)
- v2.0.0: Added Feature Clustering (K-Means, DBSCAN with cluster membership and distance features)
- v2.0.0: Added Dimensionality Reduction as feature engineering (PCA, t-SNE)
- v2.0.0: Added Feature Selection with Mutual Information (captures non-linear dependencies)
- v2.0.0: Added Synthetic Feature Generation (feature crossing, domain-specific, automated tools)
- v2.0.0: Added Feature Engineering Documentation Requirements (metadata catalog, importance tracking, A/B testing)
