---
description: Refactor feature pipelines to restore contracts, temporal integrity, and feature store compliance (Feature Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype feature-architect --json ` and ensure ENV_VALID. Abort if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/feature-architect/templates/env-config.yaml` for store settings, lineage tooling, and quality thresholds

### 3. Parse Input
Extract from $ARGUMENTS: feature pipeline path, observed issues (leakage, missing metadata, quality failures), target consumers, compliance deadlines. Request notebook/scripts, feature store entries, and lineage reports if missing.

### 4. Assess Current Implementation
Review for:
- Missing source validation or freshness checks
- Broken feature contracts (types, ranges, owner metadata)
- Temporal leakage via future joins or misaligned windows
- Features published outside governed store or without registration metadata
- PII exposure without hashing/tokenization
- Non-deterministic transforms lacking seeds
- Absent versioning or audit logs
- Gaps in quality tests, skew detection, unit tests

### 5. Design Refactor
Recommend updates:
- Introduce standardized source validation module and freshness SLA enforcement
- Rebuild point-in-time joins with `as_of_ts` patterns and time-travel queries
- Regenerate feature contracts with owner, description, allowed ranges, lineage
- Register or update entries in feature store with tags and governance attributes
- Implement privacy-preserving transforms and encrypt/hide PII per policy
- Seed random operations and document reproducibility steps
- Add comprehensive quality tests and skew monitoring jobs
- Version control materializations (Delta history, MLflow artifacts)

### 6. Future-Proofing
Suggest enhancements:
- Modular transformation package with semantic releases
- Azure DevOps pipeline for schema evolution approvals
- Delta Live Tables or incremental processing setup
- Cost and performance dashboards for materialization jobs
- Business glossary integration and automated documentation exports
- Reusable unit test templates shared across squads

### 7. Validate and Report

## Error Handling
- Persistent hard-stop: Halt assistance until temporal leakage, privacy breaches, or missing contracts resolved
- Evidence gap: Request feature store entry, job configs, lineage graphs; share example command for context
- Tooling mismatch: Flag absent Purview/Unity connectors or feature store permissions and point to env-config guidance
- Compliance deadline risk: Escalate to steward if remediation timeline jeopardizes obligations

## Examples
- **Example 1**: `/refactor-feature Harden churn features with point-in-time joins and skew monitoring`
- **Example 2**: `/refactor-feature Restore feature contracts and metadata for marketing propensity set`
- **Example 3**: `/refactor-feature Move legacy fraud features into governed feature store with lineage`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/feature-architect/templates/env-config.yaml`
