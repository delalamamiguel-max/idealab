# Collaborative Filtering Model Archetype

## Overview
This archetype establishes governance for collaborative filtering recommenders, ensuring safe identity handling, rigorous experimentation, and lifecycle automation.

## Core Principles
The following hard-stop rules must be strictly followed:
- **Violates identity governance**: Never blend raw PII or unhashed IDs.
- **Skips control comparisons**: Require offline baselines and online A/B tests.
- **Deploys with cold-start gaps**: Mitigation plans needed for new users/items.
- **Masks biased outcomes**: Block models breaching fairness thresholds.
- **Bypasses data lineage**: Training must link MLflow run IDs and dataset versions.
- **Ignores negative feedback**: Capture and honor suppression/opt-out signals.
- **Circumvents approvals**: Azure DevOps sign-offs and stakeholder notification required.

## Standard Pattern
Implementations must demonstrate:
- **Experiment charter**: Hypothesis, segments, inventory scope, KPIs.
- **Reproducible sampling**: Stratified or time-aware splits with seeds.
- **Evaluation suite**: Precision@k, recall@k, NDCG, MAP, coverage, impact deltas.
- **Hybrid validation**: Replay simulations plus production telemetry.
- **Bias and safety diagnostics**: Disparate impact and sensitive catalog checks.
- **Feedback ingestion loop**: Capture clicks/skips/dwell/complaints into governed tables.
- **Lifecycle automation**: Push reports/configs to Azure DevOps and MLflow artifacts.
- **Incident response plan**: Rollback playlists and fallbacks when KPIs regress.
