---
description: Compare language model evaluation approaches, grader strategies, and decision criteria (Language Model Evaluation)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype language_model_evaluation` and ensure ENV_VALID. Halt if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/env-config.yaml` for baseline configurations

### 3. Parse Input and Identify Comparison
Extract from $ARGUMENTS: comparison type (grader configurations, evaluation approaches, output formats, decision criteria), specific alternatives to compare, evaluation context (use case, model type, constraints). Categorize comparison: grader strategy, data source, concurrency settings, threshold tuning, output generation.

### 4. Compare Alternatives

#### Grader Configuration Comparison
**Heuristic vs LLM Judge Trade-offs**:
- **Heuristic Graders**:
  - ✅ Pros: Deterministic, fast (no API calls), no cost, reproducible, no credentials needed
  - ❌ Cons: Limited to surface patterns, cannot assess semantic correctness, brittle to format changes
  - **Best for**: Format validation, length checks, keyword presence, structured output parsing
  
- **LLM Judge Graders**:
  - ✅ Pros: Semantic understanding, nuanced evaluation, handles ambiguity, contextual reasoning
  - ❌ Cons: Slow (API latency), costly (per-call pricing), non-deterministic, requires credentials
  - **Best for**: Correctness, safety, helpfulness, tone, coherence, relevance

**Recommendation Matrix**:
| Dimension | Heuristic | LLM Judge | Hybrid |
|-----------|-----------|-----------|--------|
| Format validation | ✓✓ | ✗ | Use heuristic |
| Length check | ✓✓ | ✗ | Use heuristic |
| Keyword presence | ✓✓ | ✗ | Use heuristic |
| Factual correctness | ✗ | ✓✓ | LLM judge with ground truth |
| Safety/toxicity | ✗ | ✓✓ | LLM judge with policy template |
| Helpfulness | ✗ | ✓✓ | LLM judge |
| Relevance | ✗ | ✓✓ | LLM judge |
| Style/tone | ~ | ✓✓ | Heuristic for obvious violations, LLM for subtle |

#### Evaluation Approach Comparison
**Batch vs Real-Time vs Streaming**:
- **Batch Evaluation**:
  - Use case: Model validation before deployment, A/B test analysis, periodic quality audits
  - Data source: CSV/JSONL/Parquet files, database queries
  - Latency: Offline (minutes to hours)
  - Cost: Efficient (batch API calls)
  
- **Real-Time Evaluation**:
  - Use case: Production inference monitoring, user feedback loop, live model selection
  - Data source: API endpoints, application logs
  - Latency: Low (seconds)
  - Cost: Higher (per-request overhead)
  
- **Streaming Evaluation**:
  - Use case: Continuous monitoring, drift detection, SLA compliance
  - Data source: Event streams (Kafka, Kinesis), database CDC
  - Latency: Near real-time (sub-second to seconds)
  - Cost: Moderate (micro-batching)

#### Output Format Comparison
**Structured vs Prose vs Both**:
- **Structured Only (CSV/JSON/Parquet)**:
  - ✅ Pros: Machine-readable, easy to aggregate, supports downstream analysis
  - ❌ Cons: Not human-friendly, requires additional tooling for interpretation
  - **Best for**: Automated pipelines, MLflow tracking, programmatic decision-making
  
- **Prose Only (Markdown/HTML/PDF)**:
  - ✅ Pros: Human-readable, stakeholder-friendly, narrative context
  - ❌ Cons: Hard to parse programmatically, not suitable for automation
  - **Best for**: Executive reports, governance documentation, stakeholder communication
  
- **Both**:
  - ✅ Pros: Serves both automated and human workflows
  - ❌ Cons: Increased storage, longer generation time
  - **Recommendation**: Always generate both for production evaluations

#### Decision Criteria Comparison
**Hard-Stops vs Targets vs Progressive Thresholds**:
- **Hard-Stops Only**:
  - Strict pass/fail (e.g., `safety_judge >= 0.9`)
  - Blocks deployment on violation
  - Use for: Safety, compliance, format validation
  
- **Targets Only**:
  - Soft goals with warnings (e.g., `correctness_judge >= 7.0`)
  - Does not block deployment
  - Use for: Quality aspirations, continuous improvement metrics
  
- **Progressive Thresholds**:
  - Tiered requirements (Bronze/Silver/Gold)
  - Bronze: Minimal hard-stops for PoC
  - Silver: Moderate requirements for pilot
  - Gold: Strict requirements for production
  - Use for: Staged rollout, maturity progression

### 5. Sensitivity Analysis

For threshold tuning, perform sensitivity analysis:
```python
# Test threshold variations
thresholds_to_test = [0.5, 0.6, 0.7, 0.8, 0.9]
for threshold in thresholds_to_test:
    decision_config['hard_stops']['safety_judge'] = threshold
    decision = check_decision_criteria(results_df, config)
    print(f"Threshold {threshold}: Pass rate = {decision['pass']}")
```

Generate ROC-style curves showing pass rate vs threshold for each grader.

### 6. Cost-Benefit Analysis

Compare total cost (time, money, complexity) vs benefit (accuracy, coverage, confidence):
```
Option A: 2 heuristics + 1 LLM judge
- Cost: $0.50 per 1000 samples, 30 seconds runtime
- Benefit: 85% coverage, 90% confidence

Option B: 5 heuristics only
- Cost: $0.00 per 1000 samples, 5 seconds runtime
- Benefit: 60% coverage, 70% confidence

Option C: 3 LLM judges
- Cost: $2.00 per 1000 samples, 120 seconds runtime
- Benefit: 95% coverage, 95% confidence
```

### 7. Recommendation and Report

Provide structured comparison report:
- **Summary table**: Side-by-side comparison of alternatives
- **Trade-off analysis**: Pros/cons for each option
- **Recommendation**: Best option given constraints (budget, latency, accuracy requirements)
- **Implementation guidance**: Next steps to adopt recommended approach

## Error Handling
- Insufficient context: Request use case details, constraints (budget, latency, accuracy SLA)
- Ambiguous alternatives: Clarify what dimensions to compare (grader types, data sources, output formats, etc.)
- Missing baseline: Establish current approach as baseline before comparing alternatives

## Examples
- **Example 1**: `/compare-language-model-evaluation Compare using 2 heuristics + 1 LLM judge vs 3 LLM judges for chatbot evaluation`
- **Example 2**: `/compare-language-model-evaluation Compare batch evaluation on CSV files vs real-time evaluation on API endpoint`
- **Example 3**: `/compare-language-model-evaluation Compare hard-stop threshold of 0.8 vs 0.9 for safety grader`
- **Example 4**: `/compare-language-model-evaluation Compare structured CSV output vs Markdown prose report vs both`
- **Example 5**: `/compare-language-model-evaluation Compare Bronze/Silver/Gold progressive thresholds vs single hard-stop criteria`

## References
Constitution: (pre-loaded above) | Config: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/env-config.yaml` | Grader Library: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/grader-library.py`
