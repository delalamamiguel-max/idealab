---
description: Debug language model evaluation pipeline failures, grader errors, and async issues (Language Model Evaluation)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype language_model_evaluation` and ensure ENV_VALID. Halt if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/env-config.yaml` for runtime settings and troubleshooting

### 3. Parse Input and Identify Issue
Extract from $ARGUMENTS: error description, stack trace, evaluation run ID, failing grader names, data sample causing failure, expected vs actual behavior. Categorize issue type: grader failure, data loading, async/concurrency, output validation, MLflow logging, LLM API error.

### 4. Diagnose Root Cause

#### Grader Failures
- **Check exception handling**: Verify graders catch exceptions and populate `GradeResult.error` field without raising
- **Inspect grader logic**: Review `compute_score()` implementation for null pointer errors, type mismatches, division by zero
- **Validate input data**: Confirm `EvaluationInput` has required fields (`response` present, optional fields handled gracefully)
- **Test grader isolation**: Run single grader on sample input to isolate failure
- **Check LLM judge prompts**: Verify placeholders (`{response}`, `{prompt}`, `{system_prompt}`) are properly formatted
- **Inspect parser logic**: For LLM judges, validate score extraction from raw LLM response

#### Data Loading Issues
- **Validate column mappings**: Confirm configured column names exist in source data
- **Check required columns**: Verify `response` column is present (hard-stop requirement)
- **Inspect data types**: Ensure columns map to correct types (strings for text fields, dicts for context)
- **Test data sample**: Load first 10 rows to identify format issues early
- **Validate context fields**: Check context columns are properly deserialized to dict

#### Async/Concurrency Problems
- **Check semaphore limits**: Verify `max_concurrency` is set appropriately for environment
- **Inspect event loop**: Ensure evaluation runs in proper async context (`asyncio.run()`)
- **Test sequential execution**: Reduce `max_concurrency=1` to eliminate race conditions
- **Validate async patterns**: Confirm all graders use `async def grade()` signature
- **Check timeout settings**: Verify `timeout_seconds` is sufficient for LLM API calls

#### LLM API Errors
- **Validate credentials**: Confirm API key is accessible from Key Vault or env vars (no hardcoding)
- **Check rate limits**: Verify `max_concurrency` respects API provider limits
- **Inspect retry logic**: Confirm `retry_on_error=true` and `max_retries` are configured
- **Test API connectivity**: Make direct API call with same credentials to isolate issue
- **Validate LLM callable**: Check `llm_callable` function signature and error handling

#### Output Validation Failures
- **Check structured output**: Verify DataFrame has expected columns (`{grader_name}_score`, `{grader_name}_reasoning`)
- **Inspect prose report**: Validate Markdown/HTML rendering and completeness of sections
- **Validate aggregation**: Confirm metrics (mean, median, pass rates) compute correctly
- **Check decision criteria**: Verify hard-stops and targets are evaluated properly
- **Test MLflow logging**: Confirm experiment run ID, artifacts upload successfully

### 5. Implement Fix
Based on root cause:
- **Grader bug**: Patch `compute_score()` logic, add null checks, handle edge cases
- **Data format**: Update column mappings in YAML config, add data validation step
- **Async issue**: Adjust concurrency limits, add timeout handling, fix event loop usage
- **API error**: Rotate credentials, implement exponential backoff, add circuit breaker
- **Output bug**: Fix aggregation logic, repair report template, validate MLflow schema

### 6. Add Regression Prevention
- **Unit test**: Create test case reproducing failure with synthetic data
- **Error logging**: Add detailed logging at failure point for future debugging
- **Validation**: Add upfront checks preventing similar failures (e.g., column existence check)
- **Documentation**: Update README with troubleshooting guidance for this issue class

### 7. Validate and Report

## Error Handling
- Cannot reproduce: Request complete stack trace, evaluation config YAML, sample data
- Multiple failures: Triage by severity (hard-stop violations first, then errors, then warnings)
- Systemic issue: Escalate if problem affects core framework classes or constitutional requirements
- LLM API outage: Provide fallback strategy (skip LLM judges, use heuristics only, queue for retry)

## Examples
- **Example 1**: `/debug-language-model-evaluation Grader 'correctness_judge' raises KeyError on missing context field`
- **Example 2**: `/debug-language-model-evaluation Evaluation hangs indefinitely at 50% progress`
- **Example 3**: `/debug-language-model-evaluation OpenAI API returns 429 rate limit error for all samples`
- **Example 4**: `/debug-language-model-evaluation Prose report generation fails with UnicodeDecodeError`
- **Example 5**: `/debug-language-model-evaluation MLflow artifact upload succeeds but results DataFrame is empty`

## References
Constitution: (pre-loaded above) | Config: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/env-config.yaml` | Grader Library: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/grader-library.py` | Pipeline Example: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/evaluation-pipeline-example.py`
