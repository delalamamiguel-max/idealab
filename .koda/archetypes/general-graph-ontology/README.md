# General Graph Ontology Engineer Archetype

## Overview
This archetype is responsible for designing platform-agnostic ontologies that power enterprise knowledge graphs, reasoning engines, and downstream analytics. It defines the rules for ontology lifecycle management, schema modeling, and semantic reasoning.

## Core Principles
*   **Ontology Lifecycle:** Manage design, publication, and evolution of ontologies.
*   **Schema Modeling:** Define entities, relationships, and attributes clearly.
*   **Data Quality:** Incorporate lineage and provenance into the model.
*   **Harmonization:** Create canonical vocabularies to unify multi-source data.
*   **Platform Agnostic:** Focus on general graph principles first, then strict platform rules.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-general-graph-ontology**: Compare ontology versions or schemas.
*   **debug-general-graph-ontology**: Identify inconsistencies or errors in the ontology.
*   **document-general-graph-ontology**: Generate documentation for ontology classes and properties.
*   **refactor-general-graph-ontology**: optimize or restructure the ontology.
*   **scaffold-general-graph-ontology**: Create a new ontology or taxonomy.
*   **test-general-graph-ontology**: Validate the ontology against data and competency questions.

## Usage
Use `scaffold-general-graph-ontology` to begin modeling a new domain. Use `test-general-graph-ontology` to ensure your model supports the required queries and reasoning.
