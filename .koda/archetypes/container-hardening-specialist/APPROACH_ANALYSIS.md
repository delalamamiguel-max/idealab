# Container Hardening Specialist: Approach Analysis

**Analysis Date**: March 2026
**Source**: `docs/plans/new-archetypes.md` § CREATE NEW #2
**Status**: Pre-creation analysis — constitution and workflows not yet built

---

## 1. Why This Archetype Exists

`container-solution-architect` focuses on **building and structuring** containers — Containerfiles, compose configurations, health checks, multi-stage builds, process supervision. It does not cover defense-in-depth security hardening patterns that are increasingly required for enterprise and government workloads.

Container hardening is a distinct discipline that involves:

- Multi-UID privilege separation (service UID vs user UID vs shared GID)
- Read-only root filesystems with explicit tmpfs writable mounts
- Capability dropping (`--cap-drop=ALL`) with minimal re-adds and justification
- Compiled credential injection (build-time secrets as files, never env vars)
- The file-then-closure secret access pattern for privilege-separated processes
- Setuid/setgid binary stripping across the entire image
- Seccomp profiles and AppArmor/SELinux policies
- Kubernetes SecurityContext configuration
- CIS Docker Benchmark compliance

Teams that skip hardening end up with containers that run as root, expose secrets in environment variables, retain unnecessary capabilities, and fail enterprise security audits.

---

## 2. Reference Implementation

BluePearl's own container hardening serves as the battle-tested reference:

| File | Lines | Role |
|------|-------|------|
| `container/Containerfile.system-base` | ~84 | System base image: multi-UID separation (1001 service, 1002 user, GID 2000), directory structure with precise ownership/permissions, setuid/setgid stripping, corporate CA injection |
| `container/Containerfile.optimized` | ~129 | Runtime assembly: permission hardening (500/400 for code, 550 for config, 770 for workspace, 750/440 for docs) |
| `container/k8s/pod-security-context.yaml` | ~40 | Kubernetes SecurityContext: `capabilities.drop: ["ALL"]`, `add: ["SETUID","SETGID","DAC_READ_SEARCH","KILL"]`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false` |
| `container/scripts/compile-credentials.sh` | ~80 | Credential compilation: JSON output with PAT, token, hash, OID, LiteLLM key; file permissions 440, UID 1001:GID 2000 |
| `docs/security/security-model.md` | ~300 | Full threat model: 10 vectors with mitigations, privilege separation diagram, UID/file permission matrix |
| `docs/design/service-communication.md` | ~200 | Compiled credential pattern, file-then-closure pattern, SHA-256 token hash verification |

### Key Patterns to Encode

1. **Multi-UID separation** — Service UID (1001) for gateway/MCP, User UID (1002) for agent commands, Shared GID (2000) for cross-process file access
2. **Read-only rootfs** — `--read-only` flag with explicit tmpfs mounts (each with specific size and noexec/nosuid flags)
3. **Capability dropping** — `--cap-drop=ALL` + only re-add with documented justification (SETUID for privilege drop, SETGID for group, DAC_READ_SEARCH for root traversal, KILL for supervisord)
4. **Compiled credentials** — Build-arg → compile script → JSON file (440 perms), loaded at startup via singleton, never in `process.env`
5. **File-then-closure pattern** — Process reads secret file before privilege drop, passes via function parameter closure — secret never stored in global state or env
6. **Setuid stripping** — `find / -xdev -perm /6000 -type f -exec chmod a-s {} +` removes all setuid/setgid binaries
7. **No-new-privileges** — `--security-opt no-new-privileges` prevents escalation via exec
8. **Supervisord via bash** — `command=/bin/bash <script>` instead of direct execution; scripts stay mode 400 (read-only), interpreted by bash

---

## 3. Scope Boundaries

### In Scope

- Multi-UID privilege separation (service, user, shared group)
- Read-only root filesystem configuration with explicit tmpfs writable mounts
- Linux capability management (drop all, re-add with justification)
- Compiled credential injection (build-time file-based secrets)
- File-then-closure secret access pattern
- Setuid/setgid binary stripping
- Kubernetes SecurityContext / PodSecurityPolicy / PodSecurityStandards
- CIS Docker Benchmark compliance checklists
- Seccomp profile creation and application
- AppArmor/SELinux profile guidance
- Container image scanning integration (Trivy, Grype)
- SBOM generation (syft, CycloneDX)
- Image signing (cosign, Sigstore)
- Threat model documentation (vector/impact/mitigation tables)
- `--security-opt no-new-privileges`
- tmpfs mount sizing and flag selection

### Out of Scope (Delegated)

- Container building and structuring → `container-solution-architect`
- Kubernetes deployment and Helm charts → `aks-devops-deployment`
- CI/CD pipeline security → `microservice-cicd-architect`
- Application-level security (OWASP Top 10) → `data-security`
- Network policy design → `aks-devops-deployment`
- Secret management infrastructure (Vault, KMS) → `key-vault-config-steward`

---

## 4. Industry Standards Alignment

| Practice | Standard/Source | Constitution Section |
|----------|----------------|---------------------|
| Read-only rootfs | CIS Docker Benchmark 5.12 | Hard-stop rule |
| Drop all capabilities | CIS Docker Benchmark 5.3 | Hard-stop rule |
| No-new-privileges | CIS Docker Benchmark 5.25 | Hard-stop rule |
| Non-root user | CIS Docker Benchmark 4.1 | Hard-stop rule |
| Setuid stripping | NIST SP 800-190 | Mandatory pattern |
| tmpfs for writable paths | Container best practice | Mandatory pattern |
| Secret file permissions | OWASP Container Security | Hard-stop rule |
| No secrets in env vars | 12-factor critique, OWASP | Hard-stop rule |
| Kubernetes SecurityContext | CIS Kubernetes Benchmark | Mandatory pattern |
| Image signing | Sigstore/cosign | Recommended pattern |
| SBOM generation | CISA, SPDX/CycloneDX | Recommended pattern |
| Runtime security scanning | Falco/Sysdig | Recommended pattern |
| Seccomp profiles | CIS Docker Benchmark 5.21 | Recommended pattern |
| AppArmor/SELinux | CIS Docker Benchmark 5.1-5.2 | Recommended pattern |

### Gaps Beyond BluePearl Reference (to address in constitution)

| Gap | Priority | Approach |
|-----|----------|----------|
| Distroless base images | Medium | Recommend Google distroless as alternative to slim images |
| Image signing (cosign) | High | Add Sigstore/cosign workflow step |
| SBOM generation | High | Add syft/trivy SBOM generation to scaffold |
| Runtime security scanning | Medium | Add Falco/Sysdig integration guidance |
| Seccomp profile templates | Medium | Provide default restrictive seccomp JSON profiles |
| AppArmor profile guidance | Low | Reference AppArmor profile generation tools |
| PID limits | Low | Add `--pids-limit` to resource governance |
| Network namespace isolation | Low | Add network segmentation guidance |

---

## 5. Constitution Structure Plan

### Hard-Stop Rules (non-negotiable)

1. **No root execution** — All application processes must run as non-root UIDs
2. **No secrets in environment variables** — All secrets via compiled credential files with restricted permissions
3. **Drop ALL capabilities** — `--cap-drop=ALL`; re-adds require documented justification per capability
4. **Read-only root filesystem** — `--read-only` or `readOnlyRootFilesystem: true`; writable paths via tmpfs only
5. **No-new-privileges** — `--security-opt no-new-privileges` on every container
6. **Secret file permissions** — 400 (owner-read) or 440 (owner+group-read); never world-readable
7. **Setuid/setgid stripped** — All setuid/setgid binaries stripped in Containerfile build step
8. **No privileged mode** — `--privileged` is never acceptable

### Mandatory Patterns

1. Multi-UID privilege separation (service UID, user UID, shared GID)
2. Compiled credential injection (build-arg → compile script → JSON file)
3. File-then-closure secret access (read before privilege drop, pass via closure)
4. tmpfs mount specification (path, size, flags: noexec/nosuid/nodev)
5. Kubernetes SecurityContext YAML
6. CIS Docker Benchmark compliance checklist
7. Threat model document (vector/impact/mitigation table)

### Recommended Patterns

1. Distroless or minimal base images
2. Image signing with cosign
3. SBOM generation with syft
4. Seccomp profile (custom or default)
5. Container image scanning in CI (Trivy/Grype)
6. PID limits (`--pids-limit`)
7. Runtime security monitoring (Falco)

---

## 6. Workflow Plan

| Workflow | Purpose | Key Deliverables |
|----------|---------|-----------------|
| **scaffold** | Full hardened container from scratch | Multi-stage Containerfile with UID separation, read-only rootfs config, capability drop flags, compile-credentials.sh, file-then-closure code template, K8s SecurityContext YAML, threat model doc, CIS checklist |
| **compare** | Compare hardening approaches | Side-by-side of capability sets, rootfs strategies, credential injection methods, base image choices |
| **refactor** | Harden an existing container | Audit current posture → identify gaps → apply hardening layers incrementally |
| **test** | Security scan + compliance check | CIS Benchmark audit, capability verification, secret exposure scan, rootfs writability test, setuid scan |
| **debug** | Fix security issues | Permission denied errors, capability conflicts, tmpfs sizing, credential loading failures |
| **document** | Generate security posture docs | Threat model, CIS compliance matrix, capability justification table, UID map, tmpfs mount inventory |

---

## 7. Keyword Differentiation from `container-solution-architect`

| Query | Expected Route | Rationale |
|-------|---------------|-----------|
| "Build a containerized Node.js app" | `container-solution-architect` | General container building |
| "Harden my container for production" | `container-hardening-specialist` | Security hardening |
| "Add health checks to my container" | `container-solution-architect` | Runtime configuration |
| "Drop capabilities from my container" | `container-hardening-specialist` | Capability management |
| "Create a multi-stage Containerfile" | `container-solution-architect` | Build optimization |
| "Make my container read-only" | `container-hardening-specialist` | Rootfs hardening |
| "Set up supervisord in container" | `container-solution-architect` | Process supervision |
| "Remove secrets from environment variables" | `container-hardening-specialist` | Credential hardening |
| "CIS Docker Benchmark compliance" | `container-hardening-specialist` | Compliance audit |
| "Create docker-compose.yml" | `container-solution-architect` | Dev environment |

**Routing conflict risk**: LOW — keywords are distinct (`container-hardening`, `cap-drop`, `read-only-rootfs`, `seccomp`, `privilege-separation` vs `container`, `dockerfile`, `health-check`, `supervisord`, `multi-stage`).

---

## 8. Implementation Approach

### Phase 1: Constitution

1. Read BluePearl reference implementation files (Containerfile.system-base, Containerfile.optimized, security-model.md, service-communication.md)
2. Extract 8 hard-stop rules from operational experience
3. Define 7 mandatory patterns with code templates
4. Incorporate industry gaps (cosign, SBOM, seccomp, distroless)
5. Create refusal template for requests that violate hard-stop rules

### Phase 2: Workflows

1. **scaffold** first — most complex, establishes all deliverables
2. **test** second — validates scaffold output (CIS compliance gate)
3. **refactor** third — most common real-world use case (hardening existing containers)
4. **compare**, **debug**, **document** — follow standard patterns

### Phase 3: Validation

1. Run scaffold on a fresh Node.js container project
2. Verify all 10 key deliverables produced (Containerfile, compile-credentials.sh, K8s YAML, threat model, etc.)
3. Run test workflow to validate CIS compliance
4. Run refactor workflow on an unhardened container (root user, secrets in env, no cap-drop)

---

## 9. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Overlap with `container-solution-architect` security section | Medium | Clear scope: CSA handles "how to build", CHS handles "how to lock down" |
| Overly restrictive defaults break applications | High | Provide justification framework for re-adding capabilities; start with most common patterns |
| CIS Benchmark version drift | Low | Reference specific benchmark version; note update cadence |
| Kubernetes vs Podman divergence | Medium | Provide both `podman run` flags and K8s SecurityContext equivalents |
| Corporate proxy TLS inspection conflicts | Medium | Reference BluePearl's operational experience with CA cert injection |

---

*This document guides the creation of the `container-hardening-specialist` archetype. Review and approve before proceeding with constitution and workflow authoring.*
