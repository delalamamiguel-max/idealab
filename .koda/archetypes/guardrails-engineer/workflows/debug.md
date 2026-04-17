---
description: Debug guardrail failures, false positives, bypass attempts, and performance issues (Guardrails Engineer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Environment Setup

// turbo
Verify debugging tools are available:
- Python logging configured
- Guardrails test suite accessible
- Phoenix/monitoring access (if applicable)

### 2. Load Configuration

- Read `guardrails-engineer-constitution.md` for expected behavior
- Load current guardrails configuration

### 3. Parse Input

Extract from $ARGUMENTS:
- **Issue type**: false_positive | false_negative | bypass | performance | crash
- **Guardrail type**: prompt_injection | pii_detection | hallucination | etc.
- **Sample input/output**: The triggering input or output
- **Expected behavior**: What should have happened
- **Actual behavior**: What actually happened
- **Error messages**: Any error logs or stack traces

If incomplete, request:
```
Please provide:
1. Issue Type: false_positive | false_negative | bypass | performance | crash
2. Guardrail Type: (e.g., "prompt_injection")
3. Sample Input: (the text that triggered the issue)
4. Expected: (what should have happened)
5. Actual: (what actually happened)
6. Error Messages: (if any)
```

### 4. Diagnose Issue

**4.1. False Positive Analysis**
```python
# Debug false positives
async def debug_false_positive(guardrail, input_text):
    """Analyze why a legitimate input was blocked."""
    
    # Get detailed evaluation
    result = await guardrail.evaluate_with_reasoning(input_text)
    
    return {
        "confidence": result.confidence,
        "threshold": guardrail.threshold,
        "reasoning": result.reasoning,
        "similar_patterns": find_similar_blocked_patterns(input_text),
        "recommendation": suggest_threshold_adjustment(result)
    }
```

**4.2. False Negative Analysis**
```python
# Debug false negatives (missed threats)
async def debug_false_negative(guardrail, malicious_input):
    """Analyze why a threat was not detected."""
    
    # Check if pattern is known
    known_patterns = load_attack_patterns()
    is_known = match_known_patterns(malicious_input, known_patterns)
    
    # Get detailed evaluation
    result = await guardrail.evaluate_with_reasoning(malicious_input)
    
    return {
        "is_known_pattern": is_known,
        "confidence": result.confidence,
        "threshold": guardrail.threshold,
        "gap": guardrail.threshold - result.confidence,
        "recommendation": "Lower threshold" if result.confidence > 0.5 else "Add pattern"
    }
```

**4.3. Bypass Analysis**
```python
# Debug bypass attempts
async def debug_bypass(input_text, expected_block):
    """Analyze how guardrails were bypassed."""
    
    # Check all guardrails
    results = await evaluate_all_guardrails(input_text)
    
    # Find the gap
    bypassed = [r for r in results if r.passed and r.guardrail_type == expected_block]
    
    return {
        "bypassed_guardrails": bypassed,
        "confidence_scores": {r.guardrail_type: r.confidence for r in results},
        "attack_vector": classify_attack_vector(input_text),
        "recommendation": generate_bypass_fix(input_text, bypassed)
    }
```

**4.4. Performance Analysis**
```python
# Debug performance issues
async def debug_performance(guardrail_type, sample_inputs):
    """Analyze guardrail latency issues."""
    
    latencies = []
    for input_text in sample_inputs:
        start = time.time()
        await guardrail.evaluate(input_text)
        latencies.append(time.time() - start)
    
    return {
        "p50_latency": np.percentile(latencies, 50),
        "p95_latency": np.percentile(latencies, 95),
        "p99_latency": np.percentile(latencies, 99),
        "bottleneck": identify_bottleneck(guardrail_type),
        "recommendation": suggest_optimization(guardrail_type, latencies)
    }
```

### 5. Generate Fix Recommendations

Based on diagnosis, provide targeted fixes:

**For False Positives:**
- Adjust threshold (current: X, recommended: Y)
- Add exception pattern for legitimate use case
- Improve classifier training data
- Add context-aware evaluation

**For False Negatives:**
- Add new attack pattern to detection
- Lower detection threshold
- Implement additional guardrail layer
- Update adversarial test suite

**For Bypasses:**
- Patch specific bypass vector
- Add input normalization
- Implement defense-in-depth
- Alert on similar patterns

**For Performance:**
- Enable caching for guardrail type
- Use lighter model variant
- Implement async evaluation
- Add early exit conditions

### 6. Implement Fix

Apply the recommended fix and create test case:

```python
# Add regression test for the fix
@pytest.mark.asyncio
async def test_fix_{issue_id}():
    """Regression test for {issue_description}."""
    guardrails = load_guardrails("config.yaml")
    
    # The problematic input
    input_text = "{sample_input}"
    
    # Expected behavior after fix
    result = await guardrails.evaluate(input_text)
    assert result.{expected_assertion}
```

### 7. Validate Fix

// turbo
Run validation:
- [ ] Original issue is resolved
- [ ] No new false positives introduced
- [ ] No new false negatives introduced
- [ ] Latency within acceptable range
- [ ] Full test suite passes

### 8. Document Resolution

```markdown
## Issue Resolution

### Issue ID: {id}
### Type: {issue_type}
### Guardrail: {guardrail_type}

### Root Cause
{explanation}

### Fix Applied
{description of fix}

### Verification
- Test case added: test_fix_{issue_id}
- Regression suite: PASSED
- Performance impact: {none/minimal/acceptable}

### Prevention
{how to prevent similar issues}
```

## Error Handling

| Error | Resolution |
|-------|------------|
| Cannot reproduce | Request more context/logs |
| Fix causes regressions | Rollback and refine approach |
| Performance degradation | Optimize or accept tradeoff |
| Unknown attack vector | Escalate to security team |

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide agent name, scope (input/output/both), and guardrail level (L1–L4). |
| `guardrails-engineer-constitution.md` not found | Stop. Ensure file is present at repo root. |
| `deepeval` or `presidio` not installed | Run `pip install deepeval presidio-analyzer presidio-anonymizer`. |
| Guardrail blocks all inputs unexpectedly | Check threshold in `config.template.json` — L1 defaults may be too strict for your domain. |
| PII detection false positives | Review Presidio entity list; exclude irrelevant entity types for your context. |
| Injection pattern test fails | Verify test prompts in `references/` match your threat model; add domain-specific patterns. |

## Examples

**Example 1**: `/debug-guardrails-engineer false_positive prompt_injection "Please ignore the noise and focus on the task"`
- Output: Threshold adjustment recommendation

**Example 2**: `/debug-guardrails-engineer bypass pii_detection "My social is one two three..."`
- Output: Pattern normalization fix

**Example 3**: `/debug-guardrails-engineer performance hallucination latency=3000ms`
- Output: Caching and model optimization recommendations

## References

Constitution: `guardrails-engineer-constitution.md`
