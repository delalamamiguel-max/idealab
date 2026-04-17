---
description: Generate comprehensive documentation for Databricks developer workflows and deployment scripts
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Documentation Scope

Extract from $ARGUMENTS:
- What to document (scripts, workflows, configurations)
- Target audience (developers, ops, new team members)
- Documentation depth (quick start, comprehensive, reference)

### 2. Gather Source Materials

Collect existing artifacts:
- Deployment scripts (bash, Python)
- Configuration files (profiles, job configs)
- Environment setup documentation
- Existing README files

### 3. Generate Documentation Package

Based on scope and audience:

**Developer Quick Start:**
- Environment setup checklist
- First notebook deployment walkthrough
- Common commands reference
- Troubleshooting quick tips

**Comprehensive Guide:**
- Architecture overview (Git-based vs Workspace-based)
- Detailed setup instructions
- Script usage documentation
- Job configuration guide
- Security best practices
- Monitoring and debugging guide

**Operations Reference:**
- CLI command reference
- Environment variable catalog
- Profile configuration guide
- Runbook for common operations

### 4. Document Scripts

For each deployment script, generate:
- Purpose and use case
- Prerequisites and dependencies
- Usage syntax and examples
- Input parameters and environment variables
- Output and exit codes
- Error handling behavior

### 5. Document Workflows

Create workflow documentation:
- End-to-end deployment workflow diagram
- Step-by-step execution guide
- Decision points and alternatives
- Integration with CI/CD pipelines

### 6. Create Environment Setup Guide

Document setup requirements:
- CLI installation and version requirements
- Profile configuration steps
- Environment variable setup
- Pre-commit hook configuration
- Local development environment setup

### 7. Assemble Documentation

Deliver documentation package:
- `docs/README.md` - Main entry point
- `docs/QUICK_START.md` - Getting started guide
- `docs/CLI_REFERENCE.md` - Command reference
- `docs/TROUBLESHOOTING.md` - Common issues and solutions
- `docs/SECURITY.md` - Security guidelines

## Error Handling

**Missing Scripts**: Document what should exist based on constitution patterns.

**Incomplete Setup**: Note gaps and provide setup instructions.

## Examples

### Example 1: Quick Start Guide

```
/document-databricks-developer-workflow "
Create quick start guide for new team members.
Focus: Get first notebook deployed in 30 minutes
Include: Environment setup, first deployment, verification
"
```

### Example 2: Full Documentation

```
/document-databricks-developer-workflow "
Comprehensive documentation for our Databricks deployment workflow.
Include all scripts, configurations, and operational procedures.
Audience: Development and operations teams
"
```

### Example 3: CLI Reference

```
/document-databricks-developer-workflow "
Create CLI command reference card.
Include: Common operations, syntax, examples
Format: Quick reference for daily use
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/databricks-developer-workflow/databricks-developer-workflow-constitution.md`
- **CLI Reference**: Constitution Section V - CLI Operations Reference
- **Documentation Standards**: Delegate to documentation-evangelist for prose quality
