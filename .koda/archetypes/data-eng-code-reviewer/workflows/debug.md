---
description: Debugging the Code Reviewer's own logic or rules.
---

User input: $ARGUMENTS

# Debug Code Reviewer Workflow

## Mission Statement
Establish a AI assisted, consistent code and peer review practice that improves correctness, security, performance, and maintainability—so every change is understandable, testable, and safe to operate in production.

## Execution Steps

1. **Rule Validation**:
   - Check if the reviewer is mis-identifying violations.
   - Analyze the `Code_Review.md` generation logic for false positives.

2. **Regex/Pattern Check**:
   - Verify SQL/Python/TWS parsing patterns against the constitution.

## Error Handling
- Use the Debug Archetype results to trace logical flaws in the review engine.

## References
- [code-reviewer-constitution.md](../../code-reviewer-constitution.md)

## Examples

```bash
# Debug why a rule is firing incorrectly
/debug-code-reviewer --rule "No Hardcoded Secrets" --file ./src/app.py
```
