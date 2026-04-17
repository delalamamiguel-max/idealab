---
description: Generate documentation for bash/PowerShell scripts and automation (Automation Scripter)
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
Extract from $ARGUMENTS: script file path, target audience (developers, operators, end users), documentation scope (README, runbook, user guide). Request clarification if incomplete.

### 4. Analyze Code/System

Analyze script: identify purpose and use cases, document parameters and arguments, explain functions and logic flow, note dependencies and prerequisites, identify error handling and exit codes, document environment variables and configuration.

### 5. Generate Documentation

Create comprehensive documentation with: script purpose and overview, prerequisites and dependencies, installation instructions, usage examples with all options, parameter reference, troubleshooting guide, operational runbook (for production scripts).

Include README.md, inline script comments, runbook for operations, deployment guide.

### 6. Add Recommendations

Include recommendations for documentation maintenance, operational procedures (scheduling, monitoring, alerting), security considerations (credential management, permissions), testing procedures, rollback procedures.

### 7. Validate and Report


Generate documentation artifacts. Report completion.

## Error Handling

**Insufficient Context**: Request script purpose and operational context.

**Complex Script**: Break documentation into sections per function.

**Missing Runbook**: Request operational procedures from team.

## Examples

**Example 1**: `/document-automation Create docs for backup.sh script` - Output: README with usage, parameters, scheduling guide

**Example 2**: `/document-automation Generate runbook for deployment script` - Output: Operational runbook with procedures and troubleshooting

**Example 3**: `/document-automation Document automation for end users` - Output: User-friendly guide with examples

## References

