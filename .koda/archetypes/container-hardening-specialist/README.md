# Container Hardening Specialist

Apply defense-in-depth security hardening to containers including privilege separation with multi-UID, read-only rootfs, capability dropping, compiled credential injection, setuid stripping, seccomp profiles, and the file-then-closure secret pattern.

## Status

**Complete** — Constitution, all 6 workflows, and manifest finalized.

## Workflows

| Workflow | Command | Purpose |
|----------|---------|---------|
| **Scaffold** | `/scaffold-container-hardening-specialist` | Generate a fully hardened container from scratch |
| **Compare** | `/compare-container-hardening-specialist` | Compare capability sets, rootfs strategies, credential injection methods |
| **Refactor** | `/refactor-container-hardening-specialist` | Audit existing container and apply hardening incrementally |
| **Test** | `/test-container-hardening-specialist` | CIS compliance check, capability verification, secret exposure scan |
| **Debug** | `/debug-container-hardening-specialist` | Diagnose permission denied, read-only FS, capability conflicts |
| **Document** | `/document-container-hardening-specialist` | Generate threat model, CIS matrix, UID map, capability justification |

## Key Deliverables

- Hardened Containerfile with multi-UID separation (service UID 1001, user UID 1002, shared GID 2000)
- `compile-credentials.sh` with mode-400 output and directory lockdown
- Podman/Docker run command with `--cap-drop=ALL`, `--read-only`, `--security-opt no-new-privileges`
- Kubernetes SecurityContext YAML with Pod Security Standard `restricted` namespace
- CIS Docker Benchmark v1.6.0 compliance checklist
- Threat model with 10 attack vectors and UID/GID access matrix

## Constitution Highlights

- **8 Hard-Stop Rules**: No root execution, no secrets in env vars, drop ALL capabilities, read-only rootfs, no-new-privileges, secret file permissions (mode 400), setuid stripping, no privileged mode
- **7 Mandatory Patterns**: Multi-UID separation, compiled credentials, file-then-closure secret access, tmpfs specification, K8s SecurityContext, CIS checklist, threat model
- **7 Preferred Patterns**: Distroless images, cosign signing, SBOM generation, seccomp profiles, image scanning, PID limits, runtime monitoring

## Reference Implementation

BluePearl's own hardened container stack serves as the battle-tested reference:

- `container/Containerfile.system-base` — Multi-UID separation, setuid stripping, directory ownership
- `container/Containerfile.optimized` — Permission hardening, file mode matrix
- `container/k8s/pod-security-context.yaml` — Full SecurityContext with Podman equivalents
- `container/scripts/compile-credentials.sh` — Compiled credential injection pattern
- `docs/security/security-model.md` — Threat model, privilege separation diagram

## Related Archetypes

- `container-solution-architect` — Container building and structuring (delegates hardening here)
- `aks-devops-deployment` — Kubernetes deployment, Helm charts, network policies
- `key-vault-config-steward` — Secret management infrastructure (Vault, KMS)
