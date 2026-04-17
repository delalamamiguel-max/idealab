# Security Requirements

## System

- **System name:**
- **Owner/team:**
- **Primary data classification:**
- **Exposure:** internal | partner | public

## Verification target

- **Target standard:** OWASP ASVS (or equivalent)
- **Target level:** L1 | L2 | L3
- **Rationale:**

## Requirements (minimum)

### Identity and access

- Authentication mechanism documented.
- Authorization model documented (roles/permissions).
- Least privilege is enforced for service identities.

### Data protection

- Encryption in transit is enforced.
- Encryption at rest is enforced where applicable.
- Key management approach documented.

### Logging and monitoring

- Logs do not contain secrets or PII.
- Audit logging exists for privileged operations.

### Secure defaults

- Secure-by-default checklist completed.

### Supply chain

- SBOM produced for releases.
- Dependency monitoring and response process defined.

### Vulnerability management

- Vulnerability intake/triage workflow defined.
- SLAs defined for remediation.

## Exceptions

List approved exceptions with compensating controls.
