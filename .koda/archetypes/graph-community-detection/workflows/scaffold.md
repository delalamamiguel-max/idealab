---
description: Scaffold governed graph community detection workflow spanning in-memory and distributed engines (Graph Community Detection)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype graph-community-detection --json ` and confirm ENV_VALID. Halt if false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/graph-community-detection/templates/env-config.yaml` for engine thresholds, benchmarking jobs, and security controls

### 3. Parse Input
Extract from $ARGUMENTS: business problem, graph data sources, node/edge volumes, update cadence, privacy classification, target stakeholders, deployment environment (in-memory vs distributed). Request missing context.

### 4. Validate Constraints
Apply hard-stop checks:
- ✘ Reject missing data provenance or consent evidence
- ✘ Block solutions exposing sensitive relationships without masking/aggregation
- ✘ Ensure engine choice matches scale (compare against `max_inmemory_nodes/edges`)
- ✘ Require algorithm transparency (proposed method, parameters)
- ✘ Demand fairness/harm review inputs
- ✘ Require monitoring and drift plans
- ✘ Verify engine resides in approved stack
Explain violations and prescribe remediation.

### 5. Generate Workflow Blueprint
Provide scaffold covering:
- Data contract template capturing schema, lineage, retention, and owners
- Engine selection decision tree (NetworkX/Kuzu vs RelationalAI/NVIDIA cuGraph/Neo4j) with benchmark checklist
- Experiment notebook structure logging algorithms (Louvain, Leiden, label propagation, spectral) with MLflow tracking
- Privacy safeguards (node hashing, edge aggregation, k-anonymity thresholds)
- Explainability artifacts (centrality metrics, bridge edges, visualization guidance)
- Fairness assessment step evaluating community assignments across protected cohorts
- Operational pipeline design (refresh cadence, fallback model, rollback strategy)
- Integration checklist for downstream APIs/dashboards/knowledge graphs
- Monitoring plan (drift metrics, community stability index, alert routing)

### 6. Recommend Enhancements
Suggest optional improvements:
- Automated benchmarking harness comparing algorithms with reproducible seeds
- Streaming ingestion blueprint using Kafka/Delta Live Tables for near-real-time updates
- Visualization stack recommendations (Graphistry, Neo4j Bloom, Gephi exports)
- Documentation links to prior community detection incidents and mitigation playbooks
- Cross-domain knowledge sharing workflow with fraud/network optimization teams

### 7. Validate and Report

## Error Handling
- Hard-stop triggered: Halt scaffold, cite violated clause, and provide remediation checklist
- Missing inputs: Request data sources, scale estimates, algorithm preferences, stakeholder list; share example command
- Tooling gap: Flag absence of approved engine access or benchmark environment; reference env-config onboarding
- Governance ambiguity: Escalate if fairness or monitoring owners undefined

## Examples
- **Example 1**: `/scaffold-graph-community Build customer network community detection across NetworkX and Neo4j`
- **Example 2**: `/scaffold-graph-community Design fraud ring discovery workflow with cuGraph scaling plan`
- **Example 3**: `/scaffold-graph-community Prepare knowledge graph community detection with RelationalAI`

## References
Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/graph-community-detection/templates/env-config.yaml`
