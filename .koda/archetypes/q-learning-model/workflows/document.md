---
description: Document Q Learning Model solution for stakeholders and governance (Q Learning Model)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype q-learning-model --json ` and parse for MLFLOW_TRACKING_URI, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/q-learning-model/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: model location, target audience, documentation scope. Request clarification if incomplete.

### 4. Analyze Model
Extract metadata, performance metrics, governance evidence.

### 5. Generate Documentation Package
Create: Model Card, Technical Specification, User Guide, Governance Checklist.

### 6. Add Recommendations
Include maintenance procedures, monitoring, retraining triggers.

### 7. Validate and Report
Generate documentation. Report completion.

## Error Handling
**Incomplete Information**: Request model metadata and metrics.
**Missing Documentation**: Document all required components.

## Examples
**Example 1**: `/document-q-learning-model Create model documentation` - Output: Complete documentation package
**Example 2**: `/document-q-learning-model Generate governance docs` - Output: Governance-focused documentation

## References
