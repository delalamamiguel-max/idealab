---
description: Refactor data classification to close ethics gaps and strengthen governance evidence (Data Classification Policy)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-classification-policy --json ` and parse for CATALOG_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-classification-policy/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: current framework location, refactoring goals (coverage gaps, access tightening, encryption enhancement, compliance alignment), specific issues. Request clarification if incomplete.

### 4. Analyze Current State
Assess: classification coverage (tagged vs untagged data, accuracy), access controls (least privilege compliance, JIT adoption, PAW usage), encryption posture (at rest, in transit, key management), compliance alignment (GDPR/CCPA/CPNI requirements, consent documentation, retention adherence), monitoring effectiveness (DLP coverage, SIEM integration, audit completeness).

### 5. Generate Refactoring Plan
Create improvements: enhanced classification (automated tagging, lineage propagation, catalog integration), tightened access (implement ABAC, enforce JIT, require PAW), strengthened encryption (validate all paths, secure logs/caches, rotate keys), compliance enhancements (consent management, retention automation, DPA validation), improved monitoring (comprehensive SIEM, anomaly detection, audit trails).

### 6. Implement Refactorings
Generate refactored framework with improved controls, enhanced automation, strengthened compliance, updated documentation.

### 7. Validate and Report
Generate report with improvements. Report completion.

## Error Handling
**Coverage Gaps**: Prioritize by risk and implement phased rollout.
**Breaking Changes**: Coordinate with data owners and stakeholders.

## Examples
**Example 1**: `/refactor-data-classification Add ABAC controls to PII data access` - Output: Enhanced access framework with attribute-based policies
**Example 2**: `/refactor-data-classification Implement automated SPI classification` - Output: Automated tagging with catalog integration

## References
