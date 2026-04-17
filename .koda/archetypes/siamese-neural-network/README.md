# Siamese Neural Network Archetype

## Overview
This archetype establishes guardrails for designing, training, and deploying Siamese and twin-tower metric-learning models.

## Core Principles
The following hard-stop rules must be strictly followed:
- **No entity leakage**: Enforce disjoint partitions for anchor/identity.
- **No unlabeled ground truth**: Do not promote heuristics without validation.
- **No PII embeddings**: Do not persist embeddings recovering protected attributes.
- **No loss-metric mismatch**: Online metric must match training loss.
- **No threshold-free launch**: Tune thresholds on regulated holdouts.

## Standard Pattern
Implementations must demonstrate:
- **Pair balance controls**: Implement stratified pair sampling.
- **Hard-negative mining**: Schedule iterative mining with safeguards.
- **Metric tracking**: Log ROC-AUC, precision@K to MLflow.
- **Distance alignment**: Align offline eval and online serving metrics.
- **Inference contracts**: Publish dimensionalities and normalization.
- **Fairness review**: Run bias checks before promotion.
