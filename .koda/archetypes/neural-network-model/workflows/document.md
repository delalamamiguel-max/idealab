---
description: Document neural network model card, architecture spec, training guide, and deployment runbook (Neural Network Model)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype neural-network-model --json ` and parse for MLFLOW_TRACKING_URI, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/neural-network-model/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: model identifier (MLflow run ID, registry URI, code repository), documentation scope (model card, technical spec, user guide, deployment runbook, governance package), target audience (data scientists, ML engineers, business stakeholders, governance reviewers). Request clarification if incomplete.

### 4. Analyze Model Artifacts

Extract comprehensive model information from MLflow: model metadata (architecture type, framework version, parameter count, creation date, owner), hyperparameters (learning rate, optimizer, batch size, epochs, regularization), training data (dataset name and version, time period, size, class distribution, preprocessing steps), performance metrics (accuracy, F1, AUC, loss curves, validation metrics, test set results), fairness metrics (demographic parity, equal opportunity, disparate impact across protected attributes), computational requirements (GPU type, memory usage, training time, inference latency), experiment tracking (run ID, parent runs, tags, git commit hash).

Identify documentation gaps and gather additional context.

### 5. Generate Documentation Package

Create comprehensive documentation suite:

**Model Card** (MODEL_CARD.md): Model overview (architecture summary, intended use, limitations), performance summary (key metrics with confidence intervals, benchmark comparisons), fairness assessment (protected attributes analyzed, bias metrics, mitigation strategies), ethical considerations (potential harms, use case restrictions, monitoring requirements), training details (dataset description, preprocessing, augmentation), technical specifications (framework, hardware, dependencies), maintenance (owner contact, retraining schedule, deprecation timeline), references (MLflow links, papers, related models).

**Technical Specification** (TECHNICAL_SPEC.md): Architecture details (layer-by-layer breakdown, diagram, parameter counts, activation functions), implementation (code structure, key modules, configuration files), training procedure (data loading, optimizer configuration, learning rate schedule, checkpointing strategy), reproducibility (environment setup, dependency management, seed configuration, exact commands), inference (model loading, preprocessing pipeline, batch vs single inference, ONNX export), performance optimization (mixed precision, quantization, pruning options).

**User Guides**: For data scientists (training guide, evaluation procedures, hyperparameter tuning, experiment tracking), for ML engineers (deployment guide, infrastructure requirements, scaling strategies, monitoring setup, rollback procedures, troubleshooting), for business users (prediction interpretation, confidence scores, when to escalate, performance expectations).

**Deployment Runbook** (DEPLOYMENT_RUNBOOK.md): Prerequisites, deployment steps, configuration, health checks, monitoring dashboards, alerting, incident response, rollback procedures.

**Governance Checklist** (GOVERNANCE_CHECKLIST.md): Documentation completeness, testing validation, fairness assessment, security review, compliance requirements, audit trail, approval signatures, review schedule.

Include supporting artifacts: architecture diagrams, training curves and metrics plots, confusion matrices and ROC curves, fairness metrics visualizations, calibration plots, example predictions with explanations, performance benchmark tables, MLflow experiment and registry links.

### 6. Add Recommendations

Include recommendations for documentation maintenance (version alongside model releases, update on retraining, store in git, link to MLflow runs), operational procedures (monitoring dashboard URLs, alert thresholds and escalation, incident runbook links, retraining triggers), stakeholder communication (technical vs non-technical language, visualization best practices, reporting cadence), compliance tracking (audit readiness, regulatory alignment, review schedules, governance approval workflow).

Provide documentation quality checklist.

### 7. Validate and Report


Generate all documentation artifacts organized in docs/ directory. Create index.md with navigation. Report completion with artifact locations and governance approval checklist.

## Error Handling

**Incomplete MLflow Data**: Request full experiment tracking or provide instructions for missing metrics.

**Fairness Metrics Missing**: Document limitation and recommend fairness evaluation.

**Architecture Diagram Missing**: Generate from code using visualization tools.

**Performance Benchmarks Incomplete**: Flag missing benchmarks and provide evaluation scripts.

## Examples

**Example 1**: `/document-neural-model Create model card for ResNet50_image_classifier_v3` - Output: Complete model card with fairness assessment and ethical considerations

**Example 2**: `/document-neural-model Generate full documentation package for production deployment` - Output: Model card, technical spec, deployment runbook, governance checklist

**Example 3**: `/document-neural-model Document neural_nlp_model for stakeholder review` - Output: Documentation suite with business-friendly explanations and technical details

## References

