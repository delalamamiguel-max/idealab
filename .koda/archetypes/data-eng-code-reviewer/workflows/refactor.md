---
description: Refactor existing code review rules and "Fix-it" snippet logic.
---

User input: $ARGUMENTS

# Refactor Code Reviewer Workflow

## Mission Statement
Establish a AI assisted, consistent code and peer review practice that improves correctness, security, performance, and maintainability—so every change is understandable, testable, and safe to operate in production.

## Execution Steps

1. **Rule Modernization**:
   - Update `code-reviewer-constitution.md` with new standards or improved mission-aligned rules.
   - Refactor "Fix-it" snippets in `Code_Review.md` to be more understandable and testable.

2. **Loop Control**:
   - Ensure the 2-step review loop is strictly enforced.

## Error Handling
- Do not refactor rules to be less safe.

## References
- [code-reviewer-constitution.md](../../code-reviewer-constitution.md)

## Examples

```bash
# Refactor the constitution to improve readability
/refactor-code-reviewer --target ./code-reviewer-constitution.md --focus readability
```
