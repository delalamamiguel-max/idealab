---
description: Compare two container approaches or architectures
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read comparison criteria from:
`${ARCHETYPES_BASEDIR}/container-solution-architect/container-solution-architect-constitution.md`

### 2. Identify Comparison Type

Based on $ARGUMENTS, determine what to compare:

| Comparison Type | Examples |
|-----------------|----------|
| **Architectures** | Single-stage vs multi-stage, monolith vs multi-service |
| **Runtimes** | Docker vs Podman, supervisord vs s6-overlay |
| **Strategies** | Base+overlay vs single image, tmpfs vs overlay FS |
| **Configurations** | Resource limits, health check approaches |
| **Security Models** | Credential handling approaches |

### 3. Define Comparison Criteria

Apply constitution-based criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Security** | High | Credential handling, privilege separation |
| **Performance** | Medium | Build time, image size, runtime efficiency |
| **Maintainability** | Medium | Code organization, update procedures |
| **Scalability** | Medium | Multi-user support, resource usage |
| **Compliance** | High | Constitution alignment |

### 4. Analyze Option A

For the first option/approach:

```markdown
## Option A: {name}

### Description
{Brief description}

### Security
- Credential handling: {approach}
- User privileges: {UID/permissions}
- Secrets exposure: {risk level}

### Performance
- Build time: {estimate}
- Image size: {estimate}
- Startup time: {estimate}

### Maintainability
- Complexity: {low/medium/high}
- Update procedure: {description}
- Debugging: {ease}

### Scalability
- Multi-user: {yes/no}
- Resource efficiency: {description}

### Constitution Compliance
- Hard-stop violations: {count}
- Warnings: {count}
```

### 5. Analyze Option B

For the second option/approach:

```markdown
## Option B: {name}

### Description
{Brief description}

### Security
- Credential handling: {approach}
- User privileges: {UID/permissions}
- Secrets exposure: {risk level}

### Performance
- Build time: {estimate}
- Image size: {estimate}
- Startup time: {estimate}

### Maintainability
- Complexity: {low/medium/high}
- Update procedure: {description}
- Debugging: {ease}

### Scalability
- Multi-user: {yes/no}
- Resource efficiency: {description}

### Constitution Compliance
- Hard-stop violations: {count}
- Warnings: {count}
```

### 6. Generate Comparison Matrix

```markdown
## Comparison Matrix

| Criterion | Option A | Option B | Winner |
|-----------|----------|----------|--------|
| **Security** | | | |
| Credential handling | {a} | {b} | {winner} |
| Privilege separation | {a} | {b} | {winner} |
| **Performance** | | | |
| Build time | {a} | {b} | {winner} |
| Image size | {a} | {b} | {winner} |
| Startup time | {a} | {b} | {winner} |
| **Maintainability** | | | |
| Complexity | {a} | {b} | {winner} |
| Update ease | {a} | {b} | {winner} |
| **Scalability** | | | |
| Multi-user support | {a} | {b} | {winner} |
| Resource efficiency | {a} | {b} | {winner} |
| **Compliance** | | | |
| Constitution alignment | {a} | {b} | {winner} |

**Overall Score**: Option A: {score}/10, Option B: {score}/10
```

### 7. Provide Recommendations

```markdown
## Recommendation

### Recommended Option: {Option A/B}

**Rationale**:
{Why this option is recommended}

### When to Choose Option A
- {scenario-1}
- {scenario-2}

### When to Choose Option B
- {scenario-1}
- {scenario-2}

### Migration Path (if applicable)
{Steps to migrate from one to the other}

### Trade-offs to Accept
{What you give up with the recommended option}
```

---

## Common Comparisons

### Single-Stage vs Multi-Stage Build

| Aspect | Single-Stage | Multi-Stage |
|--------|--------------|-------------|
| Image size | Larger (includes build tools) | Smaller (runtime only) |
| Security | Higher attack surface | Minimal attack surface |
| Build complexity | Simpler | More complex |
| **Recommendation** | Dev/prototype only | **Production** |

### Docker vs Podman

| Aspect | Docker | Podman |
|--------|--------|--------|
| Daemon | Required | Daemonless |
| Root | Historically required | Rootless native |
| Compose | docker-compose | podman-compose |
| Corporate compatibility | TLS MITM issues | Same issues |
| **Recommendation** | Either works | **Podman** for security |

### supervisord vs s6-overlay

| Aspect | supervisord | s6-overlay |
|--------|-------------|------------|
| Size | ~30MB | ~5MB |
| Complexity | Simpler config | More complex |
| Signal handling | Manual | Better defaults |
| Python dependency | Required | None |
| **Recommendation** | **Simple cases** | Complex signal needs |

### tmpfs vs Overlay FS for Scratch

| Aspect | tmpfs | Overlay FS |
|--------|-------|------------|
| Memory usage | Proportional to writes | Zero |
| Performance | Faster I/O | Slightly slower |
| Multi-container | OOM risk | Safe |
| **Recommendation** | Single container | **Multi-container** |

### Base+Overlay vs Single Image

| Aspect | Base+Overlay | Single Image |
|--------|--------------|--------------|
| Build time | Fast (overlay seconds) | Slow (full rebuild) |
| Storage | Shared base layers | Duplicated |
| Multi-user | Designed for it | Not ideal |
| Complexity | Higher | Lower |
| **Recommendation** | **Multi-user** | Single user |

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/container-solution-architect/container-solution-architect-constitution.md`
- **Related**: scaffold-container-solution-architect, refactor-container-solution-architect
