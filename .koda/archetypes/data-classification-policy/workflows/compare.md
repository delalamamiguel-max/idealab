---
description: Compare Responsible AI strategies, governance patterns, and mitigation options for ethical risk management (Data Classification Policy)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-classification-policy --json ` and parse for CATALOG_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-classification-policy/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type (classification tools, access models, encryption approaches, compliance frameworks), candidate options, evaluation criteria. Request clarification if incomplete.

### 4. Generate Comparison Framework
Evaluate: classification tools (automated vs manual, catalog options, lineage tracking), access models (RBAC vs ABAC, JIT mechanisms, PAW implementations), encryption approaches (key management, encryption at rest/transit, secure enclaves), compliance frameworks (GDPR vs CCPA vs CPNI, consent management, retention strategies).

### 5. Create Comparison Matrix
Generate with metrics (coverage, automation level, compliance fit, cost), assessments (complexity, adoption effort, vendor lock-in), trade-off analysis, recommendations.

### 6. Add Recommendations
Recommend with justification: compliance alignment, security posture, operational feasibility, cost-benefit, migration path.

### 7. Validate and Report
Generate comparison report. Report completion.

## Error Handling
**Insufficient Context**: Request compliance requirements and risk tolerance.
**Unclear Requirements**: Facilitate requirements gathering.

## Examples
**Example 1**: `/compare-data-classification RBAC vs ABAC for SPI/PII access` - Output: Access model comparison with security analysis
**Example 2**: `/compare-data-classification GDPR vs CCPA compliance approaches` - Output: Framework comparison with implementation guidance

## References
