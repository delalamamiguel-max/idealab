---
description: Compare Databricks deployment approaches, CLI strategies, and workflow patterns
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Comparison Scope

Extract from $ARGUMENTS:
- Items to compare (approaches, scripts, configurations)
- Comparison criteria (speed, security, maintainability)
- Use case context

**Common Comparisons:**
- Git-based vs Workspace-based deployment
- Bash vs Python deployment scripts
- Manual CLI vs automated pipeline
- Development vs production workflow patterns

### 2. Gather Comparison Data

**For Deployment Approach Comparison:**

| Aspect | Git-Based (Approach 1) | Workspace-Based (Approach 2) |
|--------|------------------------|------------------------------|
| **Use Case** | Production, CI/CD | Rapid development, testing |
| **Version Control** | Built-in via Git | Manual or none |
| **Deployment Speed** | Slower (commit required) | Faster (direct push) |
| **Audit Trail** | Complete Git history | Limited |
| **Collaboration** | Code review enforced | Direct changes |
| **Rollback** | Easy via Git revert | Manual backup required |

**For Script Type Comparison:**

| Aspect | Bash Scripts | Python Scripts |
|--------|--------------|----------------|
| **Portability** | Unix/Mac only | Cross-platform |
| **Error Handling** | Basic | Rich exception handling |
| **JSON Processing** | Requires jq | Native support |
| **Complexity** | Simple operations | Complex logic |
| **Maintainability** | Lower for complex | Higher for complex |

### 3. Apply Comparison Framework

Evaluate against constitution guidelines:

**Security Considerations:**
- Credential handling approach
- Audit trail completeness
- Access control enforcement

**Reliability Considerations:**
- Error handling robustness
- Retry logic support
- Monitoring integration

**Operational Considerations:**
- Deployment speed requirements
- Team skill set
- Maintenance burden

### 4. Generate Comparison Matrix

Create structured comparison with scoring:
- Security: How well does it protect credentials and audit access?
- Reliability: How robust is error handling and recovery?
- Speed: How quickly can deployments happen?
- Maintainability: How easy is it to update and debug?
- Compliance: How well does it meet constitution standards?

### 5. Provide Recommendation

Based on comparison and use case:
- Declare recommended approach with justification
- Note trade-offs and when alternative is better
- Provide migration path if switching approaches

## Error Handling

**Insufficient Context**: Ask for specific use case details.

**Mixed Requirements**: Recommend hybrid approach if applicable.

## Examples

### Example 1: Deployment Approach

```
/compare-databricks-developer-workflow "
Compare Git-based vs Workspace-based deployment for our team.
Context: 5-person data engineering team
Use case: Mix of rapid prototyping and production pipelines
"
```

### Example 2: Script Implementation

```
/compare-databricks-developer-workflow "
Should we use bash or Python for our deployment scripts?
Current: Bash scripts with some reliability issues
Need: Better error handling and cross-platform support
"
```

### Example 3: Workflow Patterns

```
/compare-databricks-developer-workflow "
Compare manual CLI deployment vs CI/CD automated pipeline.
Current state: Manual deployments causing inconsistency
Goal: Standardized, repeatable deployments
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/databricks-developer-workflow/databricks-developer-workflow-constitution.md`
- **Approach Details**: Constitution Section 2.2 - Notebook Development Workflow
- **Script Examples**: Constitution Section V - CLI Operations Reference
