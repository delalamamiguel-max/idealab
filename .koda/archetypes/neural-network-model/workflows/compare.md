---
description: Compare neural network architectures, training strategies, and deployment approaches (Neural Network Model)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype neural-network-model --json ` and parse for PYTORCH_VERSION, MLFLOW_TRACKING_URI, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/neural-network-model/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type (architectures, training strategies, frameworks, deployment approaches), candidate approaches (A, B, C with specifications), evaluation criteria (accuracy, latency, cost, interpretability, fairness), use case requirements (data size, latency constraints, hardware availability), MLflow experiment IDs if available. Request clarification if incomplete.

### 4. Generate Comparison Framework

Based on comparison type, evaluate:

**Architecture Comparison**: Model complexity (parameter count, layer depth, architectural innovations), performance metrics (accuracy, F1, AUC on validation/test sets), training efficiency (convergence speed, GPU memory usage, training time), inference characteristics (latency, throughput, memory footprint), interpretability (explainability options, feature attribution methods), maintenance burden (code complexity, debugging difficulty).

**Training Strategy Comparison**: Optimizer performance (SGD, Adam, AdamW, LAMB convergence), learning rate schedules (step decay, cosine, OneCycle effectiveness), augmentation strategies (standard, AutoAugment, MixUp results), regularization approaches (dropout, weight decay, early stopping impact), mixed precision training (speed vs accuracy trade-off), convergence metrics (final loss, validation performance, training stability).

**Framework Comparison**: Development experience (API usability, documentation quality), performance (training speed, inference speed, memory efficiency), deployment options (TorchServe, TF Serving, ONNX Runtime), ecosystem maturity (library support, community size), production readiness (monitoring tools, debugging capabilities).

**Deployment Comparison**: Latency requirements (edge <10ms, cloud ~100ms, batch processing), cost analysis (device cost, inference cost per request, scaling cost), scalability (horizontal scaling, load balancing), operational complexity (deployment difficulty, monitoring needs, maintenance burden).

### 5. Generate Comparison Matrix

Create detailed comparison table with quantitative metrics from MLflow experiments, qualitative assessments, cost calculations, trade-off analysis.

Include visualizations: performance comparison charts, cost-benefit analysis, latency-accuracy trade-off curves, resource utilization comparisons.

### 6. Add Recommendations

Recommend approach with comprehensive justification: performance requirements alignment, cost-benefit analysis, operational feasibility, governance and fairness posture, long-term maintenance considerations.

Provide implementation roadmap: architecture selection rationale, training strategy recommendations, deployment approach, monitoring and alerting plan, optimization opportunities.

Include risk assessment and mitigation strategies.

### 7. Validate and Report


Generate comparison report with decision matrix, visualization artifacts, executive summary for stakeholders. Report completion with recommendation.

## Error Handling

**Missing Metrics**: Request complete MLflow experiment data or run missing evaluations.

**Unfair Comparison**: Ensure consistent evaluation protocols, datasets, and hardware.

**Incomplete Cost Analysis**: Request infrastructure pricing and usage projections.

## Examples

**Example 1**: `/compare-neural-model Compare ResNet50 vs EfficientNet-B0 for image classification` - Output: Architecture comparison with accuracy-efficiency trade-offs

**Example 2**: `/compare-neural-model Evaluate AdamW vs LAMB optimizers for large batch training` - Output: Training strategy comparison with convergence analysis

**Example 3**: `/compare-neural-model Compare edge deployment vs cloud API for real-time inference` - Output: Deployment approach comparison with latency-cost analysis

## References

