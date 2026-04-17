---
description: Scaffold workflow for Pub Sub Load Testing archetype (Pub Sub Load Testing)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype pub-sub-load-testing --json ` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/pub-sub-load-testing/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: relevant parameters for scaffold operation. Request clarification if incomplete.

### 4. Execute Scaffold Operation
Implement scaffold logic following constitution requirements and best practices for Pub Sub Load Testing.

### 5. Generate Outputs
Create necessary artifacts, reports, and configurations specific to scaffold operation.

### 6. Add Recommendations
Include best practices and optimization suggestions for Pub Sub Load Testing.

### 7. Validate and Report
Generate outputs and documentation. Report completion.

## Error Handling
**Common Issue**: Provide resolution guidance specific to scaffold and Pub Sub Load Testing.
**Configuration Error**: Validate settings and provide corrections.

## Examples
**Example 1**: `/scaffold-pub-sub-load-testing Sample scenario` - Output: Expected result for scaffold operation
**Example 2**: `/scaffold-pub-sub-load-testing Complex case` - Output: Detailed outcome with recommendations

## References
