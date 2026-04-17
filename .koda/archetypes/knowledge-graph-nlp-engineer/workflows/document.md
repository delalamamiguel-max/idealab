---
description: Generate documentation for a Knowledge Graph NLP Engineer project (Knowledge Graph NLP Engineer)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Set ARCHETYPES_BASEDIR [⋯]
 
**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory
 
**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set (workflow will halt if this variable is not present in the environment)
 
// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype knowledge-graph-nlp-engineer --json ` and confirm ENV_VALID. Halt if false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/knowledge-graph-nlp-engineer-constitution.md` for guardrails and required artifacts
- Load `${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/templates/env-config.yaml` for tool versions and configuration

### 3. Inventory Pipeline Components
Enumerate from the codebase:
- All NER models used with names, versions, and entity types extracted
- All embedding models with names, versions, and index build dates
- All disambiguation strategies with fallback behaviours
- All NL-to-Cypher templates with supported query patterns
- All QA interface entry points and grounding check status

### 4. Document NLP Pipeline
Update or create `docs/NLP_PIPELINE.md` with:
- End-to-end pipeline diagram: text input → NER → disambiguation → graph write → index update
- NER model section: model name/version, accepted entity types with examples, confidence threshold, evaluation metrics (precision/recall on labeled set)
- Disambiguation section: strategy description, canonical identifier property per entity type, fallback behaviour
- Embedding section: model name/version, index build date, similarity threshold for semantic search

### 5. Document NL-to-Cypher Templates
For each supported query pattern:
- Natural language pattern description and example queries
- Generated Cypher template with parameter placeholders
- Entity types and relationship types covered
- Known limitations and unsupported query forms

### 6. Document QA Interface
- Entry points (API endpoint, CLI, UI)
- Retrieval strategy: subgraph query used to find supporting evidence
- Grounding check implementation: how ungrounded answers are detected and rejected
- "No data found" response format
- Audit trail: how questions and answers are logged

### 7. Document Model Versioning and Operations
- Model version lock: how to update NER or embedding model (including index rebuild step)
- Evaluation procedure for new model candidate
- Rollback procedure if new model degrades quality

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `document-knowledge-graph-nlp-engineer "Generate complete NLP pipeline documentation for biomedical knowledge graph"`
2. `document-knowledge-graph-nlp-engineer "Document NL-to-Cypher templates and supported query patterns"`
3. `document-knowledge-graph-nlp-engineer "Create QA interface documentation including grounding check and audit trail"`

## References

- [knowledge-graph-nlp-engineer-constitution.md](${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/knowledge-graph-nlp-engineer-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/templates/env-config.yaml)
