---
description: Design governed neural network architecture, configs, and experiment plan (Neural Network Model)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Verification
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype neural-network-model --json ` and capture `ENV_VALID`, tool versions, and unset required variables. Stop immediately if `ENV_VALID` is false and enumerate remediation steps.

### 2. Governance Context
- The constitution rules are already loaded in context above.
- Inspect `${ARCHETYPES_BASEDIR}/neural-network-model/templates/env-config.yaml` to align tooling, tracking defaults, and SLA targets
- Load `${DATASET_MANIFEST_PATH}` when present to understand lineage, schema, and PII flags

### 3. Requirements Analysis
Parse $ARGUMENTS for: problem framing (classification/regression/generation), dataset identifiers, latency/SLA targets, fairness metrics of interest, hardware constraints, and compliance checkpoints. Ask for missing critical details (e.g., protected attributes, baseline run IDs).

### 4. Guardrail Pre-checks
Ensure plan honors hard-stops:
- ✘ Reject use of unverified datasets or missing rights documentation
- ✘ Reject experiments without explicit seeds and MLflow tracking metadata
- ✘ Reject architectures lacking gradient clipping, NaN guards, or alerting hooks
- ✘ Reject omissions of fairness evaluation against last approved baseline
If any guardrail fails, respond with violation rationale and compliant alternatives.

### 5. Deliverable Construction
Produce:
- Architecture blueprint summarizing feature extraction, backbone, heads, and rationale tied to requirements
- Experiment configuration (YAML/JSON) encoding hyperparameters, seed values, data splits, optimizer schedule, gradient controls, callbacks, logging destinations
- Runbook outlining training phases (warm-up, steady-state, evaluation), monitoring checks (loss plateau, gradient norms), and rollback criteria
Annotate how each element maps to governance controls and env expectations.

### 6. Risk & Dependency Callouts
Highlight data quality assumptions, hardware needs, open compliance tasks (e.g., ethics sign-off), and integration points (feature store, model registry naming, alerting webhooks).

### 7. Validation & Reporting

## Error Handling

**Missing Governance Inputs**: Request dataset manifest location, fairness baseline metrics, or security approvals before proceeding.

**Environment Gaps**: Report absent `poetry`, `databricks`, or required env vars; provide install/export guidance.

**Hard-Stop Conflicts**: Explain violation (e.g., unspecified seeds) and supply compliant template snippets.

## Examples

**Vision Classifier Kickoff**: `/scaffold-neural-model Build ResNet-based defect classifier on uc://factory/vision, latency <40ms, monitor equal opportunity`
Output: Blueprint selecting EfficientNet backbone, YAML config with seeds/logging, monitoring plan referencing PSI drift jobs.

**NLP Intent Model**: `/scaffold-neural-model Design multilingual transformer for ATT chatbot, fairness relative to 2025Q2 baseline`
Output: Architecture comparing DeBERTa vs. distilled variants, config with multilingual tokenization, fairness metric commitments.

## References

Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/neural-network-model/templates/env-config.yaml`
