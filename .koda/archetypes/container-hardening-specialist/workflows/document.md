---
description: Generate comprehensive container security documentation including threat models, CIS compliance matrices, capability justification tables, UID maps, and tmpfs mount inventories
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read documentation templates from:
`${ARCHETYPES_BASEDIR}/container-hardening-specialist/container-hardening-specialist-constitution.md`

Focus on Section II (Mandatory Patterns 2.6, 2.7) for document formats and Section V (Checklist).

### 2. Identify Documentation Scope

Determine which documents to generate from $ARGUMENTS:

| Document | Description | When to Generate |
|----------|-------------|-----------------|
| **Threat Model** | Attack vector/impact/mitigation table + UID map | Every hardened container |
| **CIS Compliance Matrix** | CIS Docker Benchmark section 4+5 compliance | Every hardened container |
| **Capability Justification** | Per-capability rationale for any re-added caps | When capabilities are re-added |
| **UID/GID Map** | User/group access matrix with file permissions | Every multi-UID container |
| **tmpfs Mount Inventory** | Mount paths, sizes, flags, and rationale | Every read-only rootfs container |
| **Security Posture Summary** | Executive summary for security review | Compliance audits |
| **Hardening Runbook** | Step-by-step operational guide for the container | Operations handoff |

### 3. Generate Threat Model

Follow the template from constitution Section II.7:

**3.1 Attack Vector Table**

Enumerate at least 10 attack vectors relevant to the specific container. For each vector:

- **Vector**: What the attacker does
- **Impact**: What damage results (Critical/High/Medium/Low)
- **Likelihood**: How likely without mitigation (High/Medium/Low)
- **Mitigation**: What defense is in place
- **Verification**: How to test the mitigation works

Tailor vectors to the application. A web server has different attack vectors than a batch processing container. Always include:

1. Container escape via root execution
2. Secret extraction from environment
3. Privilege escalation via capabilities
4. Filesystem tampering
5. Setuid binary exploitation
6. /proc information leak
7. Cross-process secret access
8. Resource exhaustion
9. Supply chain compromise
10. Image tampering

**3.2 UID/GID Access Matrix**

Map every UID/GID to its purpose, file access permissions, and what it explicitly cannot access. Include the file permission modes that enforce the access boundaries.

### 4. Generate CIS Compliance Matrix

Follow the template from constitution Section II.6:

**4.1 Section 4: Container Images and Build Files**

Evaluate each CIS recommendation against the Containerfile:

- 4.1: User for the container
- 4.2: Trusted base images
- 4.3: Unnecessary packages
- 4.6: HEALTHCHECK instruction
- 4.7: Update instructions alone
- 4.9: Use COPY instead of ADD
- 4.10: Secrets in Dockerfiles

**4.2 Section 5: Container Runtime**

Evaluate each CIS recommendation against the run configuration:

- 5.1: AppArmor profile
- 5.2: SELinux security options
- 5.3: Linux kernel capabilities
- 5.4: Privileged containers
- 5.7: Privileged ports
- 5.10: Host network mode
- 5.12: Read-only root filesystem
- 5.15: Host process namespace
- 5.21: Default seccomp profile
- 5.25: Additional privileges
- 5.28: PID cgroup limit

For each item, record: Status (PASS/FAIL/N/A), Implementation detail, Evidence command.

### 5. Generate Capability Justification Table

If any capabilities are re-added beyond `--cap-drop=ALL`:

| Capability | Justification | Process Using It | Syscall/Operation | Can It Be Avoided? |
|-----------|--------------|-----------------|-------------------|-------------------|
| `SETUID` | Executor drops from root to UID 1002 | start-executor | `setuid()` | No — required for privilege separation |
| `SETGID` | Executor sets GID 2000 for shared access | start-executor | `setgid()` | No — required for group file sharing |

Each entry must answer "Can it be avoided?" — if yes, recommend the alternative.

### 6. Generate tmpfs Mount Inventory

| Mount Path | Size | noexec | nosuid | nodev | Rationale |
|-----------|------|--------|--------|-------|-----------|
| `/tmp` | 256Mi | ✅ | ✅ | ✅ | General temporary files |
| `/var/log` | 64Mi | ✅ | ✅ | — | Application and supervisor logs |
| `/var/run` | 8Mi | ✅ | ✅ | — | PID files, Unix domain sockets |
| `/scratch` | 5Gi | — | ✅ | — | Build artifacts requiring exec |

Include the equivalent Podman and Kubernetes syntax for each mount.

### 7. Generate Security Posture Summary

Executive summary for security reviewers and compliance auditors:

```text
## Security Posture Summary — {application-name}

**Assessment Date**: {date}
**Container Image**: {image:tag}
**Base Image**: {base_image}
**CIS Benchmark Version**: v1.6.0

### Hardening Status

| Category | Status | Score |
|----------|--------|-------|
| Non-root execution | ✅ Enforced | 1/1 |
| Privilege separation | ✅ Multi-UID | 1/1 |
| Capability minimization | ✅ Drop-all + {N} re-adds | 1/1 |
| Read-only rootfs | ✅ Enforced | 1/1 |
| Secret protection | ✅ File-based, mode 400 | 1/1 |
| Setuid stripping | ✅ Complete | 1/1 |
| No-new-privileges | ✅ Enforced | 1/1 |
| No privileged mode | ✅ Confirmed | 1/1 |
| **Overall** | **✅ Fully Hardened** | **8/8** |

### Key Controls

- **Identity**: Service UID {uid1}, User UID {uid2}, Shared GID {gid}
- **Capabilities**: {list of re-added capabilities with count}
- **Writable Paths**: {count} tmpfs mounts, total {size}
- **Secret Access**: Compiled credentials, file-then-closure pattern
- **Compliance**: CIS Docker Benchmark {pass_count}/{total_count} items passed

### Residual Risks

1. {residual_risk_1} — Mitigation: {mitigation}
2. {residual_risk_2} — Mitigation: {mitigation}
```

### 8. Generate Hardening Runbook (Optional)

If requested, generate an operational runbook covering:

- **Build**: How to build the hardened image (exact command)
- **Secrets**: How to inject secrets (credential compilation script usage)
- **Run**: How to start the container with all hardening flags
- **Deploy**: How to deploy to Kubernetes with SecurityContext
- **Monitor**: What to monitor (Falco rules, log patterns)
- **Rotate**: How to rotate secrets (rebuild or remount)
- **Incident**: What to do if a security alert fires

---

## Post-Documentation Checklist

```text
✅ Threat model with 10+ attack vectors
✅ CIS compliance matrix (Sections 4 + 5)
✅ UID/GID access matrix
✅ Capability justification table (if applicable)
✅ tmpfs mount inventory with sizes and flags
✅ Security posture summary (executive view)

Optional:
✅ Hardening runbook for operations team
```

---

## Error Handling

**No Running Container**: Generate documentation from the Containerfile and run configuration files. Note which CIS items could not be verified without a running container.

**Missing Information**: If $ARGUMENTS does not specify the container or Containerfile path, ask the user to provide the Containerfile location and run command. The threat model requires understanding the application's purpose and network exposure.

**Incremental Documentation**: If some documents already exist, update them rather than regenerating from scratch. Merge new findings into existing tables.

## Examples

### Example 1: Full Documentation Suite
```text
/document-container-hardening-specialist "
Generate full security documentation for our BluePearl workspace container.
Containerfile: container/Containerfile.system-base
K8s manifest: container/k8s/pod-security-context.yaml
Credentials: container/scripts/compile-credentials
"
```

### Example 2: CIS Compliance Only
```text
/document-container-hardening-specialist "
We need CIS Docker Benchmark compliance documentation for our
upcoming security audit. Container: myapp:v2.1.0
Just the compliance matrix — threat model already exists.
"
```

### Example 3: Executive Summary
```text
/document-container-hardening-specialist "
Generate a one-page security posture summary for management review.
Container: production-api:latest
Focus on the 8/8 hardening scorecard format.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/container-hardening-specialist/container-hardening-specialist-constitution.md` Sections II.6, II.7, V
- **Related**: scaffold-container-hardening-specialist, test-container-hardening-specialist
