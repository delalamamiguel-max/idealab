---
description: Refactor workflow for Software Release Notes archetype (Software Release Notes)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype software-release-notes --json ` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/software-release-notes/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: relevant parameters for refactor operation. Request clarification if incomplete.

### 4. Execute Refactor Operation
Implement refactor logic following constitution requirements and best practices for Software Release Notes.

### 5. Generate Outputs
Create necessary artifacts, reports, and configurations specific to refactor operation.

### 6. Add Recommendations
Include best practices and optimization suggestions for Software Release Notes.

### 7. Validate and Report
Generate outputs and documentation. Report completion.

## Error Handling
**Common Issue**: Provide resolution guidance specific to refactor and Software Release Notes.
**Configuration Error**: Validate settings and provide corrections.

## Examples
**Example 1**: `/refactor-software-release-notes Sample scenario` - Output: Expected result for refactor operation
**Example 2**: `/refactor-software-release-notes Complex case` - Output: Detailed outcome with recommendations

## References
