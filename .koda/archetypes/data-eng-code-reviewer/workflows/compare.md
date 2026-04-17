---
description: Perform a deep architectural and code quality review against the Code Reviewer Constitution.
---

User input: $ARGUMENTS

# Compare & Review Workflow

## Mission Statement
Establish a AI assisted, consistent code and peer review practice that improves correctness, security, performance, and maintainability—so every change is understandable, testable, and safe to operate in production.

This workflow executes a "loud but subtle" review of generated or modified assets.

## Execution Steps

1. **Inference (No-Git Mode)**: 
   - Scan the workspace for files modified within the last 5 minutes OR check the session history for recently created/edited files.
   - List these files for the user to confirm the review scope.

2. **Location Selection**:
   - **MANDATORY**: Ask the user: "Where should I store the `Code_Review.md` file?"
   - Default to the current project root if none provided.

3. **Checklist Execution**:
   - For each identified file, cross-reference against the **Code Reviewer Constitution**.
   - **Understandability**: Ensure naming, structure, and documentation are clear.
   - **Testability**: Verify that the change can be validated (unit/integration checks).
   - **Production Safety**: Check for idempotency, error handling, and security.
   - Flag all **Hard-Stop Rules (✘)** with loud warning headers.
   - Group **Mandatory Patterns (✔)** suggestions in a "Quality Improvements" section for a subtle yet clear delivery.

4. **Remediation Suggestions**:
   - Generate specific code snippets for fixing each identified violation.
   - Do NOT run the fixes; instead, provide them as "Fix-it" recommendations within the `Code_Review.md`.

5. **Output Generation**:
   - Save the consolidated review to the user-specified location as `Code_Review.md`.

## Error Handling
- If no files are identified as changed, ask the user to specify files to review.
- If the Constitution is missing, abort and request /scaffold-code-reviewer.

## Examples
- Reviewing a new Snowflake MERGE script for fan-out risks and audit columns.
- Checking a Python ETL script for memory management and credential leakage.

## References
- [code-reviewer-constitution.md](../../code-reviewer-constitution.md)

## Examples

```bash
# Compare local changes against the constitution
/compare-code-reviewer --scope local
```
