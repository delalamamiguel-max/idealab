# Identity Graph Specialist Archetype

## Overview
This archetype builds identity and metadata knowledge graphs that power entity resolution, master data management, and data governance. It covers techniques for record linkage, fuzzy matching, confidence scoring, metadata cataloging, data lineage tracking, and golden record construction.

## Core Principles
*   **Privacy by Design:** Protect PII with encryption and masking at every layer of the identity graph.
*   **Confidence Scoring:** Every identity match must carry a traceable confidence score.
*   **Auditability:** All merge/split decisions must be logged and reversible.
*   **Cross-Source Validation:** Identity resolution requires evidence from multiple independent sources.
*   **Metadata as First-Class:** Treat metadata (lineage, quality, ownership) as graph-native entities, not annotations.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **scaffold-identity-graph-specialist**: Scaffold workflow for Identity Graph Specialist.
*   **debug-identity-graph-specialist**: Debug workflow for Identity Graph Specialist.
*   **refactor-identity-graph-specialist**: Refactor workflow for Identity Graph Specialist.
*   **test-identity-graph-specialist**: Test workflow for Identity Graph Specialist.
*   **compare-identity-graph-specialist**: Compare workflow for Identity Graph Specialist.
*   **document-identity-graph-specialist**: Document workflow for Identity Graph Specialist.

## Usage
Start with `scaffold-identity-graph-specialist` to set up your environment. Use `test-identity-graph-specialist` to validate your implementation.
