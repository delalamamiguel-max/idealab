---
description: Compare model training strategies for reproducibility, performance, and governance readiness (Model Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype model-architect --json ` and require ENV_VALID. Stop if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/model-architect/templates/env-config.yaml` for runtime policies, registry expectations, and CI standards

### 3. Parse Input
Extract from $ARGUMENTS: candidate training approaches (frameworks, pipelines, architectures), performance goals, fairness constraints, runtime limitations, infrastructure budgets, promotion timelines. Request data sources, feature contract references, and MLflow experiments if missing.

### 4. Define Evaluation Criteria
Assess alternatives on:
- MLflow tracking completeness and registry integration
- Reproducibility (seed control, environment capture)
- Feature contract alignment and dependency on governed features
- Model performance vs baseline with statistical significance
- Fairness metric coverage and mitigation capability
- Artifact packaging quality and deployment readiness
- CI/CD integration (tests, linting, security scans)
- Cost, training efficiency, and scalability (distributed support)
- Documentation effort and governance overhead

### 5. Analyze Options
For each candidate:
- Score against criteria with evidence and MLflow results
- Flag hard-stop violations (missing tracking, unsupported runtime, fairness gaps)
- Summarize strengths/weaknesses (accuracy, speed, maintainability)
- Estimate remediation needed to meet guardrails

### 6. Recommend Path Forward
Provide recommendation:
- Preferred approach with rationale aligned to guardrails and business objectives
- Complementary benchmarking (AutoML baseline) if warranted
- Remediation plan for viable alternatives (CI integration, fairness tests)
- Governance actions (stakeholder reviews, documentation updates)

### 7. Summarize Decision

## Error Handling
- Missing context: Request MLflow experiments, feature contracts, runtime constraints; provide example command clarifying needed inputs
- Hard-stop triggered: Exclude option and cite constitution clause with remediation guidance
- Conflicting priorities: Facilitate discussion on accuracy vs reproducibility vs cost
- Tooling gap: Flag missing CI pipelines or registry access; reference env-config onboarding

## Examples
- **Example 1**: `/compare-model Evaluate LightGBM vs neural net for churn prediction`
- **Example 2**: `/compare-model Decide between Spark MLlib and PyTorch pipeline for recommendation engine`
- **Example 3**: `/compare-model Assess AutoML baseline vs bespoke model for credit risk`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/model-architect/templates/env-config.yaml`
