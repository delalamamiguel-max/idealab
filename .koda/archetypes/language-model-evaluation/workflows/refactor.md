---
description: Refactor language model evaluation pipeline for improved maintainability, performance, and compliance (Language Model Evaluation)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype language_model_evaluation` and ensure ENV_VALID. Halt if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/env-config.yaml` for target standards

### 3. Parse Input and Identify Refactoring Scope
Extract from $ARGUMENTS: code location (grader implementations, evaluation orchestration, output generation, MLflow integration), refactoring goal (improve error handling, optimize concurrency, enhance report quality, add visualizations, strengthen compliance), specific pain points. Prioritize refactorings: constitutional violations first, then performance, then code quality.

### 4. Execute Refactorings

#### Grader Implementation Refactoring
**Extract Common Patterns**:
```python
# Before: Duplicated error handling across graders
class LengthCheckGrader(Heuristic):
    def compute_score(self, input_data):
        try:
            length = len(input_data.response)
            # scoring logic
        except Exception as e:
            return 0.0, f"Error: {e}", {}

# After: Centralized error handling in base class
class Heuristic(BaseGrader):
    async def grade(self, input_data):
        try:
            score, reasoning, metadata = self.compute_score(input_data)
            return GradeResult(grader_name=self.name, score=score, reasoning=reasoning, metadata=metadata)
        except Exception as e:
            return GradeResult(grader_name=self.name, score=0.0, error=str(e))
```

**Improve Null Handling**:
```python
# Before: KeyError on missing fields
context_value = input_data.context['ground_truth']

# After: Safe access with defaults
context_value = input_data.context.get('ground_truth', 'N/A')
```

**Enhance LLM Judge Parsers**:
```python
# Before: Naive regex extraction
match = re.search(r'\b\d+(\.\d+)?\b', response)
score = float(match.group(0)) if match else 0.0

# After: Robust extraction with multiple strategies
def robust_parser(response: str) -> Tuple[float, str]:
    # Strategy 1: Look for "Score: X" pattern
    match = re.search(r'Score:\s*(\d+(?:\.\d+)?)', response, re.IGNORECASE)
    if match:
        return float(match.group(1)), response
    
    # Strategy 2: Look for "X/10" or "X out of 10" pattern
    match = re.search(r'(\d+(?:\.\d+)?)\s*(?:/|out of)\s*10', response, re.IGNORECASE)
    if match:
        return float(match.group(1)), response
    
    # Strategy 3: Extract first number
    match = re.search(r'\b\d+(\.\d+)?\b', response)
    if match:
        return float(match.group(0)), response
    
    # Fallback: Return 0 with explanation
    return 0.0, f"Could not parse score from: {response[:100]}"
```

#### Evaluation Orchestration Refactoring
**Optimize Concurrency**:
```python
# Before: Fixed concurrency limit
evaluator = Evaluator(graders=graders, max_concurrency=5)

# After: Dynamic concurrency based on grader types
heuristic_count = len([g for g in graders if isinstance(g, Heuristic)])
llm_judge_count = len([g for g in graders if isinstance(g, LLMJudge)])

# Heuristics are fast, can run many in parallel
# LLM judges are rate-limited, need conservative limits
max_concurrency = min(heuristic_count + llm_judge_count * 2, 20)
evaluator = Evaluator(graders=graders, max_concurrency=max_concurrency)
```

**Add Retry Logic**:
```python
# Before: No retries on transient failures
llm_response = await self.llm_callable(formatted_prompt)

# After: Exponential backoff retries
import asyncio

async def call_llm_with_retry(callable, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await callable(prompt)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # Exponential backoff
            await asyncio.sleep(wait_time)
```

**Implement Circuit Breaker**:
```python
# Add circuit breaker for LLM API to prevent cascade failures
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")
        
        try:
            result = await func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

#### Output Generation Refactoring
**Enhance Report Quality**:
```python
# Before: Basic report
report = f"# Evaluation Report\n\nMean scores:\n"
for grader, metrics in aggregated.items():
    report += f"- {grader}: {metrics['mean']:.2f}\n"

# After: Rich report with sections, tables, and insights
def generate_rich_report(results_df, aggregated, decision, config):
    report = f"""# {config['evaluation_name']} - Evaluation Report

## Executive Summary
- **Total Samples**: {len(results_df):,}
- **Graders**: {len(aggregated)}
- **Decision**: {'✅ PASS' if decision['pass'] else '❌ FAIL'}
- **Pass Rate**: {sum(1 for _, row in results_df.iterrows() if all_graders_pass(row)) / len(results_df) * 100:.1f}%

## Per-Grader Performance

| Grader | Mean | Median | Std | Pass Rate | Status |
|--------|------|--------|-----|-----------|--------|
"""
    for grader_name, metrics in aggregated.items():
        status = "✅" if metrics['pass_rate'] > 0.8 else "⚠️"
        report += f"| {grader_name} | {metrics['mean']:.3f} | {metrics['median']:.3f} | {metrics['std']:.3f} | {metrics['pass_rate']*100:.1f}% | {status} |\n"
    
    # Add failure analysis, recommendations, etc.
    return report
```

**Add Visualization Generation**:
```python
import matplotlib.pyplot as plt
import seaborn as sns

def generate_visualizations(results_df, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # Score distributions
    score_cols = [c for c in results_df.columns if c.endswith('_score')]
    fig, axes = plt.subplots(len(score_cols), 1, figsize=(10, 4*len(score_cols)))
    for i, col in enumerate(score_cols):
        results_df[col].hist(bins=20, ax=axes[i])
        axes[i].set_title(f"{col} Distribution")
        axes[i].set_xlabel("Score")
        axes[i].set_ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/score_distributions.png", dpi=200)
    
    # Grader comparison
    mean_scores = results_df[score_cols].mean()
    plt.figure(figsize=(10, 6))
    mean_scores.plot(kind='bar')
    plt.title("Average Scores by Grader")
    plt.ylabel("Mean Score")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/grader_comparison.png", dpi=200)
```

#### MLflow Integration Refactoring
**Comprehensive Logging**:
```python
# Before: Basic logging
mlflow.log_param("num_samples", len(inputs))
mlflow.log_metric("mean_score", results_df['correctness_judge_score'].mean())

# After: Structured logging with hierarchy
with mlflow.start_run(run_name=config['evaluation_name']):
    # Log configuration
    mlflow.log_param("evaluation_name", config['evaluation_name'])
    mlflow.log_param("data_source_type", config['data_source']['type'])
    mlflow.log_param("num_samples", len(inputs))
    mlflow.log_param("num_graders", len(graders))
    mlflow.log_param("max_concurrency", config['settings']['max_concurrency'])
    
    # Log each grader config as nested run
    for grader_config in config['graders']:
        with mlflow.start_run(run_name=grader_config['name'], nested=True):
            mlflow.log_param("grader_type", grader_config['type'])
            mlflow.log_param("dimension", grader_config['dimension'])
            mlflow.log_param("threshold", grader_config.get('threshold', 'N/A'))
    
    # Log all metrics
    for grader_name, metrics in aggregated.items():
        mlflow.log_metrics({
            f"{grader_name}_mean": metrics['mean'],
            f"{grader_name}_median": metrics['median'],
            f"{grader_name}_std": metrics['std'],
            f"{grader_name}_pass_rate": metrics['pass_rate']
        })
    
    # Log decision
    mlflow.log_metric("evaluation_passed", 1.0 if decision['pass'] else 0.0)
    mlflow.log_param("hard_stop_violations", len(decision['hard_stop_violations']))
    
    # Log artifacts
    mlflow.log_artifact("results/evaluation_results.csv")
    mlflow.log_artifact("results/evaluation_report.md")
    mlflow.log_artifact("results/plots/", artifact_path="plots")
```

### 5. Apply Code Quality Improvements
- **Extract magic numbers**: Convert hardcoded thresholds to named constants
- **Add type hints**: Annotate function signatures with types
- **Improve naming**: Use descriptive variable names (`eval_inputs` instead of `inputs`)
- **Add docstrings**: Document all public functions with purpose, args, returns
- **Remove dead code**: Delete unused graders, commented-out logic
- **Format consistently**: Apply black/autopep8 formatting

### 6. Strengthen Constitutional Compliance
Review against constitution hard-stops:
- ✔ All graders inherit from `BaseGrader`
- ✔ Error handling populates `GradeResult.error`
- ✔ Concurrency uses semaphore limits
- ✔ No hardcoded credentials (use Key Vault)
- ✔ MLflow logging present
- ✔ Output validation before persistence

### 7. Validate and Report

## Error Handling
- Breaking changes: Maintain backward compatibility or provide migration guide
- Performance regression: Benchmark before/after, ensure no degradation
- Constitutional violation introduced: Revert refactoring, find compliant alternative

## Examples
- **Example 1**: `/refactor-language-model-evaluation Extract common error handling pattern from heuristic graders into base class`
- **Example 2**: `/refactor-language-model-evaluation Add exponential backoff retry logic for LLM judge API calls`
- **Example 3**: `/refactor-language-model-evaluation Enhance prose report generation with tables, charts, and structured sections`
- **Example 4**: `/refactor-language-model-evaluation Implement circuit breaker pattern for LLM API to prevent cascade failures`
- **Example 5**: `/refactor-language-model-evaluation Add comprehensive MLflow logging with nested runs for each grader`

## References
Constitution: (pre-loaded above) | Config: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/env-config.yaml` | Grader Library: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/grader-library.py`
