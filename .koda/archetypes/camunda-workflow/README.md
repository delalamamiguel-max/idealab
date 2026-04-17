# Camunda Orchestration Archetype

Specialist archetype for Camunda 7 workflow orchestration, covering BPMN 2.0 process design, DMN decision tables, Apache Camel integration, external task patterns, and Spring Boot configuration best practices.

## Structure

```
camunda-orchestration/
├── .windsurf/workflows/              # Specialist workflows
│   ├── scaffold-camunda-orchestration.md   # Build new BPMN/Camel workflows
│   ├── debug-camunda-orchestration.md      # Debug process engine issues
│   ├── compare-camunda-orchestration.md    # Compare workflow approaches
│   ├── test-camunda-orchestration.md       # Generate workflow tests
│   ├── document-camunda-orchestration.md   # Document workflows
│   └── refactor-camunda-orchestration.md   # Refactor BPMN/code
├── scripts/
│   ├── validate_bpmn.sh              # BPMN constitution validator
│   ├── layout_bpmn.sh                # Auto-layout tool wrapper
│   └── layout/                       # Node.js auto-layout module
│       ├── package.json
│       ├── layout-bpmn.js            # Single file layout
│       └── layout-all-bpmn.js        # Batch layout all files
├── templates/
│   └── env-config.yaml               # Environment configuration
├── camumda-orchestration-constitution.md  # Rules and best practices
├── manifest.yaml                     # Archetype metadata for discovery
└── README.md                         # This file
```

## Capabilities

### BPMN 2.0 Workflow Design
- Process modeling with proper element naming and ID conventions
- External task patterns for decoupled, scalable execution
- Call activities with deployment binding for sub-process orchestration
- Event-based gateways (message + timer) for callback patterns
- Multi-instance activities for parallel line-by-line processing
- Error boundary events and fallout handling
- Abort sub-processes via conditional events

### DMN Decision Tables
- Decision table design with appropriate hit policies
- Integration with BPMN processes via business rule tasks

### Apache Camel Integration
- Camel route definitions for message-driven integration
- Kafka consumer/producer patterns
- REST and SOAP integration routes
- Event publishing and subscription

### Error Handling & Fallout
- Reusable fallout sub-process patterns
- User task–based manual resolution
- Decision gateways after every task for fallout/success routing
- Conditional sequence flows for recovery validation

### Testing
- camunda-bpm-assert for process instance verification
- Spock Framework specifications
- H2 in-memory database for test isolation
- BPMN element–level unit testing

## Usage

### Auto-Layout BPMN Diagrams

Fix overlapping flows and improve diagram visibility using the auto-layout tool:

```bash
# Install dependencies (one-time)
cd scripts/layout && npm install && cd ../..

# Layout a single BPMN file
./scripts/layout_bpmn.sh src/main/resources/bpmn/workflow.bpmn

# Layout all BPMN files (creates _layouted.bpmn copies)
./scripts/layout_bpmn.sh --all

# Layout all BPMN files in-place (overwrites originals)
./scripts/layout_bpmn.sh --all --in-place
```

### Scaffold a new BPMN workflow
```
/scaffold-camunda-orchestration Create a BPMN workflow for order activation with external task calls and callback events
```

### Debug a Camunda issue
```
/debug-camunda-orchestration Process instance stuck at gateway after timer event fires
```

### Generate tests for a workflow
```
/test-camunda-orchestration Generate tests for call-and-wait-for-event-flow.bpmn
```

## Technology Stack

- **Camunda 7 EE** with Spring Boot Starter
- **Java 17**, **Groovy 4.x**
- **Maven** build
- **PostgreSQL** (runtime), **H2** (test)
- **Apache Camel** for integration
- **Spock Framework** + **camunda-bpm-assert** for testing
- **Docker/AKS** deployment
