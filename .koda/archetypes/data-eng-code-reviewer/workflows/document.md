---
description: Document the Code Reviewer's protocols and constitutional rules.
---

User input: $ARGUMENTS

# Document Code Reviewer Workflow

## Mission Statement
Establish a AI assisted, consistent code and peer review practice that improves correctness, security, performance, and maintainability—so every change is understandable, testable, and safe to operate in production.

## Execution Steps

1. **Constitutional Synching**:
   - Update `README.md` and `code-reviewer-constitution.md` to ensure the Mission Statement is front and center.

2. **Runbook Update**:
   - Detail the manual invocation: `@code-reviewer /compare`.

## References
- [README.md](../../README.md)
- [code-reviewer-constitution.md](../../code-reviewer-constitution.md)

## Error Handling

If documentation generation fails:
1. Verify the archetype structure aligns with standard patterns.
2. Check write permissions for the target directory.
3. Ensure no referenced files are missing.

## Examples

```bash
# Generate documentation for the current version
/document-code-reviewer --output ./docs/v1.0
```
