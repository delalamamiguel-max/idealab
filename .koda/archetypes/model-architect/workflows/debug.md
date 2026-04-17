---
description: Diagnose model training failures and restore reproducibility, compliance, and registry readiness (Model Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype model-architect --json ` and require ENV_VALID. Stop if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/model-architect/templates/env-config.yaml` for approved runtimes, CI hooks, and security tooling

### 3. Parse Input
Collect from $ARGUMENTS: training run identifier, failure symptom (metric drift, registry rejection, CI failure), environment, recent changes, impacted stakeholders. Request MLflow run link, logs, feature contracts, and pipeline outputs if absent.

### 4. Reproduce Issue
Investigate by:
- Reviewing MLflow logs for missing parameters/metrics/artifacts
- Checking reproducibility (seeds, environment capture, package list)
- Validating feature contracts and ensuring version alignment
- Inspecting fairness metrics vs policy thresholds
- Examining runtime versions for compliance
- Analyzing CI logs for failing unit tests, linting, security scans
- Reviewing artifact packaging (signature, conda/pip files)
- Checking documentation completeness and promotion checklist items

### 5. Apply Fixes
Recommend remediation:
- Patch training scripts to log full MLflow metadata and artifacts
- Set deterministic seeds and capture environment snapshot in requirements file
- Align feature references with feature store contracts and update metadata
- Regenerate fairness metrics and document mitigations if needed
- Update dependency management to approved runtime versions
- Fix failing unit/integration tests, lint issues, or security findings
- Rebuild MLflow model package with signature and dependency files
- Update documentation and promotion checklist entries

### 6. Prevent Recurrence
Propose safeguards:
- Add pre-commit hooks enforcing MLflow logging conventions
- Automate CI gates for feature contract drift detection
- Schedule fairness metric monitoring and alerts
- Introduce AutoML benchmark comparison for drift detection
- Maintain knowledge base of recurring issues and resolutions

### 7. Validate and Report

## Error Handling
- Missing evidence: Request MLflow run, feature contract, CI logs; provide example command listing required inputs
- Hard-stop unresolved: Refuse continuation until MLflow tracking, reproducibility, or fairness compliance restored
- Tooling outage: Escalate if MLflow or CI services unavailable; reference env-config contingency plan
- Governance escalation: Notify compliance if policy thresholds exceeded without mitigation plan

## Examples
- **Example 1**: `/debug-model MLflow promotion blocked due to missing artifacts`
- **Example 2**: `/debug-model Training run not reproducible across environments`
- **Example 3**: `/debug-model CI pipeline failing on security scan for dependencies`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/model-architect/templates/env-config.yaml`
