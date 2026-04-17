---
description: Compare feature engineering approaches for compliance, performance, and reuse across candidate pipelines (Feature Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype feature-architect --json ` and require ENV_VALID. Stop if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/feature-architect/templates/env-config.yaml` for quality thresholds, feature store guidance, and lineage tooling

### 3. Parse Input
Extract from $ARGUMENTS: candidate pipelines/notebooks, comparison goals (point-in-time accuracy, compute cost, governance fit), deployment targets, privacy considerations. Request missing assets (feature store entries, lineage graphs, test reports).

### 4. Define Evaluation Dimensions
Assess alternatives on:
- Source validation coverage and freshness enforcement
- Temporal integrity and leakage risk
- Feature contract completeness and documentation quality
- Feature store registration status and metadata richness
- Privacy compliance (PII handling, hashing)
- Quality and skew monitoring maturity
- Versioning and lineage fidelity
- Performance/cost metrics and scalability
- Reusability, modularity, schema evolution readiness

### 5. Analyze Candidates
For each option:
- Score against evaluation dimensions with supporting evidence
- Highlight hard-stop violations (e.g., missing feature store, leakage, privacy breach)
- Note strengths/weaknesses for operational resilience and maintainability
- Estimate remediation effort to reach production readiness

### 6. Recommend Strategy
Provide ranked recommendation with:
- Preferred pipeline and justification tied to guardrail compliance
- Required remediation tasks for adoption (quality tests, metadata updates)
- Governance implications (approvals, documentation updates)
- Optional enhancements (modular libraries, DLT adoption, cost monitoring)

### 7. Summarize Findings

## Error Handling
- Missing context: Request pipeline artifacts, feature store IDs, SLA requirements; share sample command highlighting needed parameters
- Hard-stop triggered: Disqualify option, cite constitution clause, outline remediation before reconsideration
- Ambiguous priorities: Facilitate alignment on weighting (accuracy vs cost vs governance)
- Tooling gap: Flag absence of lineage or feature store tooling and reference env-config onboarding

## Examples
- **Example 1**: `/compare-feature Evaluate Delta Live Tables vs manual Spark job for churn features`
- **Example 2**: `/compare-feature Contrast marketing propensity feature pipelines across regions`
- **Example 3**: `/compare-feature Decide between nightly batch and streaming fraud features`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/feature-architect/templates/env-config.yaml`
