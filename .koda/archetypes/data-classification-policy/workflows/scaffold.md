---
description: Scaffold data classification governance framework with SPI/PII controls and compliance automation (Data Classification Policy)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-classification-policy --json ` and parse for CATALOG_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-classification-policy/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: data assets scope, classification requirements, compliance mandates (GDPR, CCPA, CPNI), access governance model, monitoring needs. Request clarification if incomplete.

### 4. Generate Classification Framework
Create: Data classification inventory (SPI/PII mapping, field-level tagging, owner assignment), automated classification engine (catalog integration, lineage propagation, CI/CD guardrails), access governance (Just-In-Time elevation, PAW requirements, approval workflows, ABAC policies), encryption controls (AES-256 at rest, TLS 1.2+ in transit, key management), data minimization (masking rules, tokenization, pseudonymization, synthetic data generation), retention policies (automated purge schedules, legal holds, archival procedures).

### 5. Generate Monitoring and Compliance
Implement: SIEM integration with DLP alerts, anomaly detection for access patterns, continuous compliance scanning, audit trail capture, breach response playbooks, policy drift detection, stakeholder compliance scorecards.

### 6. Add Recommendations
Include: privacy-by-design templates, secure analytics patterns, third-party assurance requirements, incident response procedures, compliance KPI tracking.

### 7. Validate and Report
Generate framework with documentation. Report completion.

## Error Handling
**Missing Classification**: Require explicit SPI/PII inventory before proceeding.
**Access Too Broad**: Enforce least privilege and JIT elevation.
**Encryption Gaps**: Validate encryption at rest and in transit.

## Examples
**Example 1**: `/scaffold-data-classification Create framework for customer data with PII controls` - Output: Complete governance with classification and access controls
**Example 2**: `/scaffold-data-classification Implement GDPR-compliant data governance` - Output: Framework with consent management and retention policies

## References
