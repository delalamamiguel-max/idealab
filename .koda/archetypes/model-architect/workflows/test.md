---
description: Validate model training pipeline for reproducibility, fairness, and promotion readiness (Model Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype model-architect --json ` and confirm ENV_VALID. Abort if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/model-architect/templates/env-config.yaml` for runtime policies, CI templates, and security tooling

### 3. Parse Input
Extract from $ARGUMENTS: training pipeline path, target environment, metrics and thresholds, fairness requirements, registry stage, CI pipeline identifier. Request MLflow run IDs, feature contracts, and test configs if missing.

### 4. Plan Test Coverage
Include validations for:
- MLflow logging completeness (parameters, metrics, artifacts, code snapshot)
- Reproducibility (seeds, environment capture, dependency lockfiles)
- Feature contract adherence and version alignment
- Dataset integrity (train/validation/test splits, leakage checks)
- Model evaluation metrics with confidence intervals and calibration
- Fairness metrics for applicable cohorts with thresholds
- Artifact packaging (signature, schema, conda/pip files)
- Security scanning results (pip-audit, safety)
- CI pipeline execution (unit tests, style checks, static analysis)
- Documentation completeness and promotion checklist compliance

### 5. Execute Tests
Outline steps:
- Run automated unit/integration tests via Azure DevOps
- Reproduce training run in clean environment to verify determinism
- Execute fairness and calibration notebooks, log results to MLflow
- Run security scans on dependencies and review findings
- Validate packaging (MLflow `pyfunc` load, schema enforcement)
- Generate test report summarizing outcomes and attach evidence

### 6. Evaluate Results
Summarize pass/fail status:
- Highlight hard-stop violations blocking promotion
- Provide remediation backlog with owners and due dates
- Update MLflow tags and CI badges to reflect validation status
- Notify governance board of readiness or outstanding issues

### 7. Guardrail Verification

## Error Handling
- Missing artifacts: Request MLflow run, test report, feature contract; include example command clarifying expectations
- Hard-stop breach: Block promotion, cite constitution clause, outline remediation before retest
- Tooling gap: Flag absent CI pipeline or security scanner; reference env-config onboarding
- Governance dependency: Escalate if fairness or documentation approvals incomplete

## Examples
- **Example 1**: `/test-model Validate churn training pipeline before registry promotion`
- **Example 2**: `/test-model Run fairness and reproducibility checks for credit risk model`
- **Example 3**: `/test-model Execute CI validation suite for recommendation training project`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/model-architect/templates/env-config.yaml`
