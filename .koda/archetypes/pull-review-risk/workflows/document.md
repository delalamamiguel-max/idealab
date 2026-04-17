---
description: Generate documentation for pull review risk methodology and reports
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Scope

Extract from $ARGUMENTS:
- Documentation type (methodology, report summary, playbook)
- Target audience

### 2. Generate Documentation

Create:
- Risk analysis methodology
- Governance matrix explanation
- Standard notation reference
- Response playbook

### 3. Deliver

Output documentation in requested format.

## Error Handling

**Missing Context**: Request specific report or focus area.

## Examples

```
/document-pull-review-risk "Create risk response playbook for team"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/pull-review-risk/pull-review-risk-constitution.md`
