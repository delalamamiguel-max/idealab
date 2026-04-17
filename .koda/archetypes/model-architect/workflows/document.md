---
description: Package model training documentation, MLflow evidence, and promotion checklist artifacts (Model Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype model-architect --json ` and ensure ENV_VALID. Stop if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/model-architect/templates/env-config.yaml` for templates, registry settings, and CI evidence paths

### 3. Parse Input
Extract from $ARGUMENTS: model version, intended stage promotion, stakeholders, required artifacts (design doc, evaluation report, fairness analysis, CI logs), approval deadlines. Request MLflow run links, feature contracts, and pipeline outputs if missing.

### 4. Assemble Core Artifacts
Include in package:
- Model objective summary with assumptions, limitations, and acceptance criteria
- Feature contract references and data provenance details
- Training configuration (hyperparameters, seeds, runtime environment)
- Evaluation results across train/validation/test with confidence intervals and calibration
- Fairness metrics and mitigation plan for protected attributes
- MLflow artifact index (run IDs, code snapshot, data versions, environment files)
- Security scan results and dependency lockfiles
- CI/CD evidence (unit/integration test logs, lint reports)
- Promotion checklist with stakeholder sign-offs

### 5. Tailor Deliverables
Produce outputs for:
- Governance review packet (PDF/HTML) consolidating evidence and approvals
- Technical appendix (notebooks, scripts, configuration files)
- Executive summary (key metrics, business impact, risk outlook)
- Knowledge base entry linking to MLflow experiments and feature documentation

### 6. Quality Checks
- Verify reproducibility artifacts (requirements files, seeds) present and tested
- Ensure documentation references MLflow and feature store records
- Confirm PII absent or appropriately masked in materials
- Store artifacts in governed repository with retention metadata
- Trigger stakeholder notification and approval workflow in Azure DevOps

### 7. Guardrail Validation

## Error Handling
- Missing materials: Request evaluation report, MLflow run, CI logs; include example command specifying expectations
- Hard-stop unmet: Refuse publication until MLflow tracking, reproducibility, or fairness documentation complete
- Storage conflict: Direct to approved repositories per env-config guidance
- Approval ambiguity: Ask for stakeholder list and required sign-off order

## Examples
- **Example 1**: `/document-model Prepare promotion packet for churn prediction model`
- **Example 2**: `/document-model Package training evidence for credit risk governance review`
- **Example 3**: `/document-model Update knowledge base entry for recommendation engine model`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/model-architect/templates/env-config.yaml`
