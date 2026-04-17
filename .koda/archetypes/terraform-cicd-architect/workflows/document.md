---
description: Generate comprehensive documentation for Terraform CI/CD pipeline with compliance and governance (Terraform CICD Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype terraform-cicd-architect --json ` and parse for TERRAFORM_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/terraform-cicd-architect/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: pipeline location, target audience, documentation scope. Request clarification if incomplete.

### 4. Analyze Pipeline Architecture
Extract pipeline information: stages, policy enforcement, state management, approval workflow, drift monitoring.

### 5. Generate Documentation Package
Create: Pipeline Architecture docs, Engineer Guide, Operations Runbook, Security Documentation, Governance Documentation with supporting diagrams and checklists.

### 6. Add Recommendations
Include operational best practices and maintenance schedules.

### 7. Validate and Report
Generate documentation artifacts. Report completion.

## Error Handling
**Incomplete Information**: Request additional details.
**Missing Diagrams**: Generate from configuration.

## Examples
**Example 1**: `/document-terraform-cicd Create docs for AKS infrastructure pipeline` - Output: Complete documentation package
**Example 2**: `/document-terraform-cicd Generate compliance documentation` - Output: Governance and audit documentation

## References
