# Clustering ML Models Archetype

## Overview
This archetype establishes disciplined practices for unsupervised clustering on Databricks and similar platforms, focusing on responsible feature handling, reproducible workflows, and transparent cluster interpretation.

## Core Principles
The following hard-stop rules must be strictly followed:
- **Uses raw PII features**: Never include direct identifiers unless irreversibly tokenized/hashed.
- **Runs stochastic algorithms without seeding**: Deterministic seeding required for KMeans/GMM/etc.
- **Skips MLflow tracking**: Parameters, metrics, and artifacts must be logged.
- **Persists clusters to uncontrolled zones**: Do not write assignments to ungovened zones or overwrite curated assets without MERGE + lineage.
- **Drops features silently**: Log retained/excluded columns and rationale, including PCA/UMAP steps.

## Standard Pattern
Implementations must demonstrate:
- **Feature hygiene**: Null imputation, outlier handling, and scale normalization before vector assembly.
- **Cluster evaluation**: Silhouette and stability metrics per candidate k/epsilon/minPts logged to MLflow.
- **Hyperparameter sweeps**: Explore cluster counts, eps/minPts ranges, and init strategies under budget controls.
- **Explainability artifacts**: Profile clusters (top features, population share, drift checks) and publish summaries.

## Preferred Pattern
- **Auto-tuned initialization**: Favor k-means++/scalable seeding and guarded epsilon/minPts selection for DBSCAN/HDBSCAN.
