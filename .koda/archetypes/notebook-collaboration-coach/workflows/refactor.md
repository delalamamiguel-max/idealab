---
description: Refactor collaborative notebook to enforce source control, reproducibility, and review guardrails (Notebook Collaboration Coach)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype notebook-collaboration-coach --json ` and confirm ENV_VALID. Abort if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/notebook-collaboration-coach/templates/env-config.yaml` for pairing rules, linting config, and archival policies

### 3. Parse Input
Extract from $ARGUMENTS: notebook path, identified issues (missing pairing, hidden state, failed reviews), collaborators, deadline. Request PR link, CI results, and archival status if missing.

### 4. Assess Current Notebook
Review for:
- Not under git control or lacking branch policy adherence
- Absent reviewer assignments or unresolved comment threads
- Hidden state dependencies (manual steps, skipped cells)
- Missing Jupytext pairing or desynchronized `.py/.R`
- Inline secrets or credentials
- Failing Papermill/NBQA validation or missing CI integration
- Formatting/linting violations (Black/Ruff, isort)
- Sparse documentation and follow-up notes

### 5. Refactor Plan
Recommend changes:
- Move notebook into protected branch workflow with PR template usage
- Assign reviewers and enforce comment resolution before merge
- Reorder cells for top-to-bottom execution; add environment setup cells
- Establish Jupytext pairing and ensure bi-directional sync
- Replace secrets with environment configs/secret scopes
- Configure Papermill/NBQA jobs in CI and fix failing tests
- Apply formatting/linting tools and remove extraneous output
- Enhance documentation cells with summary, next steps, and decisions
- Archive executed notebooks with sanitized outputs in governed storage

### 6. Sustain Improvements
Suggest enhancements:
- Modularize repeated logic into shared packages with unit tests
- Add review dashboard to monitor SLA adherence
- Integrate auto-comment bots for stale reviews
- Provide pair-programming guidance for complex workstreams
- Sync documentation with Confluence or internal portals automatically

### 7. Validate and Report

## Error Handling
- Hard-stop persists: Refuse completion until git control, Jupytext pairing, or execution validation restored
- Missing evidence: Request PR link, CI logs, archival location; provide example command clarifying expectations
- Tooling absence: Flag need for NBQA, Papermill, or branch protections; reference env-config onboarding
- Governance conflict: Escalate if reviewers unavailable or policies waived without approval

## Examples
- **Example 1**: `/refactor-notebook Align Databricks exploration notebook with Jupytext workflow`
- **Example 2**: `/refactor-notebook Fix Papermill validation failures in fraud analysis notebook`
- **Example 3**: `/refactor-notebook Remove secrets and enforce review checklist for churn study`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/notebook-collaboration-coach/templates/env-config.yaml`
