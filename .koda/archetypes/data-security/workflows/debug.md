---
description: Debug data security incidents, breaches, and vulnerability exposures (Data Security)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-security --json ` and parse for SECURITY_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-security/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: incident type, affected systems, threat indicators, timeline. Request clarification if incomplete.

### 4. Diagnose Issue
Check: access violations, encryption failures, network breaches, authentication bypasses, authorization gaps, data exfiltration, vulnerability exploits, configuration drift.

### 5. Generate Fix Recommendations
Provide fixes for identified security issues with immediate remediation steps and long-term preventions.

### 6. Add Prevention Measures
Recommend enhanced security controls, continuous monitoring, threat hunting, security hardening.

### 7. Validate and Report
Generate incident report. Report completion.

## Error Handling
**Active Breach**: Escalate immediately and initiate incident response.
**Data Exposure**: Contain, assess impact, notify stakeholders.

## Examples
**Example 1**: `/debug-data-security Unauthorized data access detected` - Output: Access analysis with remediation
**Example 2**: `/debug-data-security Encryption misconfiguration found` - Output: Configuration fix with validation

## References
