# clustering ML models Constitution

## Purpose

Establishes disciplined practices for unsupervised clustering on Databricks, ensuring responsible feature handling, reproducible workflows, and transparent cluster interpretation.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** any approach that:

- ✘ **Uses raw PII features**: Never include direct identifiers (SSN, phone, email, card numbers) in feature vectors unless irreversibly tokenized or hashed.
- ✘ **Runs stochastic algorithms without seeding**: Always apply deterministic `setSeed` (or equivalent) for KMeans, GaussianMixture, BisectingKMeans, approximate kNN initializations, and any randomized dimensionality reduction.
- ✘ **Skips MLflow tracking**: Do not propose clustering workflows that omit MLflow logging of parameters, metrics, artifacts, and code snapshot.
- ✘ **Persists clusters to uncontrolled zones**: Do not write cluster assignments to bronze/raw tables or overwrite curated assets without Delta `MERGE` + lineage metadata.
- ✘ **Drops features silently**: Refuse PCA/UMAP or aggressive feature filtering without explicit logging of retained/excluded columns and rationale.

## II. Mandatory Patterns (Must Apply)

The LLM **must** ensure:

- ✔ **Feature hygiene** with null imputation, outlier clipping, and scale normalization (e.g., `StandardScaler` or `MinMaxScaler`) prior to vector assembly.
- ✔ **Cluster evaluation** capturing silhouette score (and, when applicable, Davies-Bouldin or HDBSCAN stability) for each candidate `k` or epsilon/minPts grid, logged to MLflow.
- ✔ **Hyperparameter sweeps** using `CrossValidator`, `TrainValidationSplit`, or Hyperopt to explore cluster counts, epsilon/minPts ranges for DBSCAN-class algorithms, and initialization strategies under budget controls.
- ✔ **Explainability artifacts** that profile each cluster (top features, population percentages, drift checks) and publish summaries to Delta tables or markdown reports.
- ✔ **Model versioning** with semantic version tags in MLflow model registry, including cluster count, algorithm type, and feature set hash in model metadata.

## III. Preferred Patterns (Recommended)

The LLM **should** adopt:

- ➜ **Auto-tuned initialization** leveraging k-means++ or scalable k-means++ seeding for stability, and guardrails for selecting epsilon/minPts when evaluating DBSCAN/HDBSCAN.
- ➜ **Neighbor-aware insights** that surface exemplar members per cluster using kNN queries for explainability and downstream personalization.
- ➜ **Incremental refresh pipelines** that recompute centroids on sliding windows and monitor drift against historical centroids.
- ➜ **Visualization notebooks** with Databricks dashboards showcasing cluster scatter plots (PCA/TSNE) and interactive profiles.
- ➜ **Curated data layer alignment** sourcing standardized features from governed Delta Live Tables or approved data products referenced in `data-sourcing-specialist-constitution.md`.
- ➜ **Guarded inference jobs** using job cluster policies with table ACL checks and MFA-protected secrets scopes.

---

**Version**: 1.0.1
**Last Updated**: 2025-10-27
**Source**: Derived from Databricks clustering and ML governance best practices
