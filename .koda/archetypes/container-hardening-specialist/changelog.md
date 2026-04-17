# Changelog — Container Hardening Specialist

## 1.0.0 (2026-03-02)

### Added

- **Constitution** (`container-hardening-specialist-constitution.md`): 817 lines covering 7 sections
  - 8 hard-stop rules: no root execution, no secrets in env vars, drop ALL capabilities, read-only rootfs, no-new-privileges, secret file permissions (mode 400), setuid stripping, no privileged mode
  - 7 mandatory patterns: multi-UID separation, compiled credentials, file-then-closure secret access, tmpfs specification, K8s SecurityContext, CIS checklist, threat model
  - 7 preferred patterns: distroless images, cosign signing, SBOM generation, seccomp profiles, image scanning, PID limits, runtime monitoring
  - Troubleshooting guide with 6 common issues
  - Security and performance checklist (build-time, runtime, K8s, documentation)
  - Refusal template with example
- **Scaffold workflow** (`scaffold-container-hardening-specialist.md`): Full hardened container generation with Containerfile, compile-credentials.sh, run command, K8s SecurityContext, CIS checklist, and threat model
- **Compare workflow** (`compare-container-hardening-specialist.md`): Side-by-side evaluation of capability strategies, base images, credential injection methods, rootfs strategies, and signing tools with 4 pre-built comparison tables
- **Refactor workflow** (`refactor-container-hardening-specialist.md`): Security posture audit with incremental hardening layers (non-root, cap-drop, read-only rootfs, credential hardening, setuid stripping, security flags)
- **Test workflow** (`test-container-hardening-specialist.md`): 10-category validation covering non-root execution, multi-UID separation, secret exposure, setuid binaries, capabilities, read-only rootfs, no-new-privileges, privileged mode, K8s SecurityContext, and documentation
- **Debug workflow** (`debug-container-hardening-specialist.md`): 8-category issue diagnosis with diagnostic commands for permission denied, read-only FS, capability failures, credential loading, tmpfs exhaustion, K8s admission, health checks, and setuid conflicts
- **Document workflow** (`document-container-hardening-specialist.md`): Threat model, CIS compliance matrix, capability justification table, UID/GID map, tmpfs mount inventory, security posture summary, and hardening runbook generation
- **Manifest** (`manifest.yaml`): 13 keywords, constitution path, all 6 workflow entries
- **README** (`README.md`): Workflow table, key deliverables, constitution highlights, reference implementation links
