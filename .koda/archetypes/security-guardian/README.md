# Security Guardian Archetype

The Security Guardian archetype provides a cross-cutting security baseline for delivery teams. It defines security requirements, SDLC gates, secure-by-default configuration checklists, and verification workflows aligned to OWASP guidance.

## When to use
- You need a standard, organization-wide security baseline for delivery artifacts.
- You are defining security requirements for new systems or major changes.
- You need to operationalize DevSecOps gates across CI/CD.

## What it delivers
- Security requirements framework (ASVS-aligned)
- Threat modeling template
- Secure-by-default checklist
- Security test matrix (SAST/DAST/IAST/SCA/SBOM)
- Vulnerability management workflow
- Security metrics starter set

## Workflows
- `scaffold-security-guardian`: generate baseline security artifacts for a project
- `test-security-guardian`: validate that security gates and artifacts are present
- `refactor-security-guardian`: harden existing artifacts to meet baseline
- `document-security-guardian`: compile a security packet for audits
- `debug-security-guardian`: triage security gate failures

## Folder layout
```
security-guardian/
  manifest.yaml
  README.md
  security-guardian-constitution.md
  .windsurf/workflows/
  templates/
  scripts/
```

## Notes
- This archetype is designed to be used alongside other archetypes and should not replace their domain-specific security controls.
- Validation is expected to run in strict mode and now checks for fail-closed CI security gates plus SBOM presence.
