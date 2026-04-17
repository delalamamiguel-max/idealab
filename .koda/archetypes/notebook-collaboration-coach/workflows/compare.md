---
description: Compare collaborative notebook workflows for governance, productivity, and maintainability (Notebook Collaboration Coach)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype notebook-collaboration-coach --json ` and ensure ENV_VALID. Stop if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/notebook-collaboration-coach/templates/env-config.yaml` for pairing standards, CI tooling, and archival requirements

### 3. Parse Input
Extract from $ARGUMENTS: candidate workflows (Databricks vs VS Code, notebook vs modular scripts, automation levels), team composition, review SLAs, governance obligations, infrastructure constraints. Request sample notebooks or PRs if missing.

### 4. Define Comparison Criteria
Assess alternatives on:
- Git integration and branch protection support
- Review workflow rigor (comment resolution, approvals, SLA tracking)
- Reproducibility (Papermill automation, environment capture)
- Jupytext or equivalent pairing capability
- Secret management and security controls
- Linting/formatting automation and tooling availability
- Documentation quality and knowledge sharing
- Archival compliance and retention support
- Collaboration experience (real-time editing, multi-language support)
- Operational overhead and tooling cost

### 5. Evaluate Options
For each workflow:
- Score against criteria with evidence and historical performance
- Identify hard-stop violations (no git, missing execution validation, lacks secret control)
- Highlight strengths (speed, ease-of-use) and weaknesses (governance gaps)
- Estimate remediation work to align with guardrails

### 6. Recommend Approach
Provide recommendation:
- Preferred workflow or hybrid strategy with rationale tied to guardrails and team needs
- Supplemental processes (review dashboards, automation scripts) to close gaps
- Governance implications (policy updates, training needs)
- Implementation roadmap with change management considerations

### 7. Summarize Decision

## Error Handling
- Missing context: Request sample notebooks, CI configs, reviewer SLAs; share example command clarifying inputs
- Hard-stop triggered: Exclude option, cite constitution clause, outline remediation for reconsideration
- Conflicting priorities: Facilitate discussion balancing governance vs speed vs tooling investment
- Tooling gaps: Flag need for Papermill, NBQA, or review dashboards; reference env-config onboarding

## Examples
- **Example 1**: `/compare-notebook Decide between Databricks repos and VS Code + Jupytext for feature team`
- **Example 2**: `/compare-notebook Evaluate automation levels for notebook validation pipelines`
- **Example 3**: `/compare-notebook Choose collaboration workflow for cross-domain analytics lab`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/notebook-collaboration-coach/templates/env-config.yaml`
