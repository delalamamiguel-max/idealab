---
description: Refactor data security controls to strengthen protection and compliance (Data Security)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-security --json ` and parse for SECURITY_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-security/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: security framework location, refactoring goals, specific vulnerabilities. Request clarification if incomplete.

### 4. Analyze Current State
Assess security posture, identify gaps, evaluate threat coverage, review compliance alignment.

### 5. Generate Refactoring Plan
Create improvements for encryption, access controls, network security, monitoring, incident response.

### 6. Implement Refactorings
Generate enhanced security controls with updated configurations and documentation.

### 7. Validate and Report
Generate report. Report completion.

## Error Handling
**Breaking Changes**: Plan careful migration with security validation.
**Compliance Impact**: Coordinate with security and compliance teams.

## Examples
**Example 1**: `/refactor-data-security Implement zero-trust architecture` - Output: Enhanced security with zero-trust controls
**Example 2**: `/refactor-data-security Strengthen encryption and key management` - Output: Improved encryption with rotation

## References
