---
description: Generate comprehensive documentation for data security architecture and controls (Data Security)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-security --json ` and parse for SECURITY_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-security/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: security framework location, target audience, documentation scope. Request clarification if incomplete.

### 4. Analyze Security Architecture
Extract security controls, configurations, monitoring, incident procedures.

### 5. Generate Documentation Package
Create: Security Architecture, Access Control Guide, Encryption Documentation, Threat Response Runbook, Compliance Documentation.

### 6. Add Recommendations
Include security maintenance procedures, review schedules, continuous improvement.

### 7. Validate and Report
Generate documentation. Report completion.

## Error Handling
**Incomplete Information**: Request security architecture and configuration details.
**Missing Diagrams**: Generate from security configurations.

## Examples
**Example 1**: `/document-data-security Create security documentation package` - Output: Complete security docs with architecture and runbooks
**Example 2**: `/document-data-security Generate compliance security documentation` - Output: Compliance-focused security documentation

## References
