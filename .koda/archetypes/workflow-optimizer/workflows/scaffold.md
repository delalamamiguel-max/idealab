---
description: Create optimization plan for agent workflows (Workflow Optimizer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Workflow path**: Path to workflow to optimize
- **Goal**: latency | cost | quality
- **Target**: Optimization target (e.g., 20% reduction)

### 2. Profile Workflow
- Measure baseline latency
- Track token usage
- Identify bottlenecks

### 3. Generate Optimization Plan

```markdown
## Optimization Plan

### Baseline
- Latency P95: {ms}
- Cost per request: ${cost}

### Bottlenecks
1. {bottleneck1} - {impact}
2. {bottleneck2} - {impact}

### Recommendations
1. {optimization1} - Expected: {improvement}
2. {optimization2} - Expected: {improvement}
```

### 4. Validate

Verify the optimization actually delivered the promised improvement — without regressing quality:

```python
# Run with the active environment interpreter
import time
# Run 10 sample requests through optimized workflow
# Compare P95 latency against baseline from Step 2
print('Run latency benchmark: compare P95 before vs after')
```

**Checklist:**
- [ ] Optimized P95 latency meets the target from Step 1 (e.g., ≤15s if target was 15s)
- [ ] Quality metrics (faithfulness, relevancy) stayed within acceptable bounds (no regression)
- [ ] Cost per request is maintained or reduced
- [ ] A/B test shows statistically significant improvement (not noise)
- [ ] Rollback procedure is documented and tested
- [ ] LangSmith traces confirm the optimization is applied in production paths

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide workflow path or description, optimization goal (latency/cost/quality), and target. |
| `workflow-optimizer-constitution.md` not found | Stop. Ensure file is present at repo root. |
| `LANGSMITH_API_KEY` not set | Set environment variable. LangSmith is required for profiling and A/B testing. |
| Baseline measurement returns 0ms | Profiling not wired correctly. Verify LangSmith instrumentation is active before running baseline. |
| Optimization regresses quality below threshold | HARD STOP per constitution. Roll back the optimization. Document regression and reason. |
| A/B test inconclusive | Run more samples (minimum 100 requests). Do not apply optimization until statistical significance is reached. |

## Examples
**Example**: `/scaffold-workflow-optimizer graph/workflow.py latency target=20%`
