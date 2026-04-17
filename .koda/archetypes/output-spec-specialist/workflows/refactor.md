---
description: Improve existing output schemas for better validation and compatibility (Output Spec Specialist)
---

User input: $ARGUMENTS

## Execution Steps
1. Parse Input - schema path, goal
2. Analyze schema completeness
3. Add missing validations
4. Improve field descriptions
5. Update version

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide output name, target format (JSON/Pydantic), and validation mode (strict/lenient). |
| `output-spec-specialist-constitution.md` not found | Stop. Ensure file is present at repo root. |
| `pydantic` not installed | Run `pip install pydantic>=2.0`. |
| Schema validation rejects valid output | Review field constraints — check `min_length`, `pattern`, and required fields against actual agent output format. |
| JSON parse fails on agent output | Agent is not returning valid JSON. Add output parser with retry logic using LangChain's `OutputFixingParser`. |
| Schema registry URL unreachable | Set `SCHEMA_REGISTRY_URL` env var or operate in local-only mode (remove registry push steps). |

## Examples
**Example**: `/refactor-output-spec-specialist schemas/entity.py validation`
