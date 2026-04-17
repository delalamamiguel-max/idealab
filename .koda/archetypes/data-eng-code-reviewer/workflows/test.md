---
description: Test the Code Reviewer's effectiveness against known bad patterns.
---

User input: $ARGUMENTS

# Test Code Reviewer Workflow

## Mission Statement
Establish a AI assisted, consistent code and peer review practice that improves correctness, security, performance, and maintainability—so every change is understandable, testable, and safe to operate in production.

## Execution Steps

1. **Synthetic Violation Loading**:
   - Inject intentional ✘ (Hard-Stop) violations into a temp file (e.g., hardcoded secrets, large memory load).

2. **Detection Verification**:
   - Run `/compare-code-reviewer` and verify that ALL synthetic violations are detected and flagged "loudly".

3. **Report Validation**:
   - Verify `Code_Review.md` contains accurate "Fix-it" suggestions.

## Error Handling
- Fail test if ✘ rules are missed.

## References
- [code-reviewer-constitution.md](../../code-reviewer-constitution.md)

## Examples

```bash
# Run a full test suite against the archetype
/test-code-reviewer --test-suite full
```
