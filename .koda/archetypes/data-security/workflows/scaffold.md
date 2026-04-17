---
description: Scaffold data security framework with encryption, access controls, and threat detection (Data Security)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype data-security --json ` and parse for SECURITY_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/data-security/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: data assets scope, security requirements, threat model, compliance mandates, access control needs. Request clarification if incomplete.

### 4. Generate Security Framework
Create comprehensive security controls: encryption (at-rest AES-256, in-transit TLS 1.3, key management with rotation), access controls (zero-trust architecture, least privilege, MFA enforcement, RBAC/ABAC), network security (VPC isolation, private endpoints, security groups, network policies), threat detection (anomaly detection, intrusion detection, DLP monitoring, SIEM integration), data protection (backup encryption, secure deletion, data masking, tokenization), audit logging (comprehensive access logs, security event capture, compliance trails).

### 5. Generate Security Monitoring
Implement: security dashboards, threat alerts, compliance scanning, vulnerability assessment, penetration testing procedures, incident response playbooks.

### 6. Add Recommendations
Include: security best practices, zero-trust principles, defense-in-depth strategies, continuous monitoring, security reviews.

### 7. Validate and Report
Generate framework. Report completion.

## Error Handling
**Encryption Gaps**: Require encryption for all data at rest and in transit.
**Access Too Broad**: Enforce least privilege and zero-trust.

## Examples
**Example 1**: `/scaffold-data-security Create security framework for customer data` - Output: Complete security controls with encryption and monitoring
**Example 2**: `/scaffold-data-security Implement zero-trust data access` - Output: Zero-trust architecture with ABAC

## References
