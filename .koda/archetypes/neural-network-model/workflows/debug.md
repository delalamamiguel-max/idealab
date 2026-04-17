---
description: Diagnose neural network training, architecture, and deployment failures (Neural Network Model)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype neural-network-model --json ` and parse for PYTORCH_VERSION, CUDA_AVAILABLE, MLFLOW_TRACKING_URI, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/neural-network-model/templates/env-config.yaml` for debugging configuration

### 3. Parse Input
Extract from $ARGUMENTS: failure type (training crash, NaN loss, convergence issues, inference errors, deployment failures), error messages and stack traces, model specification (architecture, dataset, hyperparameters), recent changes (code, data, config), MLflow experiment ID if available. Request clarification if incomplete.

### 4. Diagnose Issue

Run diagnostic checks based on failure type:

**Training Failures**: Check learning rate magnitude, inspect gradient norms (identify exploding/vanishing gradients), verify data normalization and preprocessing, detect numerical instability (NaN/Inf in loss or weights), validate batch size and memory constraints, examine optimizer configuration.

**Architecture Issues**: Count parameters and verify capacity, check layer output shapes and dimensions, validate activation functions, inspect regularization (dropout rates, weight decay), analyze under/overfitting patterns, verify batch normalization placement.

**Data Pipeline Issues**: Profile data loading performance, check GPU utilization, verify batch collation and augmentation, inspect data types and value ranges, test for data leakage or corruption.

**Inference Failures**: Verify model.eval() mode, check device placement (CPU/GPU), validate input preprocessing pipeline, test output shape and range, inspect serialization/deserialization.

Provide diagnostic report with root cause hypothesis.

### 5. Generate Fix Recommendations

Provide targeted fixes: for NaN/Inf loss (reduce learning rate 10x, add gradient clipping, verify data normalization, check loss function stability), for slow training (increase num_workers, enable pin_memory, use mixed precision, optimize batch size), for overfitting (add dropout, increase weight decay, augment data, reduce model capacity), for underfitting (increase model capacity, reduce regularization, extend training, verify data quality), for memory errors (reduce batch size, enable gradient checkpointing, optimize model size).

Include code examples for fixes, configuration changes, monitoring additions.

### 6. Add Debugging Tools

Provide debugging utilities: anomaly detection setup (torch.autograd.set_detect_anomaly(True)), logging hooks (forward hooks for layer outputs, gradient hooks for gradient monitoring), profiling commands (torch.profiler for performance analysis), assertion checks (loss bounds, gradient norms, output ranges), visualization scripts (loss curves, gradient histograms, activation distributions).

### 7. Validate and Report


Generate debug report with issue summary, root cause analysis, recommended fixes, validation steps, prevention measures. Report completion.

## Error Handling

**Insufficient Information**: Request complete error logs, model architecture code, training configuration.

**Environment Mismatch**: Verify CUDA version, PyTorch installation, and dependency compatibility.

**Reproducibility Issues**: Request seed configuration and exact data/code versions used.

## Examples

**Example 1**: `/debug-neural-model Training loss became NaN at epoch 5` - Output: Diagnosis of numerical instability with gradient clipping fix

**Example 2**: `/debug-neural-model GPU utilization only 30% during training` - Output: Data loading bottleneck analysis with optimization recommendations

**Example 3**: `/debug-neural-model Model predictions differ between training and inference` - Output: Batch normalization eval mode issue with fix

## References

