# Security Guardian Constitution

## Purpose

Establishes an enterprise-wide, cross-cutting security baseline that applies to:

- Web applications and APIs
- Data pipelines and batch/stream processing
- Notebooks and interactive analysis environments
- Infrastructure and platform automation (IaC, CI/CD)

This archetype is tool-agnostic: it defines minimum requirements and required evidence artifacts rather than prescribing specific vendors.

---

## I. Hard-Stop Rules (Non-Negotiable)

The LLM must refuse or correct any deliverable that violates these rules:

### 1.1 Secrets and credentials

- ✘ Never commit secrets (tokens, passwords, private keys, connection strings) into source control.
- ✘ Never place secrets in notebook cells, markdown docs, or example payloads.
- ✔ Always use an approved secrets mechanism (vault/secret manager/KMS/environment injection) and document the mechanism.

### 1.2 Data classification and privacy

- ✘ Never log or emit PII/secrets into logs, traces, metrics, or events.
- ✘ Never include PII/secrets in example data, screenshots, or documentation.
- ✔ Always document data classification for any system handling sensitive data.

### 1.3 Identity and access

- ✘ Never ship unauthenticated network services where authentication is required.
- ✘ Never use broad, shared credentials when least-privilege identities (service principals/workload identities) are available.
- ✔ Always define authorization boundaries (roles/permissions) for critical operations.

### 1.4 Security validation gates

- ✘ Never release without documented security gates and evidence artifacts (see Section V).
- ✘ Never accept "security TBD" for high/critical risk systems.
- ✔ Always document exceptions with approvals and compensating controls.

### 1.5 Vulnerability management

- ✘ Never ignore known critical/high vulnerabilities without a documented exception, owner, and remediation timeline.
- ✔ Always track vulnerabilities with a consistent workflow and SLA.

### 1.6 CI security gates must fail closed

- ✘ Never mark core security checks as non-blocking (`continue-on-error: true`) in release/PR pipelines.
- ✘ Never treat SBOM generation as optional for release candidates.
- ✔ Always fail the pipeline when dependency, secret, container-vulnerability, or SBOM checks fail.

---

## II. Mandatory Patterns (Must Apply)

### 2.1 Minimum evidence pack (required artifacts)

Each project adopting this archetype must produce a "security evidence pack" directory:

- `security/evidence/`
  - `security-requirements.md`
  - `risk-profile.md`
  - `threat-model.md`
  - `secure-by-default-checklist.md`
  - `security-test-matrix.md`
  - `vulnerability-management.md`
  - `security-metrics.md`

The artifacts must be version-controlled and updated as the system changes.

### 2.2 Risk profiling

- Classify the system risk (low/medium/high/critical) based on impact and exposure.
- Select a target verification level (default: ASVS Level 2 for typical enterprise applications).
- Document the decision in `security/evidence/risk-profile.md`.

### 2.3 Threat modeling

- Produce a threat model with:
  - system overview and data flows
  - assets and trust boundaries
  - prioritized threats and mitigations
  - residual risk and decision log

### 2.4 Secure-by-default configuration

- Maintain a secure-by-default checklist spanning:
  - authentication/authorization defaults
  - encryption in transit and at rest
  - logging/telemetry redaction
  - network exposure controls
  - dependency and build integrity

### 2.5 Security testing and verification

- Maintain a security test matrix describing:
  - what is tested (by category)
  - how it is tested (tool-agnostic)
  - when it runs (PR, nightly, release)
  - who owns it
  - what evidence is produced

### 2.6 Supply chain integrity

- Produce and store an SBOM for each release.
- Track third-party dependencies and monitor for vulnerabilities.
- Validate build provenance and artifact integrity where applicable.

### 2.7 Operational readiness

- Document incident response contacts and escalation path.
- Document log retention and access controls.
- Document backup/restore expectations for critical data.

### 2.8 CI gate baseline

- Maintain a dedicated security workflow under `.github/workflows/`.
- Include at minimum:
  - dependency vulnerability checks
  - secret scanning
  - container/image vulnerability scanning (where applicable)
  - SBOM generation and artifact retention
- Enforce fail-closed behavior for the above checks.

---

## III. Preferred Patterns (Recommended)

- Security champions per team/project.
- Automated policy checks in CI for evidence pack presence.
- Regular tabletop exercises for high/critical systems.
- Security scorecards based on defined metrics.

---

## IV. Required Outputs per Release

At minimum, each release must provide:

- Updated evidence pack (Section II.1)
- Release SBOM location recorded
- Security test execution evidence recorded
- Vulnerability status summary recorded

---

## V. Acceptance Criteria

A project is considered compliant with this archetype when:

- All required evidence artifacts exist and are non-empty.
- A risk profile and target verification level are documented.
- A threat model exists and includes mitigations for high-risk items.
- Security testing coverage is defined and executed on an agreed cadence.
- A vulnerability management workflow exists with explicit SLAs.
