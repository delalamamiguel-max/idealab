# DBSCAN Model Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the DBSCAN clustering archetype.

**Source**: Consolidated from internal `ml/clustering/dbscan` guardrails and production retrospectives

## Model Description

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) groups points by locating regions of high sample density separated by sparse regions. It requires two primary hyperparameters: `eps`, the maximum neighborhood radius for points to be considered connected, and `min_samples`, the minimum number of neighbors needed to form a dense core point. Core points expand clusters by linking to directly reachable neighbors, while points that fail density checks are labeled as noise or border points. DBSCAN naturally discovers arbitrarily shaped clusters, resists outliers, and avoids specifying the number of clusters upfront, making it a strong fit for spatial, behavioral, and anomaly-heavy datasets when distance metrics and scaling are carefully governed.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** output that violates these rules:

- ✘ **No unscaled numeric features**: Do not fit or score DBSCAN on continuous features that have not been standardized or normalized to comparable ranges
- ✘ **No arbitrary epsilon**: Do not accept the default `eps` or any value lacking documented justification (e.g., k-distance curve, domain heuristic)
- ✘ **No under-sized neighborhoods**: Do not set `min_samples` lower than `max(3, n_features + 1)`
- ✘ **No mixed raw feature types**: Do not pass raw categorical/text columns without deterministic numeric encoding aligned with the distance metric
- ✘ **No silent null handling**: Do not drop or impute missing values without logging the strategy and affected record counts
- ✘ **No dark deployments**: Refuse promotion if telemetry pipelines for required clustering metrics are absent or disabled.

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

- ✔ **Feature preprocessing pipeline**: Apply explicit scaling/encoding steps (e.g., `StandardScaler`, `OneHotEncoder`) captured in a reproducible pipeline artifact
- ✔ **Parameter selection workflow**: Produce a parameter sweep or heuristic notebook that records the `eps`/`min_samples` selection rationale and stores plots in object storage
- ✔ **Cluster diagnostics**: Log silhouette-like density metrics, cluster size distribution, and noise ratio; fail the run when noise > 40% unless waived by config
- ✔ **Spatial indexing**: Ensure the implementation uses a `ball_tree`/`kd_tree` metric structure or approximate neighbor index for datasets exceeding 50k samples
- ✔ **Model card + lineage**: Emit a model card documenting feature set, preprocessing, hyperparameters, and evaluation artifacts, and persist lineage IDs alongside serialized models
- ✔ **Telemetry emission**: Stream the following metrics to the observability platform each run: `cluster_count`, `noise_ratio`, `avg_cluster_density`, `eps`, `min_samples`, processing latency, input record counts, and drift indicators; align exporters with `observability-constitution.md`.

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Dimensionality reduction first**: Apply PCA/UMAP to reduce high-dimensional spaces (>30 features) before clustering
- ➜ **Adaptive eps grid**: Start with HDBSCAN or adaptive epsilon search to stabilize clusters under data drift
- ➜ **Visualization package**: Provide optional 2D/3D embeddings with labeled noise/outliers for exploratory dashboards
- ➜ **Drift monitoring**: Schedule periodic re-computation of neighbor distance histograms to detect density shifts
- ➜ **Resource-aware batching**: Chunk scoring jobs to keep memory usage below 70% of cluster limits and parallelize via joblib/Dask when available
- ➜ **Unified dashboards**: Attach DBSCAN telemetry panels (metric trends, anomaly counts, failure alerts) to the service’s golden observability dashboard.

---

**Version**: 1.1.0
**Last Updated**: 2025-10-27
**Source**: `/Users/yc010e/Documents/Projects/pythonProject/apm0013448-aifc-ds/vibe_cdo-windsurf-integration/.cdo-aifc/memory/archetypes/dbscan-model-constitution.md`
