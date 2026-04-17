---
description: Document Responsible AI assessment outcomes, decisions, and monitoring commitments (Data Classification Policy)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-classification-policy --json ` and parse for CATALOG_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-classification-policy/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: framework location, target audience (data owners, compliance, security, leadership), documentation scope. Request clarification if incomplete.

### 4. Analyze Classification Framework
Extract: data inventory (classified assets, SPI/PII catalog, ownership), access controls (RBAC/ABAC policies, JIT procedures, PAW requirements), encryption (at rest/transit configurations, key management), compliance (GDPR/CCPA/CPNI alignment, consent management, retention policies), monitoring (DLP rules, SIEM integration, audit procedures).

### 5. Generate Documentation Package
Create: Classification Policy (SPI/PII definitions, tagging procedures, owner responsibilities, catalog integration), Access Governance Guide (least privilege principles, JIT elevation procedures, PAW requirements, ABAC implementation, approval workflows), Security Documentation (encryption standards, key management, log scrubbing, secure analytics patterns), Compliance Guide (regulatory requirements, consent management, retention schedules, DPA requirements, breach response), Operations Runbook (monitoring procedures, incident response, audit processes, policy reviews, stakeholder scorecards).

### 6. Add Recommendations
Include: policy maintenance schedules, compliance reviews, security audits, training procedures, continuous improvement.

### 7. Validate and Report
Generate documentation artifacts. Report completion.

## Error Handling
**Incomplete Information**: Request classification inventory and compliance details.
**Missing Diagrams**: Generate from configuration and policies.

## Examples
**Example 1**: `/document-data-classification Create complete governance documentation` - Output: Policy docs, access guide, compliance documentation
**Example 2**: `/document-data-classification Generate compliance documentation for GDPR audit` - Output: GDPR compliance package with evidence

## References
