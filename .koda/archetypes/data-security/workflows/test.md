---
description: Validate data security controls for protection, detection, and compliance readiness (Data Security)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-security --json ` and parse for SECURITY_ENDPOINT, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-security/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: security framework location, test scope, acceptance criteria. Request clarification if incomplete.

### 4. Analyze Test Requirements
Identify testable security components: encryption, access controls, network security, threat detection, audit logging.

### 5. Generate Test Suite
Create comprehensive security tests: encryption validation, access control tests, penetration tests, vulnerability scans, compliance checks.

### 6. Add Recommendations
Include security testing best practices, continuous validation, red team exercises.

### 7. Validate and Report
Execute: `pytest tests/ --junitxml=results.xml --cov --cov-report=html`
Generate test report. Report completion.

## Error Handling
**Security Test Failures**: Document vulnerabilities and remediate immediately.
**Compliance Gaps**: Flag violations and provide remediation plan.

## Examples
**Example 1**: `/test-data-security Validate encryption and access controls` - Output: Security test suite with vulnerability assessment
**Example 2**: `/test-data-security Run penetration tests on data platform` - Output: Pen test results with remediation

## References
