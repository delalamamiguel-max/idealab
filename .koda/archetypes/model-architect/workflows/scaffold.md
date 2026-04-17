---
description: Scaffold reproducible model training pipeline with MLflow tracking, feature contracts, and CI integration (Model Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype model-architect --json ` and ensure ENV_VALID. Halt if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/model-architect/templates/env-config.yaml` for approved runtimes, registry targets, CI pipelines, and security scans

### 3. Parse Input
Extract from $ARGUMENTS: problem statement, target metric, feature set references, training data versions, runtime preferences, deployment target, governance timeline. Request missing details (feature store IDs, MLflow workspace, Azure DevOps project).

### 4. Validate Constraints
Enforce hard stops:
- ✘ Reject workflows lacking MLflow tracking for parameters/metrics/artifacts
- ✘ Block non-deterministic training without seeding/environment capture
- ✘ Refuse usage of features without version-locked contracts
- ✘ Require MLflow registry publication and stage management
- ✘ Demand fairness metric coverage where applicable
- ✘ Ensure supported runtime versions only
- ✘ Require CI pipeline with tests, linting, security scans

### 5. Generate Training Blueprint
Provide scaffold including:
- Parameterized training script/notebook (data version, hyperparameters, output path)
- Data prep module referencing feature store contracts and validation checks
- Experiment logging template capturing dataset versions, feature hashes, git SHA, environment packages
- Hyperparameter tuning workflow (Hyperopt/Optuna) with budget constraints
- Evaluation suite (train/validation/test metrics, calibration, fairness metrics)
- Artifact packaging instructions (MLflow signature, conda/pip env, inference scripts)
- Documentation skeleton summarizing objective, assumptions, limitations, acceptance criteria
- Azure DevOps pipeline definition with unit tests, style checks, static analysis, security scans

### 6. Recommended Enhancements
Suggest optional additions:
- Modular architecture separating data prep, training, evaluation, registration
- AutoML baseline comparison for benchmarking
- Distributed training guidance (TorchDistributor, Spark MLlib)
- Advanced diagnostics (SHAP feature importance, residual analysis, uplift metrics)
- Integration tests verifying end-to-end pipeline execution
- Promotion checklist aligning with stakeholder sign-offs

### 7. Validate and Report

## Error Handling
- Hard-stop triggered: Halt scaffold, cite violated clause, provide remediation plan
- Missing inputs: Request feature contracts, MLflow workspace, CI pipeline info; share example command
- Tooling gap: Flag absent MLflow access, feature store permissions, or CI templates; reference env-config onboarding
- Governance conflicts: Escalate if fairness or security requirements undefined

## Examples
- **Example 1**: `/scaffold-model Build churn prediction training pipeline with MLflow registry`
- **Example 2**: `/scaffold-model Create credit risk model training project with fairness metrics`
- **Example 3**: `/scaffold-model Prepare distributed training workflow for recommendation engine`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/model-architect/templates/env-config.yaml`
