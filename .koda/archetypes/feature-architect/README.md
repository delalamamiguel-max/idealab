# Feature Architect Archetype

## Overview
This archetype defines the guardrails for producing reusable, high-quality features with reproducible lineage across Databricks Feature Store, Feast, and downstream ML consumers.

## Core Principles
The following hard-stop rules must be strictly followed:
- **Skips source validation**: Never engineer features without validating raw input.
- **Breaks feature contract**: Do not publish features lacking documentation.
- **Violates temporal integrity**: No target leakage via future data.
- **Bypasses feature store**: Do not deliver features outside the governed store.
- **Ignores privacy policies**: Do not include PII without tokenization.
- **Uses non-deterministic transforms**: Avoid random operations without seeding.
- **Fails to version**: Never overwrite feature tables without versioning.

## Standard Pattern
Implementations must demonstrate:
- **Point-in-time correctness**: Enforced via time-travel joins.
- **Feature quality tests**: Verifying null rates and monotonicity.
- **Metadata registration**: Storing description and lineage.
- **Automated documentation**: Generating markdown summaries.
- **Training-serving skew detection**: Comparing distributions.
