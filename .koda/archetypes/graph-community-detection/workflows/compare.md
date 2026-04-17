---
description: Compare graph community detection strategies for accuracy, scalability, and governance compliance (Graph Community Detection)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype graph-community-detection --json ` and ensure ENV_VALID. Stop if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/graph-community-detection/templates/env-config.yaml` for engine thresholds, benchmarking defaults, and fairness requirements

### 3. Parse Input
Extract from $ARGUMENTS: candidate algorithms/platforms (e.g., NetworkX Louvain, cuGraph Leiden, RelationalAI spectral, Neo4j GDS), graph scale, latency budget, privacy classification, downstream integrations, stakeholder priorities. Request supporting artifacts (MLflow runs, benchmark logs, community metrics) if missing.

### 4. Define Comparison Criteria
Assess each option on:
- Data governance readiness (contract, lineage, consent)
- Scalability vs engine capabilities and cost
- Algorithm performance (modularity, conductance, purity) and reproducibility
- Fairness/harm impact across protected cohorts
- Privacy safeguards and minimization controls
- Explainability and visualization support
- Monitoring and drift management capabilities
- Integration complexity with downstream systems
- Operational overhead (refresh cadence, infrastructure, licensing)
- Alignment with approved tooling stack

### 5. Analyze Alternatives
For each candidate:
- Score against criteria with evidence from benchmarks and MLflow logs
- Flag hard-stop violations (non-approved tool, missing fairness review, privacy gap)
- Highlight strengths/weaknesses (accuracy, interpretability, cost)
- Estimate remediation required to meet guardrails

### 6. Recommend Path Forward
Provide recommendation:
- Preferred algorithm/engine combo with rationale tied to guardrails and business goals
- Secondary options and remediation steps if conditions change
- Governance implications (additional reviews, documentation updates)
- Suggested enhancements (hybrid approach, benchmarking automation, visualization stack)

### 7. Summarize Decision

## Error Handling
- Missing context: Request benchmark data, MLflow runs, privacy requirements; provide example command clarifying expectations
- Hard-stop triggered: Exclude option, cite constitution clause, offer remediation guidance
- Conflicting priorities: Facilitate discussion on accuracy vs speed vs governance trade-offs
- Tooling limitations: Flag need for GPU cluster, RelationalAI license, or Neo4j capacity; reference env-config onboarding

## Examples
- **Example 1**: `/compare-graph-community Decide between cuGraph Leiden and RelationalAI spectral clustering`
- **Example 2**: `/compare-graph-community Evaluate Kuzu vs Neo4j GDS for network operations data`
- **Example 3**: `/compare-graph-community Choose hybrid architecture for marketing community discovery`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/graph-community-detection/templates/env-config.yaml`
