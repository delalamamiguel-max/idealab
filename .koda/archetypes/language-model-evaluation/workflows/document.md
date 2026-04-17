---
description: Generate comprehensive documentation for language model evaluation pipeline (Language Model Evaluation)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype language_model_evaluation` and ensure ENV_VALID. Halt if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load evaluation configuration from YAML or extract from code/MLflow

### 3. Parse Input and Identify Documentation Scope
Extract from $ARGUMENTS: documentation type (grader specifications, evaluation runbook, governance report, stakeholder brief), target audience (technical team, data scientists, executives, auditors), format preference (Markdown, HTML, PDF, Confluence). Determine completeness level: quick reference vs comprehensive guide.

### 4. Generate Documentation

#### Grader Specifications Documentation
**Purpose**: Technical reference for grader library

**Contents**:
```markdown
# Grader Library Documentation

## Overview
This document catalogs all available graders for LLM evaluation, including implementation details, usage examples, and configuration guidance.

## Grader Catalog

### Heuristic Graders

#### LengthCheckGrader
**Purpose**: Validates response length falls within acceptable range

**Parameters**:
- `min_length` (int): Minimum acceptable character count (default: 50)
- `max_length` (int): Maximum acceptable character count (default: 500)

**Scoring Logic**:
- Score 1.0 if `min_length ≤ length ≤ max_length`
- Score 0.5 if slightly outside range (±20 chars for min, ±50 for max)
- Score 0.0 if far outside range

**Usage Example**:
\```python
grader = LengthCheckGrader(min_length=100, max_length=1000)
result = await grader.grade(evaluation_input)
\```

**When to Use**:
- Validating summary or snippet length requirements
- Enforcing token limits for downstream systems
- Detecting truncation or padding issues

**Limitations**:
- Does not assess quality, only length
- Character count may not correlate with token count
- Language-specific considerations (e.g., CJK characters)

---

#### FormatValidatorGrader
[Similar structure for each grader]

### LLM Judge Graders

#### CorrectnessJudge
**Purpose**: Evaluates factual correctness against ground truth

**Parameters**:
- `judge_prompt_template` (str): Evaluation instructions for LLM
- `llm_callable` (async function): LLM API client
- `parser` (function): Score extraction logic (default: regex-based)

**Judge Prompt Template**:
\```
You are evaluating the factual correctness of a model response.

Prompt: {prompt}
Response: {response}
Ground Truth: {context[ground_truth]}

Rate the correctness on a scale of 0-10 where:
- 10: Completely correct and accurate
- 5: Partially correct with some errors
- 0: Completely incorrect

Provide your rating in the format: "Score: X"
Then explain your reasoning.
\```

**Scoring Logic**:
- LLM evaluates response semantically against ground truth
- Parser extracts numeric score from LLM response text
- Reasoning field captures LLM explanation

**Usage Example**:
\```python
async def openai_callable(prompt: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

judge = LLMJudge(
    name="correctness_judge",
    judge_prompt_template=CORRECTNESS_TEMPLATE,
    llm_callable=openai_callable
)
\```

**When to Use**:
- Assessing factual accuracy when ground truth is available
- Comparing model outputs to reference answers
- Evaluating semantic equivalence beyond exact string match

**Limitations**:
- Requires LLM API access (cost, latency, rate limits)
- Judge quality depends on LLM capability
- Non-deterministic (may vary across runs)
- Requires ground truth in context

**Cost Considerations**:
- OpenAI GPT-4: ~$0.03 per 1K tokens (~200 evaluations)
- Can be reduced with smaller models (GPT-3.5, Claude Haiku)

---

[Continue for all graders]

## Custom Grader Development

### Creating a Heuristic Grader
[Step-by-step guide with code examples]

### Creating an LLM Judge
[Step-by-step guide with prompt engineering tips]

## Best Practices
- Start with heuristics for fast iterations
- Add LLM judges for semantic dimensions
- Validate graders on sample data before production
- Monitor costs and latency in production
```

#### Evaluation Runbook Documentation
**Purpose**: Operational guide for running evaluations

**Contents**:
- **Prerequisites**: Environment setup, credentials, data requirements
- **Quick Start**: Minimal example to run first evaluation
- **Configuration Guide**: YAML file breakdown with all options
- **Running Evaluations**: Step-by-step command sequences
- **Output Interpretation**: How to read results, reports, metrics
- **Troubleshooting**: Common errors and fixes
- **Monitoring**: MLflow dashboard, alerts, SLO tracking
- **Maintenance**: Updating graders, rotating credentials, upgrading dependencies

#### Governance Report Documentation
**Purpose**: Compliance evidence for auditors and stakeholders

**Contents**:
```markdown
# LLM Evaluation Governance Report

## Constitutional Compliance

### Hard-Stop Rule Adherence
✅ All graders inherit from `BaseGrader` with async `grade()` method
✅ Error handling populates `GradeResult.error` without blocking
✅ Concurrency controlled via `Evaluator` semaphore (max_concurrency=5)
✅ Credentials sourced from Key Vault (scope: llm-evaluation)
✅ MLflow tracking enabled for all evaluation runs
✅ Output validation performed before artifact persistence

### Mandatory Pattern Implementation
✅ Comprehensive YAML specification provided upfront
✅ Standardized data structures (`EvaluationInput`, `GradeResult`) used throughout
✅ Async patterns implemented correctly across all graders
✅ LLM judge prompts use placeholder syntax (`{response}`, `{prompt}`)
✅ Multi-source data support (CSV, JSONL, Parquet)
✅ Decision criteria with hard-stops and targets defined
✅ MLflow integration logging grader configs and results

## Evaluation Evidence

### Evaluation Run: customer-support-chatbot-eval-2025-12-01

**Metadata**:
- Run ID: `abc123def456`
- Timestamp: `2025-12-01 10:00:00 UTC`
- Samples: 1,000
- Graders: 5 (3 heuristic, 2 LLM judge)
- Duration: 8 minutes 32 seconds
- Cost: $1.50 (OpenAI API)

**Decision**:
- ✅ **PASSED** all hard-stop criteria
- ⚠️ 1 target miss (length_check: 0.68 < 0.70 target)

**Hard-Stop Results**:
| Grader | Threshold | Actual | Status |
|--------|-----------|--------|--------|
| safety_judge | ≥ 0.90 | 0.94 | ✅ PASS |
| format_validator | = 1.00 | 1.00 | ✅ PASS |

**Target Results**:
| Grader | Target | Actual | Status |
|--------|--------|--------|--------|
| correctness_judge | ≥ 7.0 | 7.8 | ✅ MET |
| length_check | ≥ 0.70 | 0.68 | ⚠️ MISS |

**Artifacts**:
- Raw results: `mlflow://artifacts/abc123/evaluation_results.csv`
- Prose report: `mlflow://artifacts/abc123/evaluation_report.md`
- Visualizations: `mlflow://artifacts/abc123/plots/`

## Approval Status

**Approved For**: Production Deployment
**Approver**: Jane Doe (ML Engineering Lead)
**Approval Date**: 2025-12-01
**Comments**: Passed all hard-stops. Length target miss is minor and acceptable given overall quality. Recommend monitoring length distribution in production.

## Audit Trail

| Timestamp | Event | User | Details |
|-----------|-------|------|---------|
| 2025-12-01 09:45 | Evaluation Started | john.smith@company.com | Config: customer-support-v2.yaml |
| 2025-12-01 09:53 | Evaluation Completed | system | 1000/1000 samples processed |
| 2025-12-01 09:55 | Decision: PASS | system | All hard-stops met |
| 2025-12-01 10:15 | Approval | jane.doe@company.com | Approved for production |
```

#### Stakeholder Brief Documentation
**Purpose**: Executive summary for non-technical stakeholders

**Contents**:
- **Executive Summary**: One-paragraph overview of evaluation results
- **Key Findings**: Bullet points highlighting main takeaways
- **Model Quality Assessment**: Pass/fail status with context
- **Risk Assessment**: Any concerns or limitations identified
- **Recommendations**: Next steps (deploy, iterate, retest)
- **Visualizations**: Charts showing score distributions, pass rates
- **Glossary**: Explain technical terms (grader, LLM judge, hard-stop, etc.)

### 5. Generate Cross-References
Link documentation to:
- Constitution: (pre-loaded above)
- Templates: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/`
- Workflows: `.windsurf/workflows/02-ml-operations-lifecycle/language-model-evaluation/`
- MLflow experiments: Provide dashboard links
- Related archetypes: `model-architect`, `inference-orchestrator`, `interpretability-analyst`

### 6. Package and Publish
- **Version documentation**: Add version number, last updated date
- **Format conversion**: Generate HTML/PDF if requested from Markdown source
- **Publish**: Upload to Confluence, SharePoint, or documentation portal
- **Notify stakeholders**: Email/Slack notification with link

### 7. Validate and Report
Confirm documentation completeness:
- All sections present and non-empty
- Code examples are syntactically correct
- Links and cross-references resolve
- Audience-appropriate language and detail level

## Error Handling
- Missing information: Request access to evaluation run ID, MLflow artifacts, YAML config
- Sensitive data: Redact PII, credentials, proprietary information before publishing
- Version conflicts: Clarify which evaluation run or code version to document

## Examples
- **Example 1**: `/document-language-model-evaluation Generate grader library reference for data science team`
- **Example 2**: `/document-language-model-evaluation Create governance compliance report for audit`
- **Example 3**: `/document-language-model-evaluation Produce executive brief on chatbot evaluation results for VP`
- **Example 4**: `/document-language-model-evaluation Write operational runbook for MLOps team`
- **Example 5**: `/document-language-model-evaluation Generate HTML documentation for internal wiki`

## References
Constitution: (pre-loaded above) | Templates: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/` | Grader Library: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/grader-library.py` | Pipeline Example: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/evaluation-pipeline-example.py`
