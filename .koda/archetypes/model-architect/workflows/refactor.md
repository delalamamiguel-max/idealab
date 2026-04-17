---
description: Refactor model training workflow to restore reproducibility, registry compliance, and CI coverage (Model Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype model-architect --json ` and confirm ENV_VALID. Abort if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/model-architect/templates/env-config.yaml` for approved runtimes, CI templates, and security tooling

### 3. Parse Input
Extract from $ARGUMENTS: existing training asset path, pain points (missing MLflow logs, non-determinism, failing CI), deployment goals, deadlines. Request feature contracts, MLflow runs, and pipeline logs if missing.

### 4. Assess Current Pipeline
Review for:
- Absent or incomplete MLflow tracking (parameters, metrics, artifacts, code snapshot)
- Non-deterministic behavior (no seeds, undocumented environment)
- Missing feature contract references or version locks
- Unregistered models or unmanaged artifacts
- Missing fairness metrics or policy compliance checks
- Unsupported runtime usage
- Gaps in CI/CD (missing unit tests, linting, security scans)
- Insufficient documentation of objectives, assumptions, and limitations

### 5. Define Refactor Actions
Recommend updates:
- Instrument MLflow logging for all training runs and artifacts
- Enforce deterministic seeds, capture environment specs, log git SHA
- Bind feature access to governed contracts and versioned snapshots
- Automate registration to MLflow Model Registry with stage management
- Add fairness evaluation module and document results
- Align runtime dependencies with approved versions; capture via conda/pip files
- Expand CI pipeline with unit/integration tests, style checks, static analysis, security scans
- Update documentation with objective, limitations, acceptance criteria

### 6. Strengthen Architecture
Suggest enhancements:
- Modularize pipeline components for reuse and testing
- Introduce hyperparameter tuning orchestrator with budget guardrails
- Add AutoML benchmark comparison for context
- Implement advanced diagnostics (SHAP, residual analysis)
- Create promotion checklist requiring stakeholder sign-offs

### 7. Validate and Report

## Error Handling
- Hard-stop unresolved: Halt support until MLflow tracking, feature contracts, or CI coverage restored
- Missing evidence: Request notebooks, MLflow runs, feature store IDs; share example command clarifying inputs
- Tooling mismatch: Flag absence of MLflow permissions or CI pipeline access; reference env-config onboarding
- Governance block: Escalate if fairness or security requirements cannot be met

## Examples
- **Example 1**: `/refactor-model Update churn training notebook lacking MLflow logging`
- **Example 2**: `/refactor-model Harden credit risk pipeline failing CI security scans`
- **Example 3**: `/refactor-model Align recommendation training with feature store contracts`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/model-architect/templates/env-config.yaml`
