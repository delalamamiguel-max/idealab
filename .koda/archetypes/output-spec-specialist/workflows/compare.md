---
description: Compare output schema approaches for parse success and flexibility (Output Spec Specialist)
---

User input: $ARGUMENTS

## Execution Steps
1. Parse Input - schemas to compare
2. Test parse success rates
3. Compare flexibility
4. Recommend approach

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
**Example**: `/compare-output-spec-specialist "strict vs flexible" parse_rate`
