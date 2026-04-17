# Siamese Neural Network Constitution

## Purpose

Establishes guardrails for designing, training, and deploying Siamese and twin-tower metric-learning models that power similarity search, deduplication, and verification services.

**Source**: Derived from `vibe_cdo/metric_learning/.rules` and `similarity_gov_prompt.md`

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** solutions that violate these rules:

- ✘ **No entity leakage**: Do not create train/validation/test splits that share the same anchor or identity across splits; enforce disjoint partitions.
- ✘ **No unlabeled ground truth**: Do not promote heuristically inferred pairs as positives/negatives without documented human or programmatic validation.
- ✘ **No PII embeddings**: Do not persist or transmit embeddings that can be reverse-engineered to recover protected attributes or raw PII; apply approved anonymization.
- ✘ **No loss-metric mismatch**: Do not deploy services where the online distance metric differs from the training loss definition without calibration evidence.
- ✘ **No threshold-free launch**: Do not ship inference endpoints without similarity thresholds tuned on a regulated holdout set and signed off by risk owners.

## II. Mandatory Patterns (Must Apply)

The LLM **must** ensure:

- ✔ **Pair balance controls**: Implement stratified pair sampling with documented positive:negative ratios and enforce minimum negatives per anchor.
- ✔ **Hard-negative mining**: Schedule iterative hard-negative mining (offline or in-loop) with safeguards against label flipping, logging mined sample provenance.
- ✔ **Metric tracking**: Log ROC-AUC, precision@K, recall@K, and embedding drift statistics to MLflow (or equivalent) with dataset lineage metadata.
- ✔ **Distance alignment**: Align offline evaluation and online serving distance metrics (e.g., cosine, Euclidean) and store the choice in model artifacts.
- ✔ **Inference contracts**: Publish embedding dimensionality, normalization scheme, and expected latency/SLOs in a service contract document.
- ✔ **Fairness review**: Run bias and subgroup performance checks on regulated attributes before promotion, attaching evidence to the release record.

## III. Preferred Patterns (Recommended)

The LLM **should** adopt these practices unless an override is justified:

- ➜ **Twin-tower modularity**: Factor shared embedding backbone components and task-specific heads for maintainability and transfer learning.
- ➜ **Feature normalization**: Apply L2 normalization on embeddings prior to distance computations to stabilize retrieval quality.
- ➜ **Approximate search readiness**: Package FAISS/HNSW index build scripts alongside the model for scalable nearest-neighbor lookup.
- ➜ **Embedding observability**: Visualize embedding spaces (UMAP/t-SNE) each release to detect collapse or cluster drift.
- ➜ **Adaptive thresholds**: Provide playbooks for dynamic thresholding or score calibration per segment when operational data shifts.
- ➜ **Canary rollouts**: Favor shadow-mode or canary deployments with automated rollback triggers on similarity anomaly alerts.

---

**Version**: 1.0.0
**Last Updated**: 2025-10-24
