---
description: Scaffold collaborative notebook workflow with source control, reproducibility, and review discipline (Notebook Collaboration Coach)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype notebook-collaboration-coach --json ` and ensure ENV_VALID. Halt if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/notebook-collaboration-coach/templates/env-config.yaml` for repository standards, Jupytext pairing rules, lint/test tools, and archival locations

### 3. Parse Input
Extract from $ARGUMENTS: notebook purpose, target environment (Databricks, VS Code), contributors, execution cadence, required integrations (MLflow, data sources), approval workflow. Request missing context as needed.

### 4. Validate Constraints
Apply hard stops:
- ✘ Refuse notebooks outside git-backed repos or lacking branch protections
- ✘ Block missing reviewer assignments or unresolved comments workflow
- ✘ Forbid hidden cluster state reliance; must be restartable top-to-bottom
- ✘ Require Jupytext (or configured alternative) pairing with `.py/.R` sync
- ✘ Disallow secrets in notebooks; enforce secret scopes/config
- ✘ Demand automated execution validation (Papermill/NBQA) in pipelines
- ✘ Enforce formatting/linting (Black/Ruff) rules

### 5. Generate Notebook Blueprint
Provide scaffold instructions:
- Standard template sections (Overview, Configuration, Execution, Results, Follow-ups)
- Parameterization via widgets/Papermill parameters for environment toggles
- Setup cells for reproducibility (package installs, environment capture)
- Execution metadata capture (timestamp, cluster ID, git SHA, MLflow run)
- Logging hooks and error handling patterns
- Guidance for modularizing complex logic into packages/modules
- Comments/resolution workflow integration with pull request templates
- NBQA/pytest hooks for automated linting/testing
- Archival plan for executed notebooks with sanitized outputs

### 6. Recommend Enhancements
Suggest optional practices:
- Shared module repository for reusable code segments
- Live Share or Databricks shared editing guidelines
- Review dashboard integration to surface open notebook reviews
- Auto-comment bots reminding reviewers about SLA breaches
- Multi-language pairing (SQL/Python) with synchronized scripts
- Documentation sync into Confluence or internal portal

### 7. Validate and Report

## Error Handling
- Hard-stop triggered: Halt scaffold, cite violated clause, provide remediation steps
- Missing inputs: Request repository path, collaborator list, execution cadence; share example command
- Tooling gap: Flag absence of Jupytext, NBQA, or CI pipeline; reference env-config onboarding
- Governance uncertainty: Escalate if review or archival policy not defined

## Examples
- **Example 1**: `/scaffold-notebook Create Databricks notebook template for churn exploration`
- **Example 2**: `/scaffold-notebook Set up collaborative VS Code notebook with Papermill validation`
- **Example 3**: `/scaffold-notebook Launch feature engineering review workflow with Jupytext`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/notebook-collaboration-coach/templates/env-config.yaml`
