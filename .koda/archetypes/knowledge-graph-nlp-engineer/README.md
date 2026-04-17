# Knowledge Graph NLP Engineer Archetype

## Overview
This archetype bridges NLP and knowledge graphs — from extracting entities and relationships from text using NER pipelines, through building semantic search over graph-enriched content, to enabling natural language querying of knowledge graphs. It also covers the knowledge lake pattern that unifies structured and unstructured data.

## Core Principles
*   **Grounded Answers:** All query responses must be traceable to specific graph data, never hallucinated.
*   **Validated Extraction:** NER outputs must pass confidence and disambiguation checks before graph ingestion.
*   **Versioned Models:** All NLP and embedding models must be versioned for reproducibility.
*   **Multi-Modal by Design:** Plan for combining text, structured data, and graph relationships from the start.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **scaffold-knowledge-graph-nlp-engineer**: Scaffold workflow for Knowledge Graph NLP Engineer.
*   **debug-knowledge-graph-nlp-engineer**: Debug workflow for Knowledge Graph NLP Engineer.
*   **refactor-knowledge-graph-nlp-engineer**: Refactor workflow for Knowledge Graph NLP Engineer.
*   **test-knowledge-graph-nlp-engineer**: Test workflow for Knowledge Graph NLP Engineer.
*   **compare-knowledge-graph-nlp-engineer**: Compare workflow for Knowledge Graph NLP Engineer.
*   **document-knowledge-graph-nlp-engineer**: Document workflow for Knowledge Graph NLP Engineer.

## Usage
Start with `scaffold-knowledge-graph-nlp-engineer` to set up your environment. Use `test-knowledge-graph-nlp-engineer` to validate your implementation.
