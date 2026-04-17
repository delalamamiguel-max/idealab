---
description: Compare experiment designs, statistical approaches, and promotion readiness across candidate workflows (Experiment Scientist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype experiment-scientist --json ` and require ENV_VALID. Halt if false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/experiment-scientist/templates/env-config.yaml` for threshold defaults, fairness tools, reporting templates

### 3. Parse Input
Extract from $ARGUMENTS: candidate experiment artifacts, comparison goals (speed, statistical power, governance fit), metrics of interest, regulatory constraints, stakeholder priorities. Request missing links (MLflow runs, design docs, approval tickets).

### 4. Establish Evaluation Criteria
Frame comparison along:
- Hypothesis clarity and control/treatment fidelity
- Sample sizing and power sufficiency relative to traffic
- Statistical methodology (frequentist vs Bayesian, sequential testing)
- KPI coverage and risk of cherry-picking
- Fairness assessment breadth and mitigation strategies
- Lineage completeness (datasets, run IDs, git SHAs)
- Governance readiness (Azure DevOps gates, approvals, decision logs)
- Metric tolerance alignment vs baseline

### 5. Analyze Alternatives
For each candidate workflow:
- Score against criteria with qualitative/quantitative evidence
- Highlight any hard-stop violations (missing control, missing stats, lineage gaps)
- Surface strengths/weaknesses for execution speed, transparency, or compliance
- Estimate effort to close identified gaps

### 6. Recommend Path Forward
Provide ranked recommendation:
- Preferred experiment design with rationale and guardrail compliance
- Remediation plan for runner-up options if viable
- Governance implications (approvers to engage, expected timelines)
- Suggested enhancements (adaptive methods, simulations, notifications)

### 7. Summarize and Archive

## Error Handling
- Insufficient data: Request experiment artifacts, traffic assumptions, KPI definitions; provide example command showing required parameters
- Hard-stop encountered: Reject offending workflow and cite constitution clause; recommend remediation before reconsideration
- Ambiguous priorities: Prompt stakeholder alignment on decision criteria (speed vs rigor vs governance)
- Tooling mismatch: Note absent fairness/statistics libraries and direct to env-config setup

## Examples
- **Example 1**: `/compare-experiment Evaluate A/B vs multi-armed bandit for personalization rollout`
- **Example 2**: `/compare-experiment Contrast challenger experiments for credit risk model promotion`
- **Example 3**: `/compare-experiment Assess uplift test variants for marketing campaign with fairness guardrails`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/experiment-scientist/templates/env-config.yaml`
