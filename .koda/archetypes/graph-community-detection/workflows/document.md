---
description: Package graph community detection documentation, governance evidence, and stakeholder briefs (Graph Community Detection)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype graph-community-detection --json ` and confirm ENV_VALID. Stop if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/graph-community-detection/templates/env-config.yaml` for templates, storage locations, and approval flows

### 3. Parse Input
Extract from $ARGUMENTS: project identifier, target audiences (operations, compliance, leadership), required deliverables (experiment log, fairness report, visualization pack), confidentiality level, publishing channels, approval deadlines. Request MLflow runs, benchmark reports, and monitoring dashboards if missing.

### 4. Assemble Core Artifacts
Include:
- Graph data contract with schema, lineage, retention, and owners
- Engine selection rationale with benchmark evidence and scale limits
- Algorithm summary (method, parameters, performance metrics, limitations)
- MLflow experiment log links and key artifacts (plots, metrics, configs)
- Privacy safeguards documentation (masking, aggregation, differential privacy)
- Fairness and harm assessment results with mitigation plan
- Explainability package (central nodes, bridging edges, visualizations, narratives)
- Operational runbook excerpt (refresh cadence, monitoring thresholds, rollback procedures)
- Integration checklist and SLA confirmations for downstream systems

### 5. Tailor Deliverables
Produce audience-specific outputs:
- Compliance dossier consolidating governance evidence and approvals
- Executive brief highlighting insights, business impact, risks, and actions
- Technical appendix with notebooks, scripts, configuration files, and deterministic seeds
- Visualization gallery or interactive dashboard references with access controls

### 6. Quality Checks
- Verify PII removal and secure storage of artifacts
- Ensure accessibility (alt text, high-contrast palettes) for visuals
- Confirm documentation stored in governed repository with retention metadata
- Log approvals and notify stakeholders via designated channels

### 7. Guardrail Verification

## Error Handling
- Missing materials: Request MLflow run, benchmark report, fairness artifacts; provide example command clarifying expectations
- Hard-stop unmet: Refuse delivery until privacy, fairness, or monitoring evidence complete
- Storage conflict: Direct to approved repositories per env-config guidance
- Audience ambiguity: Ask for distribution list and tailoring requirements

## Examples
- **Example 1**: `/document-graph-community Publish compliance packet for fraud ring community detection`
- **Example 2**: `/document-graph-community Deliver executive summary on customer community shifts`
- **Example 3**: `/document-graph-community Archive RelationalAI community pipeline evidence`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/graph-community-detection/templates/env-config.yaml`
