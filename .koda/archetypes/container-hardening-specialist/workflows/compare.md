---
description: Compare container hardening approaches including capability sets, rootfs strategies, credential injection methods, and base image choices
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read hardening requirements from:
`${ARCHETYPES_BASEDIR}/container-hardening-specialist/container-hardening-specialist-constitution.md`

All comparisons must evaluate compliance with Section I hard-stop rules.

### 2. Identify Comparison Type

Categorize the comparison requested in $ARGUMENTS:

| Type | Description | Criteria |
|------|-------------|----------|
| **Capability Strategy** | Compare capability sets (drop-all+re-add vs selective drop) | Attack surface, CIS compliance, application compatibility |
| **Base Image** | Compare distroless vs slim vs Alpine vs full | Image size, vulnerability count, debug accessibility, shell availability |
| **Credential Injection** | Compare file-based vs env var vs Vault agent vs K8s CSI driver | Security, complexity, rotation, audit trail |
| **Rootfs Strategy** | Compare read-only+tmpfs vs read-write with AppArmor vs overlay-ro | Write protection, operational complexity, performance |
| **Secret Access** | Compare file-then-closure vs singleton vs env var passthrough | Scope confinement, testability, third-party library safety |
| **Signing/Provenance** | Compare cosign vs Notary v2 vs Docker Content Trust | Ecosystem support, keyless mode, K8s admission integration |
| **Runtime Monitoring** | Compare Falco vs Sysdig vs Tetragon vs custom eBPF | Detection coverage, performance overhead, alert quality |
| **Full Posture** | Compare two container configurations end-to-end | All hardening dimensions |

### 3. Build Comparison Matrix

For each comparison type, evaluate both options against constitution-aligned criteria.

**Capability Strategy Comparison**:

| Criterion | Drop-ALL + Re-Add | Selective Drop |
|-----------|-------------------|----------------|
| **CIS 5.3 compliance** | ✅ Fully compliant | ⚠️ May retain dangerous caps |
| **Default attack surface** | Minimal — only explicitly justified caps | Larger — all caps not explicitly dropped |
| **Application debugging** | Harder — must identify needed caps | Easier — fewer breakages |
| **Audit trail** | Clear — justification table documents each re-add | Unclear — which caps are needed vs inherited |
| **Constitution compliance** | ✅ Required by Rule 1.3 | ❌ Violates Rule 1.3 |

**Base Image Comparison**:

| Criterion | Distroless | Slim (Debian) | Alpine | Full (Debian) |
|-----------|-----------|---------------|--------|--------------|
| **Image size** | ~20-80MB | ~150-250MB | ~50-100MB | ~400-800MB |
| **CVE count** | Very low | Medium | Low | High |
| **Shell access** | ❌ None | ✅ bash | ✅ ash/sh | ✅ bash |
| **Package manager** | ❌ None | ✅ apt | ✅ apk | ✅ apt |
| **Debug ease** | Hard (kubectl debug) | Easy | Medium | Easy |
| **musl vs glibc** | glibc | glibc | musl (compat issues) | glibc |
| **Best for** | Production | Dev/CI + Prod | Small footprint | Development |

**Credential Injection Comparison**:

| Criterion | Compiled File (Build-time) | K8s Secret Mount | Vault Agent Sidecar | K8s CSI SecretStore |
|-----------|--------------------------|-----------------|--------------------|--------------------|
| **Constitution compliance** | ✅ Rule 1.2 compliant | ✅ If mode 0400 | ✅ File-based | ✅ File-based |
| **Rotation** | Requires rebuild | K8s auto-updates | Auto-rotation | Auto-rotation |
| **Audit trail** | Build log only | K8s audit log | Vault audit log | Both |
| **Complexity** | Low | Low | Medium | High |
| **External dependency** | None | K8s Secrets API | HashiCorp Vault | CSI driver + backend |
| **Best for** | Baked images, dev | Standard K8s | Enterprise, rotation | Multi-cloud |

### 4. Evaluate Against Constitution

For each option, explicitly check:

- [ ] Rule 1.1: Does it enforce non-root execution?
- [ ] Rule 1.2: Does it avoid secrets in environment variables?
- [ ] Rule 1.3: Does it support cap-drop=ALL?
- [ ] Rule 1.4: Does it work with read-only rootfs?
- [ ] Rule 1.5: Does it support no-new-privileges?
- [ ] Rule 1.6: Does it enforce file permissions on secrets?

### 5. Generate Recommendation

```text
## Hardening Comparison Report

**Comparison Type**: {type from Step 2}
**Date**: {timestamp}

### Options Evaluated

| Option | Constitution Compliance | Key Advantage | Key Risk |
|--------|----------------------|---------------|----------|
| {option_A} | {compliant/non-compliant} | {advantage} | {risk} |
| {option_B} | {compliant/non-compliant} | {advantage} | {risk} |

### Detailed Analysis

{per-criterion analysis from Step 3}

### Recommendation

**Recommended**: {option}

**Rationale**:
1. {reason_1}
2. {reason_2}
3. {reason_3}

**Migration Path** (if switching from current approach):
1. {step_1}
2. {step_2}
3. {step_3}

**Constitution Reference**: {relevant_sections}
```

---

## Error Handling

**Non-Compliant Option Requested**: If the user asks to compare an approach that violates a hard-stop rule (e.g., secrets via env vars vs file-based), clearly flag the non-compliant option as a constitution violation but still provide the comparison for educational value. Mark the recommendation as the compliant option only.

**Incomplete Input**: If $ARGUMENTS doesn't specify what to compare, present the comparison type table from Step 2 and ask the user to select.

## Examples

### Example 1: Base Image Selection
```text
/compare-container-hardening-specialist "
Compare distroless vs node:22-slim for our production Node.js API.
We need curl for health checks but want minimum CVE surface.
"
```

### Example 2: Credential Strategy
```text
/compare-container-hardening-specialist "
Compare our current compiled-credential-injection approach vs
HashiCorp Vault agent sidecar for secret injection.
We need automatic rotation for database passwords.
"
```

### Example 3: Full Posture Comparison
```text
/compare-container-hardening-specialist "
Compare our current container setup (runs as root, secrets in env,
no cap-drop) against a fully hardened configuration.
Show the gap analysis.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/container-hardening-specialist/container-hardening-specialist-constitution.md`
- **Related**: scaffold-container-hardening-specialist, refactor-container-hardening-specialist
