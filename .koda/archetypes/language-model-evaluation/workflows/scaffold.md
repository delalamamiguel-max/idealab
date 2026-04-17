---
description: Scaffold language model evaluation pipeline with custom graders and async Evaluator (Language Model Evaluation)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype language_model_evaluation` and ensure ENV_VALID. Halt if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/env-config.yaml` for approved runtimes, LLM endpoints, and security configuration

### 3. Parse Input
Extract from $ARGUMENTS: evaluation purpose, data source details, model response format, required evaluation dimensions, grader types (heuristic vs LLM judge), output format preferences, decision criteria. Request comprehensive specification if incomplete (refer user to template at `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/language-model-evaluation.yaml`).

### 4. Validate Constraints
Enforce hard stops:
- ✘ Reject graders not inheriting from `BaseGrader` with async `grade()` method
- ✘ Block incomplete `EvaluationInput` schemas (missing `response` field)
- ✘ Require error handling populating `GradeResult.error` without blocking other graders
- ✘ Refuse unbounded concurrency (require semaphore limits via `Evaluator`)
- ✘ Block hardcoded LLM credentials (require Key Vault or env vars)
- ✘ Require MLflow logging for evaluation runs
- ✘ Demand output validation before persistence

### 5. Generate Evaluation Pipeline Scaffold
Provide scaffold including:
- YAML configuration file for evaluation settings (data source, graders, thresholds, output)
- Python script with core framework imports (`EvaluationInput`, `GradeResult`, `BaseGrader`, `Evaluator`)
- Heuristic grader implementations based on specified dimensions (length, format, keywords)
- LLM judge grader implementations with prompt templates for specified dimensions (correctness, safety, helpfulness)
- Data loading module supporting file (CSV/JSONL/Parquet), API, database, and streaming sources
- Async evaluator orchestration with concurrency control
- Results aggregation and analysis (mean, median, pass rates, grouped metrics)
- Decision criteria checking (hard-stops vs targets)
- Prose report generation (Markdown/HTML/PDF) with executive summary, per-grader analysis, failure highlights
- MLflow integration for tracking evaluation metadata, grader configs, results, and artifacts
- Example usage notebook demonstrating end-to-end pipeline

### 6. Recommended Enhancements
Suggest optional additions:
- Visualization generation (score distributions, grader comparisons, outlier analysis)
- Real-time evaluation mode for production inference monitoring
- Benchmark tracking for regression detection across model versions
- Fairness analysis graders for demographic parity and equal opportunity
- Synthetic test case generation for adversarial robustness testing
- Explainability integration linking evaluation to model interpretability artifacts

### 7. Validate and Report

## Error Handling
- Hard-stop triggered: Halt scaffold, cite violated clause (e.g., "Hardcoded credentials detected"), provide Key Vault integration guide
- Missing inputs: Request complete specification, share YAML template and natural language template from constitution
- Tooling gap: Flag absent MLflow access, LLM API credentials, or Key Vault permissions; reference env-config setup
- Grader configuration unclear: Provide examples of heuristic logic and LLM judge prompt templates from grader library
- Governance conflicts: Escalate if safety/fairness requirements undefined or decision criteria ambiguous

## Examples
- **Example 1**: `/scaffold-language-model-evaluation Build evaluation pipeline for customer support chatbot with correctness and safety graders`
- **Example 2**: `/scaffold-language-model-evaluation Create LLM evaluation framework for code generation model with format validation and helpfulness scoring`
- **Example 3**: `/scaffold-language-model-evaluation Design evaluation pipeline for summarization model with ROUGE, fluency, and factuality graders`

## References
Constitution: (pre-loaded above) | Config: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/env-config.yaml` | Template: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/language-model-evaluation.yaml` | Grader Library: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/grader-library.py`
