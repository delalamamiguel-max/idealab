---
description: Compare data security approaches, encryption methods, and access control models (Data Security)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-security --json ` and parse for SECURITY_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-security/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type, candidate options, evaluation criteria. Request clarification if incomplete.

### 4. Generate Comparison Framework
Evaluate security approaches, encryption methods, access models, threat detection solutions.

### 5. Create Comparison Matrix
Generate detailed comparison with security effectiveness, cost, complexity, compliance fit.

### 6. Add Recommendations
Recommend approach with security justification and implementation guidance.

### 7. Validate and Report
Generate report. Report completion.

## Error Handling
**Insufficient Context**: Request threat model and compliance requirements.
**Security Trade-offs**: Document risks and mitigations.

## Examples
**Example 1**: `/compare-data-security RBAC vs ABAC for data access` - Output: Access model comparison with security analysis
**Example 2**: `/compare-data-security Encryption key management solutions` - Output: Key management comparison

## References
