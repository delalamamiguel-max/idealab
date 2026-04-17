---
description: Validate language model evaluation pipeline for quality, fairness, and promotion readiness (Language Model Evaluation)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype language_model_evaluation` and ensure ENV_VALID. Halt if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load evaluation configuration and test specifications

### 3. Parse Input and Identify Test Scope
Extract from $ARGUMENTS: test type (unit, integration, end-to-end, performance, governance), components to test (graders, orchestration, output generation, MLflow integration), test data requirements, expected outcomes. Prioritize tests: constitutional compliance first, then functionality, then performance.

### 4. Execute Test Suites

#### Unit Tests - Grader Implementations
**Test Heuristic Graders**:
```python
import pytest
from grader_library import LengthCheckGrader, FormatValidatorGrader, EvaluationInput

def test_length_check_grader_in_range():
    """Test length grader scores 1.0 when length is within range"""
    grader = LengthCheckGrader(min_length=50, max_length=500)
    input_data = EvaluationInput(response="x" * 100)  # 100 chars
    
    result = await grader.grade(input_data)
    
    assert result.score == 1.0
    assert result.error is None
    assert result.reasoning is not None

def test_length_check_grader_too_short():
    """Test length grader scores 0.0 when length is too short"""
    grader = LengthCheckGrader(min_length=50, max_length=500)
    input_data = EvaluationInput(response="short")  # 5 chars
    
    result = await grader.grade(input_data)
    
    assert result.score == 0.0
    assert "too short" in result.reasoning.lower()

def test_format_validator_valid_json():
    """Test format validator scores 1.0 for valid JSON with required fields"""
    grader = FormatValidatorGrader(required_fields=["answer", "confidence"])
    input_data = EvaluationInput(response='{"answer": "42", "confidence": 0.9}')
    
    result = await grader.grade(input_data)
    
    assert result.score == 1.0
    assert result.metadata['is_valid_json'] is True
    assert len(result.metadata['missing_fields']) == 0

def test_format_validator_invalid_json():
    """Test format validator scores 0.0 for invalid JSON"""
    grader = FormatValidatorGrader(required_fields=["answer"])
    input_data = EvaluationInput(response='Not JSON')
    
    result = await grader.grade(input_data)
    
    assert result.score == 0.0
    assert result.metadata['is_valid_json'] is False

def test_grader_error_handling():
    """Test graders handle exceptions without raising"""
    grader = LengthCheckGrader()
    input_data = EvaluationInput(response=None)  # Invalid input
    
    result = await grader.grade(input_data)
    
    # Should return GradeResult with error, not raise exception
    assert result.error is not None
    assert result.score == 0.0
```

**Test LLM Judge Graders**:
```python
def test_llm_judge_default_parser():
    """Test default parser extracts score from LLM response"""
    async def mock_llm(prompt: str) -> str:
        return "Score: 8.5\n\nThe response is mostly correct."
    
    judge = LLMJudge(
        name="test_judge",
        judge_prompt_template="Evaluate: {response}",
        llm_callable=mock_llm
    )
    input_data = EvaluationInput(response="Test response")
    
    result = await judge.grade(input_data)
    
    assert result.score == 8.5
    assert result.reasoning is not None
    assert "Score: 8.5" in result.metadata['raw_llm_response']

def test_llm_judge_custom_parser():
    """Test custom parser extracts structured scores"""
    async def mock_llm(prompt: str) -> str:
        return '{"score": 7.5, "reasoning": "Good response"}'
    
    def json_parser(response: str) -> Tuple[float, str]:
        import json
        data = json.loads(response)
        return data['score'], data['reasoning']
    
    judge = LLMJudge(
        name="test_judge",
        judge_prompt_template="Evaluate: {response}",
        llm_callable=mock_llm,
        parser=json_parser
    )
    input_data = EvaluationInput(response="Test")
    
    result = await judge.grade(input_data)
    
    assert result.score == 7.5
    assert result.reasoning == "Good response"

def test_llm_judge_api_error():
    """Test LLM judge handles API errors gracefully"""
    async def failing_llm(prompt: str) -> str:
        raise Exception("API rate limit exceeded")
    
    judge = LLMJudge(
        name="test_judge",
        judge_prompt_template="Evaluate: {response}",
        llm_callable=failing_llm
    )
    input_data = EvaluationInput(response="Test")
    
    result = await judge.grade(input_data)
    
    # Should return error result, not raise exception
    assert result.error is not None
    assert "API rate limit" in result.error
    assert result.score == 0.0
```

#### Integration Tests - Evaluator Orchestration
**Test Async Batch Evaluation**:
```python
def test_evaluator_batch_processing():
    """Test evaluator processes batch with multiple graders"""
    graders = [
        LengthCheckGrader(),
        FormatValidatorGrader()
    ]
    evaluator = Evaluator(graders=graders, max_concurrency=3)
    
    inputs = [
        EvaluationInput(response='{"answer": "test"}'),
        EvaluationInput(response="A" * 100),
        EvaluationInput(response="Short")
    ]
    
    results_df = await evaluator.evaluate_batch(inputs)
    
    # Validate DataFrame structure
    assert len(results_df) == 3
    assert 'length_check_score' in results_df.columns
    assert 'format_validator_score' in results_df.columns
    assert results_df['length_check_score'].notna().all()

def test_evaluator_concurrency_limit():
    """Test evaluator respects concurrency limits"""
    import time
    
    call_times = []
    
    async def slow_llm(prompt: str) -> str:
        call_times.append(time.time())
        await asyncio.sleep(1)  # Simulate slow API
        return "Score: 8.0"
    
    judge = LLMJudge(name="slow_judge", judge_prompt_template="{response}", llm_callable=slow_llm)
    evaluator = Evaluator(graders=[judge], max_concurrency=2)
    
    inputs = [EvaluationInput(response=f"test{i}") for i in range(5)]
    
    start_time = time.time()
    await evaluator.evaluate_batch(inputs)
    total_time = time.time() - start_time
    
    # With concurrency=2 and 5 items taking 1s each, should take ~3s (not 5s)
    assert 2.5 < total_time < 3.5
    
    # Check no more than 2 concurrent calls
    concurrent_count = 0
    for i, t in enumerate(call_times):
        concurrent = sum(1 for t2 in call_times[:i+1] if abs(t - t2) < 0.1)
        concurrent_count = max(concurrent_count, concurrent)
    assert concurrent_count <= 2

def test_evaluator_error_isolation():
    """Test failing grader doesn't block other graders"""
    async def failing_llm(prompt: str) -> str:
        raise Exception("Always fails")
    
    good_grader = LengthCheckGrader()
    bad_grader = LLMJudge(name="bad_judge", judge_prompt_template="{response}", llm_callable=failing_llm)
    
    evaluator = Evaluator(graders=[good_grader, bad_grader], max_concurrency=2)
    inputs = [EvaluationInput(response="test")]
    
    results_df = await evaluator.evaluate_batch(inputs)
    
    # Good grader should succeed
    assert results_df['length_check_score'].iloc[0] > 0
    
    # Bad grader should have error but not crash evaluation
    assert 'bad_judge_error' in results_df.columns
    assert results_df['bad_judge_error'].iloc[0] is not None
```

#### End-to-End Tests - Full Pipeline
**Test Complete Evaluation Workflow**:
```python
def test_full_evaluation_pipeline():
    """Test complete evaluation pipeline from data load to report generation"""
    # Create test data
    test_data = pd.DataFrame({
        'prompt': ['What is 2+2?', 'Explain ML'],
        'response': ['4', 'Machine Learning is...'],
        'ground_truth': ['4', 'ML definition']
    })
    test_data.to_csv('/tmp/test_eval_data.csv', index=False)
    
    # Create test config
    config = {
        'evaluation_name': 'test_eval',
        'data_source': {
            'type': 'file',
            'format': 'csv',
            'location': '/tmp/test_eval_data.csv',
            'columns': {'prompt': 'prompt', 'response': 'response'}
        },
        'graders': [
            {'name': 'length_check', 'type': 'heuristic'}
        ],
        'settings': {'max_concurrency': 2},
        'output': {
            'structured': {'format': 'csv', 'path': '/tmp/results.csv'},
            'prose_report': {'enabled': True, 'path': '/tmp/report.md'}
        },
        'decision_criteria': {
            'hard_stops': {},
            'targets': {'length_check': 0.5}
        }
    }
    
    # Run pipeline
    results, aggregated, decision = await run_evaluation_pipeline_from_config(config)
    
    # Validate outputs
    assert os.path.exists('/tmp/results.csv')
    assert os.path.exists('/tmp/report.md')
    assert len(results) == 2
    assert 'length_check' in aggregated
    assert 'pass' in decision

def test_decision_criteria_enforcement():
    """Test hard-stops and targets are enforced correctly"""
    results_df = pd.DataFrame({
        'safety_judge_score': [0.95, 0.92, 0.88],  # Mean 0.916
        'format_validator_score': [1.0, 1.0, 1.0],  # Mean 1.0
        'correctness_judge_score': [6.5, 7.2, 6.8]  # Mean 6.83
    })
    
    config = {
        'decision_criteria': {
            'hard_stops': {
                'safety_judge': 0.9,  # Should PASS (0.916 >= 0.9)
                'format_validator': 1.0  # Should PASS (1.0 >= 1.0)
            },
            'targets': {
                'correctness_judge': 7.0  # Should MISS (6.83 < 7.0)
            }
        }
    }
    
    decision = check_decision_criteria(results_df, config)
    
    assert decision['pass'] is True  # Hard-stops passed
    assert len(decision['hard_stop_violations']) == 0
    assert len(decision['target_misses']) == 1  # Correctness target missed
```

#### Performance Tests
**Test Throughput and Latency**:
```python
def test_evaluation_performance():
    """Test evaluation meets performance SLAs"""
    # Generate 100 samples
    inputs = [EvaluationInput(response=f"test response {i}") for i in range(100)]
    
    graders = [LengthCheckGrader(), FormatValidatorGrader()]
    evaluator = Evaluator(graders=graders, max_concurrency=10)
    
    start_time = time.time()
    results_df = await evaluator.evaluate_batch(inputs)
    duration = time.time() - start_time
    
    # SLA: Process 100 samples with 2 heuristics in < 5 seconds
    assert duration < 5.0
    
    # SLA: All samples processed successfully
    assert len(results_df) == 100
    assert results_df['length_check_score'].notna().all()

def test_memory_efficiency():
    """Test evaluation doesn't consume excessive memory"""
    import psutil
    import gc
    
    process = psutil.Process()
    gc.collect()
    
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Process large batch
    inputs = [EvaluationInput(response="x" * 1000) for _ in range(1000)]
    graders = [LengthCheckGrader()]
    evaluator = Evaluator(graders=graders, max_concurrency=5)
    
    results_df = await evaluator.evaluate_batch(inputs)
    
    gc.collect()
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory
    
    # SLA: Memory increase < 500 MB for 1000 samples
    assert memory_increase < 500
```

#### Governance Tests - Constitutional Compliance
**Test Hard-Stop Rule Enforcement**:
```python
def test_grader_inherits_base_grader():
    """Test all graders inherit from BaseGrader"""
    from grader_library import BaseGrader
    
    graders = [LengthCheckGrader(), FormatValidatorGrader()]
    
    for grader in graders:
        assert isinstance(grader, BaseGrader)

def test_no_hardcoded_credentials():
    """Test no hardcoded API keys in grader library"""
    import re
    
    with open('${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/grader-library.py') as f:
        code = f.read()
    
    # Check for common API key patterns
    assert not re.search(r'api_key\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', code)
    assert not re.search(r'sk-[a-zA-Z0-9]{48}', code)  # OpenAI key pattern

def test_mlflow_logging_present():
    """Test MLflow integration is implemented"""
    # Validate MLflow logging exists in pipeline example
    with open('${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/evaluation-pipeline-example.py') as f:
        code = f.read()
    
    assert 'import mlflow' in code
    assert 'mlflow.log_param' in code or 'mlflow.log_metric' in code

def test_output_validation_before_persistence():
    """Test outputs are validated before saving"""
    # This would check that validation logic exists
    # Example: Verify DataFrame has expected columns before to_csv()
    pass
```

### 5. Generate Test Report
Create comprehensive test report:
```markdown
# Language Model Evaluation - Test Report

## Test Summary
- **Total Tests**: 25
- **Passed**: 24
- **Failed**: 1
- **Skipped**: 0
- **Duration**: 42.3 seconds
- **Coverage**: 87%

## Test Results by Category

### Unit Tests (12/12 passed)
✅ Grader implementations
✅ Error handling
✅ Input validation
✅ Parser logic

### Integration Tests (8/8 passed)
✅ Async orchestration
✅ Concurrency control
✅ Error isolation
✅ Batch processing

### End-to-End Tests (3/4 passed)
✅ Full pipeline execution
✅ Decision criteria enforcement
❌ MLflow artifact upload (timeout)
✅ Report generation

### Performance Tests (2/2 passed)
✅ Throughput SLA met (100 samples < 5s)
✅ Memory efficiency (< 500 MB increase)

### Governance Tests (3/3 passed)
✅ BaseGrader inheritance
✅ No hardcoded credentials
✅ MLflow logging present

## Failed Tests

### test_mlflow_artifact_upload_large_files
**Error**: Timeout waiting for artifact upload
**Root Cause**: Network latency to MLflow server
**Remediation**: Increase timeout or optimize artifact size
**Severity**: Medium
**Blocks Promotion**: No (can upload manually)

## Coverage Report
- grader_library.py: 92%
- evaluation_pipeline_example.py: 78%
- __init__.py: 100%

## Recommendations
1. Fix MLflow timeout issue before production deployment
2. Add integration tests for real LLM API calls (currently mocked)
3. Increase coverage for error handling edge cases
4. Add performance tests for LLM judge graders
```

### 6. Validate Promotion Readiness
Check if evaluation pipeline is ready for production:
- ✅ All constitutional hard-stops met
- ✅ Unit test coverage > 80%
- ✅ Integration tests pass
- ⚠️ 1 end-to-end test failure (non-blocking)
- ✅ Performance SLAs met
- ✅ Governance compliance validated

**Recommendation**: Approve with caveat - fix MLflow timeout before high-volume usage.

### 7. Report and Document

## Error Handling
- Test failures: Triage by severity, create remediation plan, retest after fixes
- Flaky tests: Identify root cause (race conditions, network issues), stabilize or skip
- Missing test data: Generate synthetic data or request realistic samples from users

## Examples
- **Example 1**: `/test-language-model-evaluation Run full test suite before production deployment`
- **Example 2**: `/test-language-model-evaluation Validate grader implementations with unit tests`
- **Example 3**: `/test-language-model-evaluation Check constitutional compliance for audit`
- **Example 4**: `/test-language-model-evaluation Performance test evaluation pipeline for 10K samples`
- **Example 5**: `/test-language-model-evaluation Integration test evaluator orchestration with mock LLM`

## References
Constitution: (pre-loaded above) | Config: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/env-config.yaml` | Grader Library: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/grader-library.py` | Pipeline Example: `${ARCHETYPES_BASEDIR}/language-model-evaluation/templates/evaluation-pipeline-example.py`
