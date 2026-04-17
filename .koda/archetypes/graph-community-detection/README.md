# Graph Community Detection Archetype

## Overview
This archetype defines the guardrails for building, validating, and operationalizing graph-based community detection solutions. It covers exploratory analytics, production pipelines, and knowledge graph integrations while ensuring privacy, explainability, and responsible AI standards.

## Core Principles
*   **Data Provenance:** Ingest graph data only with documented source and consent.
*   **Privacy Protection:** Do not expose sensitive relationships; use masking and aggregation.
*   **Scale Validation:** Validate memory limits and performance for in-memory tools vs. distributed engines.
*   **Algorithm Transparency:** Clearly describe algorithm choices (Louvain, Leiden, etc.) and parameters.
*   **Fairness:** Assess disparate impacts and mitigate surveillance risks.
*   **Monitoring:** Operationalize pipelines with metrics for stability and drift.
*   **Approved Stack:** Use libraries like NetworkX, Kuzu, RelationalAI, or Neo4j within security guidelines.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-graph-community-detection**: Compare algorithm results or graph structures.
*   **debug-graph-community-detection**: Analyze performance bottlenecks or unexpected clusters.
*   **document-graph-community-detection**: Document algorithm choices and schema.
*   **refactor-graph-community-detection**: Optimize graph processing code or queries.
*   **scaffold-graph-community-detection**: Initialize a new community detection project.
*   **test-graph-community-detection**: Validate graph integrity and algorithm stability.

## Usage
Start with `scaffold-graph-community-detection` to set up your environment. Use `test-graph-community-detection` to benchmark your selected algorithm against data volume constraints.
