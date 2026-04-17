# Secure-by-Default Checklist

## Identity and access

- [ ] All services require authentication where appropriate.
- [ ] Authorization is enforced server-side.
- [ ] Default roles are least-privilege.

## Secrets

- [ ] No secrets in code/notebooks/docs.
- [ ] Secrets are injected via approved mechanism.
- [ ] Secret rotation procedure exists.

## Data protection

- [ ] Encryption in transit enabled.
- [ ] Encryption at rest enabled where applicable.
- [ ] Key management documented.

## Network exposure

- [ ] Only required ports/services exposed.
- [ ] Admin endpoints are protected.
- [ ] Egress restrictions considered/documented.

## Logging and telemetry

- [ ] Logs/telemetry redact secrets and PII.
- [ ] Audit logging exists for privileged actions.
- [ ] Log retention and access controls defined.

## Supply chain

- [ ] Dependencies are tracked.
- [ ] SBOM produced and stored per release.
- [ ] Build and release process integrity documented.

## Infrastructure and CI/CD

- [ ] Infrastructure changes are reviewed.
- [ ] CI enforces baseline policy checks.
- [ ] Release branches have security gates enabled.
