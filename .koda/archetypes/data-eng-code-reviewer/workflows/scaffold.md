---
description: Scaffolding a new instance of a code review process or checklist.
---

User input: $ARGUMENTS

# Scaffold Code Reviewer Workflow

## Mission Statement
Establish a AI assisted, consistent code and peer review practice that improves correctness, security, performance, and maintainability—so every change is understandable, testable, and safe to operate in production.

## Execution Steps

1. **Constitutional Alignment**:
   - Ensure the `code-reviewer-constitution.md` is present and up-to-date with the mission statement.

2. **Checklist Customization**:
   - If a specific project type is detected (Snowflake, Python, etc.), prepare the project-specific review checklists.

3. **Asset Preparation**:
   - Create local placeholders or templates for `Code_Review.md` if requested.

## Error Handling
- Abort if the target project base is not set.

## References
- [code-reviewer-constitution.md](../../code-reviewer-constitution.md)

## Examples

```bash
# Create a new code review checklist for a Python project
/scaffold-code-reviewer --project-type python --output ./docs/review_checklist.md
```
