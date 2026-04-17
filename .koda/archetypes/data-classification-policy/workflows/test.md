---
description: Test Responsible AI assessment package for policy compliance, monitoring readiness, and governance completeness (Data Classification Policy)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-classification-policy --json ` and parse for CATALOG_ENDPOINT, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-classification-policy/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: framework location, test scope (classification, access, encryption, compliance, monitoring), acceptance criteria. Request clarification if incomplete.

### 4. Analyze Test Requirements
Identify components: classification accuracy (tagging correctness, owner documentation, catalog integration), access controls (least privilege, JIT enforcement, PAW compliance, ABAC rules), encryption (at rest/transit validation, log scrubbing, key rotation), compliance (consent documentation, retention adherence, DPA validation, breach response), monitoring (DLP coverage, SIEM integration, audit completeness).

### 5. Generate Test Suite
Create: unit tests (classification rules, access policies, encryption validation), integration tests (end-to-end data access, catalog synchronization, SIEM alerting), compliance tests (GDPR/CCPA requirements, consent workflows, retention enforcement), security tests (penetration testing, vulnerability scanning, breach simulation), monitoring tests (DLP alert validation, anomaly detection, audit trail completeness).

### 6. Add Recommendations
Include: automated compliance scanning, continuous access reviews, encryption validation, policy drift detection, incident response drills.

### 7. Validate and Report
Execute: `pytest tests/ --junitxml=results.xml --cov --cov-report=html`
Generate test report. Report completion.

## Error Handling
**Test Data Contains PII**: Use synthetic data or properly masked datasets.
**Compliance Checks Fail**: Document violations and remediation plan.

## Examples
**Example 1**: `/test-data-classification Validate PII classification and access controls` - Output: Complete test suite with compliance validation
**Example 2**: `/test-data-classification Test GDPR compliance framework` - Output: Compliance test suite with consent and retention checks

## References
