---
description: Analyze pull requests for production risks, security vulnerabilities, and governance compliance
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Gather PR Information

Extract from $ARGUMENTS:
- PR URL or branch name
- Target files or modules
- Review scope (full, security-only, performance-only)

### 2. Scan for Production Risks

Analyze code for:
- Serialization vulnerabilities
- Error handling gaps
- Performance bottlenecks
- Hardcoded values/secrets
- Security flaws

### 3. Apply Governance Matrix

Assess against constitution standards:
- Hard-stop violations (HS-*)
- Mandatory gaps (M-*)
- Preferred pattern adoption

### 4. Generate Risk Report

Create HTML report with:
- Findings by type and severity
- Governance matrix scores
- Constitution compliance
- Action items and recommendations

## Error Handling

**No PR Specified**: Request PR URL or branch name.

## Examples

```
/scaffold-pull-review-risk "Review PR #123 for security risks"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/pull-review-risk/pull-review-risk-constitution.md`
