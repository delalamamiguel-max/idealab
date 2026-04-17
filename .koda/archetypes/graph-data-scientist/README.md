# Graph Data Scientist Archetype

## Overview
This archetype applies graph data science techniques to knowledge graphs — from running centrality, community detection, and pathfinding algorithms to building graph-native ML pipelines using embeddings, link prediction, and feature extraction via the Neo4j Graph Data Science library.

## Core Principles
*   **Projection-First:** Always work on named graph projections, never directly on the database.
*   **Memory Awareness:** Estimate resource requirements before executing algorithms at scale.
*   **Reproducibility:** Track all algorithm parameters and results for reproducible experiments.
*   **Business-Driven:** Every algorithm must answer a specific business question, not just produce metrics.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **scaffold-graph-data-scientist**: Scaffold workflow for Graph Data Scientist.
*   **debug-graph-data-scientist**: Debug workflow for Graph Data Scientist.
*   **refactor-graph-data-scientist**: Refactor workflow for Graph Data Scientist.
*   **test-graph-data-scientist**: Test workflow for Graph Data Scientist.
*   **compare-graph-data-scientist**: Compare workflow for Graph Data Scientist.
*   **document-graph-data-scientist**: Document workflow for Graph Data Scientist.

## Usage
Start with `scaffold-graph-data-scientist` to set up your environment. Use `test-graph-data-scientist` to validate your implementation.
