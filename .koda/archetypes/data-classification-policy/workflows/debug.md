---
description: Debug data classification violations, access breaches, and compliance failures (Data Classification Policy)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-classification-policy --json ` and parse for CATALOG_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-classification-policy/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: violation type (unclassified data, access breach, encryption gap, retention violation), alert details, affected assets, timestamps. Request clarification if incomplete.

### 4. Diagnose Issue
Check: classification gaps (untagged SPI/PII, missing owner approval, incorrect classification), access violations (excessive permissions, missing JIT, unauthorized access patterns), encryption failures (unencrypted at rest/transit, exposed in logs/caches), compliance breaches (consent violations, retention overruns, DPA gaps), monitoring gaps (missing DLP alerts, audit trail incomplete).

### 5. Generate Fix Recommendations
Provide fixes: for classification (apply tags, document ownership, update catalog), for access (revoke excess permissions, implement JIT, add approval workflow), for encryption (enable encryption, remove from logs, secure caches), for compliance (document consent, implement retention, update DPAs), for monitoring (configure SIEM, enhance audit logging).

### 6. Add Prevention Measures
Recommend: automated classification scanning, continuous access reviews, encryption validation, compliance monitoring, policy drift detection.

### 7. Validate and Report
Generate debug report. Report completion.

## Error Handling
**Critical Breach**: Escalate immediately per incident response playbook.
**Compliance Violation**: Coordinate with legal and compliance teams.

## Examples
**Example 1**: `/debug-data-classification Unencrypted PII found in logs` - Output: Encryption remediation with log scrubbing
**Example 2**: `/debug-data-classification Unauthorized access to SPI data detected` - Output: Access revocation with audit analysis

## References
