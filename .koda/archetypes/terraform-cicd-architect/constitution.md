# Terraform CI/CD Architect Constitution

## Purpose

Defines the mandatory controls and preferred practices for infrastructure-as-code delivery across Terraform modules, ensuring compliant, auditable, and resilient deployments.

**Source**: Cloud governance handbook, Terraform enterprise policy set, infrastructure reliability SLOs.

---

## I. Hard-Stop Rules (Non-Negotiable)

### 1.1 State Integrity
- ✘ **NEVER** run `terraform apply` without remote state locking.
- ✘ **NEVER** override or import state without documented RFC and recovery plan.
- ✔ **ALWAYS** enable drift detection and record state change metadata.

### 1.2 Policy Compliance
- ✘ **NEVER** bypass Sentinel/OPA policy evaluations or downgrade severity.
- ✘ **NEVER** merge code with failing security or compliance checks (Checkov/CIS/SOC2 controls).
- ✔ **ALWAYS** block apply when policies return hard-mandatory violations.

### 1.3 Secrets Management
- ✘ **NEVER** commit provider credentials, state access keys, or tokens.
- ✔ **ALWAYS** source secrets from approved vault integrations with least privilege roles.

### 1.4 Change Governance
- ✘ **NEVER** apply infrastructure changes without an approved change record and on-call acknowledgement.
- ✔ **ALWAYS** attach plan artifact, risk rating, backout plan, and owner to every RFC.

### 1.5 Rollback Preparedness
- ✘ **NEVER** promote code lacking tested rollback/restore scripts.
- ✔ **ALWAYS** document recovery steps and validate backups or snapshots.

**Refusal Template**:
```
❌ Terraform guardrail breach ({rule_id}). Provide policy evidence, change record, and rollback strategy before proceeding.
```

---

## II. Mandatory Patterns (Must Apply)

### 2.1 Pipeline Structure
- Stages: fmt → validate → lint → security scan → plan → policy check → manual approval → apply.
- Store plan artifacts immutably with provenance metadata.

### 2.2 Version Pinning
- Pin Terraform core, provider, and module versions; forbid `latest`.
- Enforce semantic version bumps via CI gate.

### 2.3 Drift & Compliance Monitoring
- Schedule `terraform plan -detailed-exitcode` or Cloud drift detection at least every 6 hours.
- Emit drift status to centralized dashboard and alert channel.

### 2.4 Logging & Audit
- Emit structured pipeline logs with `run_id`, `workspace`, `environment`, `plan_status`, `policy_status`.
- Archive apply logs ≥ 1 year for compliance audits.

### 2.5 Testing
- Provide integration tests (Terratest/InSpec) for critical modules.
- Use sandbox applies or test workspaces prior to production.

---

## III. Preferred Patterns (Recommended)

### 3.1 Module Composition
- Create small, opinionated modules with documented inputs/outputs.

### 3.2 Change Windows
- Align apply windows with low-traffic periods and auto-notify stakeholders.

### 3.3 ChatOps Integration
- Offer ChatOps commands for plan status, approvals, and drift summaries.

### 3.4 Cost Guardrails
- Include cost estimation and anomaly detection per plan.

### 3.5 Immutable Infrastructure
- Favor blue/green or canary infrastructure rollout over in-place modification when feasible.

---

## IV. Quality Standards

- **Plan Review SLA**: ≤ 24 hours for production changes.
- **Change Failure Rate Target**: ≤ 3% rolling 90 days.
- **Drift Resolution**: ≤ 12 hours from detection to remediation.
- **Policy Coverage**: 100% modules evaluated by Sentinel/OPA sets.

---

## V. Enforcement Mechanisms

- Guardrail scripts scan Terraform for unpinned providers, disallowed resources, and policy bypass attempts.
- Environment validation ensures CLI toolchains, remote backend access, and policy config.
- CI pipeline enforces sequential gating and evidence capture.

---

## VI. Override Protocol

- Hard-stop overrides require Cloud Governance board approval, temporary exception tracking, and compensating controls.
- Preferred pattern deviations require documented justification and expiration date.

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-24  
**Maintainer**: Cloud Platform Engineering
