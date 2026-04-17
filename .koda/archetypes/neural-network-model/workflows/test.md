---
description: Validate neural network pipeline for architecture, training, inference, and governance readiness (Neural Network Model)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype neural-network-model --json ` and parse for PYTORCH_VERSION, PYTEST_VERSION, CUDA_AVAILABLE, MLFLOW_TRACKING_URI, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/neural-network-model/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: model identifier (code path, MLflow run ID, registry URI), test scope (unit, integration, performance, fairness, full suite), acceptance criteria (accuracy thresholds, latency limits, fairness metrics), test environment (GPU availability, dataset access). Request clarification if incomplete.

### 4. Analyze Test Requirements

Identify testable components: model architecture (layer shapes, forward pass, gradient flow, parameter initialization), data pipeline (data loading, transformations, augmentation, batch collation), training loop (loss computation, optimizer step, learning rate scheduling, checkpoint saving), inference (prediction consistency, output shapes, batch vs single inference, model.eval() behavior), MLflow integration (metric logging, artifact saving, model registration), monitoring (drift detection, fairness metrics, performance tracking).

Define test scenarios: unit tests (module forward/backward passes, shape consistency, activation functions, loss functions), integration tests (end-to-end training for few steps, checkpoint save/load, MLflow tracking validation, inference pipeline), performance tests (accuracy on holdout set, inference latency benchmarks, throughput measurements, memory usage), robustness tests (adversarial inputs, out-of-distribution data, edge cases), fairness tests (demographic parity, equal opportunity, disparate impact on protected attributes), reproducibility tests (seeded training consistency, deterministic forward pass).

### 5. Generate Test Suite

Create comprehensive test suite with test fixtures (synthetic datasets, mock models, GPU/CPU device handling), unit tests (test_model_forward_pass, test_model_backward_pass, test_loss_computation, test_optimizer_step, test_data_loading), integration tests (test_training_pipeline, test_mlflow_logging, test_checkpoint_management, test_inference_pipeline), performance tests (test_accuracy_threshold, test_inference_latency, test_batch_inference, test_memory_usage), fairness tests (test_demographic_parity, test_equal_opportunity, test_calibration_by_group), regression tests (test_model_versioning, test_prediction_consistency, test_api_contract).

Include pytest configuration, conftest.py with fixtures, test data generators, GPU/CPU parameterization, CI/CD integration hooks, coverage reporting configuration.

### 6. Add Recommendations

Include recommendations for test execution (use GPU for integration tests if available, mock expensive operations, parallelize test suite, maintain test data versioning), CI/CD integration (run unit tests on every commit, run full suite on PR, gate deployments on test success, track test execution time trends), coverage improvements (test all error paths, validate numerical stability, stress test memory limits, test distributed training), monitoring (track test failures, alert on regression, maintain test health dashboard).

Provide execution commands and expected runtime.

### 7. Validate and Report


Execute test suite: `pytest tests/ --cov=src --cov-report=html --cov-report=term --junitxml=results.xml -v`

Generate test report with pass/fail summary, coverage metrics (line, branch, function coverage), performance benchmarks (accuracy, latency, throughput), fairness validation results, failed test details with remediation guidance. Report completion.

## Error Handling

**CUDA Out of Memory**: Reduce batch size in tests or skip GPU tests gracefully.

**Test Data Missing**: Provide synthetic data generation scripts or download instructions.

**Fairness Data Unavailable**: Skip fairness tests with documented limitation.

**Model Checkpoint Missing**: Provide instructions for training test model or downloading from registry.

## Examples

**Example 1**: `/test-neural-model Validate ResNet50_v2 from MLflow registry` - Output: 87 tests passing, 95% coverage, all benchmarks met

**Example 2**: `/test-neural-model Create test suite for image_classifier training pipeline` - Output: Comprehensive test suite with GPU/CPU parameterization

**Example 3**: `/test-neural-model Run fairness tests on production_model_v5` - Output: Fairness validation across protected attributes with bias report

## References

