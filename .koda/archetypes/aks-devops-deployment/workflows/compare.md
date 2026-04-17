---
description: Compare AKS deployment strategies, architectures, and framework approaches
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Parse Comparison Request

Extract from $ARGUMENTS:
- Comparison type (framework, deployment strategy, CI/CD, observability)
- Specific options to compare
- Project constraints (team skills, budget, timeline)
- Existing infrastructure

### 2. Framework Comparison

Compare Node.js vs Python vs Java vs .NET for:

| Factor | Node.js | Python | Java | .NET |
|--------|---------|--------|------|------|
| Image Size | ~100MB | ~150MB | ~200MB | ~150MB |
| Startup Time | Fast | Medium | Slow | Medium |
| Memory | Low | Medium | High | Medium |
| Concurrency | ✓✓ | ✓ | ✓✓ | ✓✓ |
| ML Support | - | ✓✓ | ✓ | ✓ |

### 3. Deployment Strategy Comparison

| Strategy | Risk | Complexity | Rollback Speed | Resource Cost |
|----------|------|------------|----------------|---------------|
| Blue/Green | Low | Medium | Instant | 2x |
| Canary | Low | High | Fast | +10-25% |
| Rolling | Medium | Low | Slow | Minimal |

### 4. CI/CD Platform Comparison

| Platform | Azure Integration | Cost | Complexity |
|----------|-------------------|------|------------|
| Azure DevOps | ✓✓ Native | Included | Medium |
| GitHub Actions | ✓ Good | Per-minute | Low |
| Jenkins | ✓ Manual | Self-hosted | High |

### 5. Generate Decision Matrix

| Criterion | Option A | Option B | Weight | Recommendation |
|-----------|----------|----------|--------|----------------|
| Performance | _/10 | _/10 | High | |
| Cost | _/10 | _/10 | Medium | |
| Complexity | _/10 | _/10 | Medium | |
| Security | _/10 | _/10 | High | |
| Team Skills | _/10 | _/10 | High | |

### 6. Provide Recommendation

Output recommendation with:
- Selected option and rationale
- Constitution compliance verification
- Migration path (if changing existing setup)
- Risk factors and mitigations

## Error Handling

**Insufficient Context**: Request specific project constraints before comparing.

**Equal Scores**: Recommend based on constitution alignment and team familiarity.

**Non-Compliant Option**: Reject options that violate hard-stop rules.

## Examples

### Example 1: Framework Selection

```
/compare-aks-devops-deployment "
Compare Python vs Node.js for ML inference API.
Team has Python expertise, need fast inference.
"
```

### Example 2: Deployment Strategy

```
/compare-aks-devops-deployment "
Compare canary vs blue/green for payment service.
Zero-downtime required, medium traffic volume.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/aks-devops-deployment/aks-devops-deployment-constitution.md`
- **Framework Guide**: Constitution Section VIII
- **Related**: scaffold-aks-devops-deployment, refactor-aks-devops-deployment
