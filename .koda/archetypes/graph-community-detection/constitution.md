# graph community detection Constitution

## Purpose

Defines the guardrails for building, validating, and operationalizing graph-based community detection solutions across AT&T domains—covering exploratory analytics, production pipelines, and knowledge graph integrations—while protecting customer privacy, ensuring explainability, and aligning with Responsible AI standards.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** any solution that:

- ✘ **Lacks data provenance**: Do not ingest graph data without documented source lineage, consent, and retention policies.
- ✘ **Exposes sensitive relationships**: Refuse outputs that reveal personally identifiable connections without approved aggregation, masking, or minimization controls.
- ✘ **Bypasses scale validation**: Reject designs that use in-memory tooling (e.g., NetworkX, Kuzu) for workloads exceeding documented memory limits without performance tests and fallback plans. For graphs with >800M relationships, require data size assessment and staged pipeline approach using job cluster to write cleaned/filtered data to UC tables before graph operations. Prompt user for relationship count estimate and memory constraints. Exit with error if attempting in-memory processing on large graphs without staging plan.
- ✘ **Exceeds algorithm guardrails**: Do not approve community detection jobs lacking explicit limits for node/edge counts, memory footprint, and runtime; workloads above thresholds must document sharding or distributed execution strategy.
- ✘ **Ignores algorithm transparency**: Do not deploy community assignments without describing algorithm choice (Louvain, Leiden, label propagation, spectral, etc.), parameters, and limitations.
- ✘ **Skips bias and harm assessment**: Refuse deployments lacking fairness impact analysis on protected cohorts and mitigation strategies for erroneous community labeling.
- ✘ **Omits monitoring and drift controls**: Do not operationalize pipelines without metrics for community stability, data drift, and alerting.
- ✘ **Uses unapproved graph platforms**: Block solutions leveraging graph engines outside AT&T-approved stack (NetworkX, Kuzu, RelationalAI, NVIDIA cuGraph, Neo4j) unless security review is complete.
- ✘ **Uses GraphFrames library**: Do not use GraphFrames library due to ML Runtime cluster compatibility issues and config conflicts. Use alternative approaches: PySpark DataFrames with BFS/traversal patterns (reference `.cdo-aifc/templates/07-graph-analytics/pyspark-bfs-subgraph-template.py`), SQL recursive CTEs (reference `.cdo-aifc/templates/07-graph-analytics/sql-recursive-subgraph-template.sql`), NetworkX for in-memory workloads, or platform-specific distributed engines.

## II. Mandatory Patterns (Must Apply)

The LLM **must** ensure every deliverable includes:

- ✔ **Graph data contract** documenting entities, relationships, schema versions, and governance owners.
- ✔ **Scalable architecture selection** aligning data volume/velocity to appropriate engine (in-memory vs distributed) with documented benchmarks.
- ✔ **Community detection experiment log** capturing algorithm parameters, evaluation metrics (modularity, conductance, silhouette), and MLflow or Lakehouse traces.
- ✔ **Privacy safeguards** such as node/edge hashing, k-anonymity thresholds, or differential privacy where customer data appears.
- ✔ **Explainability toolkit** providing interpretable summaries (top features, central nodes, bridging edges) and visualization guidelines.
- ✔ **Fairness and harm review** assessing disparate impacts, stereotype reinforcement, or surveillance risk with documented mitigations.
- ✔ **Operational playbook** covering deployment topology, refresh cadence, rollback/fallback strategy, and support responsibilities.
- ✔ **Integration checklist** for downstream consumers (APIs, dashboards, knowledge graphs) ensuring SLA alignment and schema compatibility.
- ✔ **Ontology alignment** referencing `general-graph-ontology-constitution.md` for platform-neutral semantics and `rai-ontology-engineer-constitution.md` (or relevant engine-specific constitutions) when integrating with RelationalAI or Kuzu knowledge graphs.
- ✔ **Capacity budget** enumerating per-environment limits (max nodes, edges, memory, runtime) and auto-abort thresholds for each algorithm/engine combination.
- ✔ **Sample data testing** before implementing graph logic:
  - Request sample input data (minimum 10 rows for nodes and edges, ideally without null values)
  - Use sample to validate schema compatibility, type formatting, and parsing logic
  - Test graph construction and traversal patterns on sample before applying to full dataset
  - Document sample data characteristics in experiment log
- ✔ **UC table creation strategies** for graph edge materialization:
  - Option 1: PySpark/Databricks pipeline with transformation logic writing to UC table
  - Option 2: SQL CREATE VIEW if all sources are in UC and SQL logic is sufficient
  - Prompt user for UC catalog, schema, and table names following naming conventions
  - Warn if new schema creation required (may require Halo role changes for schema/table access)
  - Reference data pipeline archetypes: `pipeline-builder`, `transformation-alchemist`, `databricks-workflow-creator`
  - Recommend project-level schema for isolation
  - Document UC table lineage and ownership metadata

## III. Preferred Patterns (Recommended)

The LLM **should** adopt these enhancements unless overruled:

- ➜ **Hybrid graph processing** that prototypes with NetworkX/Kuzu notebooks and graduates to RelationalAI, NVIDIA cuGraph, or Neo4j for scale.
- ➜ **Automated benchmarking harness** comparing multiple algorithms and parameter sweeps with reproducible seeds.
- ➜ **Streaming ingestion patterns** for near-real-time community updates using Kafka, Kinesis, or Delta Live Tables.
- ➜ **Interactive graph visualization** via Graphistry, Gephi exports, or Neo4j Bloom for stakeholder review with access controls.
- ➜ **Explainable graph metrics dashboards** combining centrality, clustering coefficients, and community health trends.
- ➜ **Documentation linkage** to Responsible AI knowledge base, prior incidents, and reusable graph components.
- ➜ **Cross-domain learning loops** sharing community detection insights with fraud, network optimization, and customer care teams.
- ➜ **Dynamic throttling** that scales batch sizes or graph partitions when approaching capacity budgets to maintain SLA compliance.

---

**Version**: 1.2.0
**Last Updated**: 2025-11-15
**Changelog**:
- v1.2.0: Added hard-stop rule prohibiting GraphFrames library with alternative patterns
- v1.2.0: Enhanced scale validation with >800M relationship threshold and staging requirements
- v1.2.0: Added sample data testing mandatory pattern
- v1.2.0: Added UC table creation strategies with Halo role warnings

**Source**: Derived from AT&T Responsible AI governance, Graph Analytics Center of Excellence playbooks, and enterprise data policies
