---
description: Compare bash/PowerShell script approaches and patterns (Automation Scripter)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype automation-scripter --json ` and parse for SHELL_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/automation-scripter/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: automation problem, comparison criteria (portability, performance, maintainability), constraints. Request clarification if incomplete.

### 4. Generate Alternatives

Create 2-3 different automation approaches: Bash script (Linux/Unix native), PowerShell script (Windows/cross-platform), Python script (universal, more dependencies). Each with complete code, use cases, pros/cons.

### 5. Generate Comparison Matrix

Compare on: portability, performance, maintainability, complexity, dependencies, error handling, testing support. Provide scores and analysis.

### 6. Add Recommendations

Recommend approach with justification. Include migration guidance, testing strategy, deployment considerations.

### 7. Validate and Report


## Error Handling

**Insufficient Context**: Request automation goals and target environments.

**Platform Ambiguity**: Clarify target OS and deployment context.

**Tool Availability**: Check for required tools and suggest alternatives.

## Examples

**Example 1**: `/compare-automation Compare bash vs PowerShell for file sync` - Output: 2 approaches with portability analysis

**Example 2**: `/compare-automation Should I use rsync or custom script?` - Output: Tool vs custom comparison

**Example 3**: `/compare-automation Compare parallel vs sequential processing` - Output: Performance trade-off analysis

## References

