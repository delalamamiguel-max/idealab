# language-model-evaluation Constitution

## Purpose

Establishes disciplined LLM evaluation practices using custom grader frameworks (heuristic and LLM-based judges), async orchestration, and comprehensive specification-driven workflows for assessing language model outputs across multiple dimensions (correctness, safety, helpfulness, format compliance).

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** any approach that:

- ✘ **Skips grader validation**: All graders must inherit from `BaseGrader` and implement async `grade()` method returning `GradeResult`.
- ✘ **Uses incomplete input schemas**: All `EvaluationInput` objects must include `response` field; prompt/system_prompt/context are optional.
- ✘ **Ignores error handling**: Grader exceptions must return `GradeResult` with populated `error` field without blocking other graders.
- ✘ **Allows unbounded concurrency**: `Evaluator` must use semaphore-based concurrency limits (max_concurrency parameter).
- ✘ **Hardcodes LLM credentials**: LLM judge API keys must use environment variables or Key Vault integration.
- ✘ **Skips evaluation logging**: All evaluation runs must log configuration, graders, and results to MLflow or equivalent tracking system.
- ✘ **Omits output validation**: Prose reports and structured outputs must validate completeness and correctness before persistence.

## II. Mandatory Patterns (Must Apply)

The LLM **must** ensure:

### Specification & Configuration
- ✔ **Comprehensive specification upfront**: Prefer single detailed prompt or YAML config over iterative refinement to maximize efficiency.
- ✔ **Complete specification template**: If specification is incomplete, provide full template covering: data source, response format, graders, evaluation settings, output requirements, and decision criteria.
- ✔ **YAML configuration support**: Support structured YAML configuration following template at `.cdo-aifc/templates/02-ml-operations-lifecycle/language-model-evaluation/language-model-evaluation.yaml`.

### Core Framework Architecture
- ✔ **Standardized data structures**: Use `EvaluationInput` dataclass with fields: `response` (required), `prompt`, `system_prompt`, `context` dict.
- ✔ **Standardized result format**: Use `GradeResult` dataclass with fields: `grader_name`, `score`, `reasoning`, `metadata`, `error`.
- ✔ **BaseGrader abstraction**: All graders inherit from `BaseGrader` abstract class with async `grade(input_data: EvaluationInput) -> GradeResult` method.
- ✔ **Heuristic grader pattern**: Heuristic graders inherit from `Heuristic` base class and implement `compute_score()` returning `(score, reasoning, metadata)` tuple.
- ✔ **LLM judge pattern**: LLM judges use composition with `judge_prompt_template`, `llm_callable`, and optional `parser` for score extraction.

### Async Orchestration
- ✔ **Async grader implementation**: All graders implement async pattern using `async def grade()` for concurrency support.
- ✔ **Evaluator orchestration**: Use `Evaluator` class with semaphore-controlled concurrency for batch evaluation.
- ✔ **Error resilience**: Failed graders populate `error` field in `GradeResult` but don't block evaluation of other graders.
- ✔ **Concurrent execution**: Run multiple graders in parallel using `asyncio.gather()` with semaphore protection.

### Grader Configuration
- ✔ **LLM judge prompt templates**: Judge prompts use placeholders: `{response}`, `{prompt}`, `{system_prompt}`, `{context}` for dynamic formatting.
- ✔ **Parser flexibility**: Support default regex-based parser or custom parsers for structured LLM output extraction.
- ✔ **Score range documentation**: Document expected score ranges for each grader (e.g., 0-1, 0-10, 1-5).
- ✔ **Threshold configuration**: Define hard-stop thresholds (must exceed) and target thresholds (should exceed) per grader.

### Data Loading & Processing
- ✔ **Multi-source support**: Support file-based (CSV, JSONL, Parquet), API-based, database, and streaming data sources.
- ✔ **Column mapping validation**: Validate required columns (`response` minimum) and map to `EvaluationInput` fields.
- ✔ **Context preservation**: Preserve metadata fields (IDs, ground truth, scenario types) in `context` dict for grader access.

### Output & Persistence
- ✔ **Aggregation and analysis**: Compute summary statistics (mean, median, pass rates) per grader and optionally group by scenario/task type.
- ✔ **Structured output formats**: Support CSV, JSON, Parquet output formats with configurable columns (scores, reasoning, metadata, errors).
- ✔ **Prose report generation**: Generate human-readable reports (Markdown, HTML, PDF) with executive summary, per-grader analysis, failure highlights, and recommendations.
- ✔ **Artifact persistence**: Save raw results, aggregated metrics, prose reports, and visualizations to versioned storage.
- ✔ **MLflow integration**: Log evaluation metadata (grader configs, thresholds, data source), results, and artifacts as MLflow experiment run.

### Decision Criteria & Governance
- ✔ **Hard-stop enforcement**: Block promotion if any grader with hard-stop threshold fails (e.g., safety_judge < 0.9).
- ✔ **Target threshold tracking**: Track graders with target thresholds and flag when targets not met (warning, not blocker).
- ✔ **Promotion rules**: Document promotion logic (e.g., "all hard-stops pass and targets met", "safety pass only").
- ✔ **Governance integration**: Link evaluation results to approval workflows, tickets, and CI checks where applicable.

## III. Preferred Patterns (Recommended)

The LLM **should** adopt:

- ➜ **Modular grader library**: Build reusable grader catalog for common dimensions (correctness, safety, format, helpfulness, relevance, style).
- ➜ **Visualization artifacts**: Generate plots for score distributions, grader comparisons, outlier analysis, and correlation matrices.
- ➜ **Real-time evaluation mode**: Support streaming evaluation for production inference monitoring and online model assessment.
- ➜ **Benchmark tracking**: Track evaluation metrics over time to detect regression in model quality across versions.
- ➜ **Fairness analysis**: Include fairness graders for demographic parity, equal opportunity when evaluating on sensitive attributes.
- ➜ **Synthetic test cases**: Generate synthetic edge cases and adversarial examples for robustness testing.
- ➜ **Explainability integration**: Link evaluation results with model interpretability artifacts (SHAP, attention weights).

---

**Version**: 1.0.0  
**Last Updated**: 2025-12-01  
**Source**: Converted from verbose workflow specification to standardized constitution format  
**Template Reference**: `.cdo-aifc/templates/02-ml-operations-lifecycle/language-model-evaluation/`  
**Original Source**: See `.cdo-aifc/templates/02-ml-operations-lifecycle/language-model-evaluation/` for detailed specifications, YAML configs, and code examples
