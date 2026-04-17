# Knowledge Graph Builder Archetype

## Overview
This archetype guides the end-to-end construction of knowledge graphs — from selecting an organizing principle and designing the graph data model, through choosing a graph database, writing Cypher/SPARQL queries, loading data at scale, and integrating the knowledge graph with enterprise information systems.

## Core Principles
*   **Organizing Principle:** Every knowledge graph starts with a clear organizing principle that defines scope and structure.
*   **Graph-Native Modeling:** Model entities and relationships as first-class citizens, not as an afterthought on relational data.
*   **Idempotent Loading:** All data pipelines must be repeatable without creating duplicates.
*   **Schema Validation:** Validate graph schema and constraints before any bulk data operations.
*   **Integration-Ready:** Design knowledge graphs as part of the broader data ecosystem, not in isolation.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **scaffold-knowledge-graph-builder**: Scaffold workflow for Knowledge Graph Builder.
*   **debug-knowledge-graph-builder**: Debug workflow for Knowledge Graph Builder.
*   **refactor-knowledge-graph-builder**: Refactor workflow for Knowledge Graph Builder.
*   **test-knowledge-graph-builder**: Test workflow for Knowledge Graph Builder.
*   **compare-knowledge-graph-builder**: Compare workflow for Knowledge Graph Builder.
*   **document-knowledge-graph-builder**: Document workflow for Knowledge Graph Builder.

## Usage
Start with `scaffold-knowledge-graph-builder` to set up your environment. Use `test-knowledge-graph-builder` to validate your implementation.
