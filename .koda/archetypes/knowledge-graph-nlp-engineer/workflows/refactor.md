---
description: Improve and optimize existing Knowledge Graph NLP Engineer code and configuration (Knowledge Graph NLP Engineer)
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

### 3. Audit Current Implementation
Review against constitution for:
- NER models missing confidence threshold configuration
- Entity disambiguation strategy absent or undocumented
- Embedding model name/version not pinned in `templates/env-config.yaml`
- NL-to-Cypher templates not versioned or lacking test cases
- QA interface capable of generating ungrounded answers (no retrieval grounding check)
- `docs/NLP_PIPELINE.md` absent or outdated

### 4. Harden NER Pipeline
- Add explicit confidence threshold to all NER model calls; reject entities below threshold
- Document accepted entity types in `docs/NLP_PIPELINE.md` with examples
- Add evaluation step: run NER on 20 labeled samples and assert precision/recall ≥ target
- Pin NER model name and version in `templates/env-config.yaml`

### 5. Strengthen Entity Disambiguation
- Add canonical identifier property to all entity node labels in graph model
- Implement disambiguation: string normalisation → embedding similarity → context scoring
- Document disambiguation logic and fallback behaviour (create new node vs merge vs flag)

### 6. Version Embedding Models
- Pin embedding model name and version in `templates/env-config.yaml`
- Add model version check at pipeline startup; halt if version mismatch with stored index
- Add rebuild index step triggered when model version changes

### 7. Improve NL-to-Cypher and QA
- Add test suite for NL-to-Cypher templates covering node types, relationship types, and filters
- Implement retrieval grounding check in QA: verify answer is traceable to returned subgraph nodes
- Add "no data found" fallback when retrieval returns empty results

### 8. Validate After Refactor
- Run NER pipeline on benchmark corpus and confirm precision/recall targets met
- Verify semantic search returns expected top-5 results on evaluation queries
- Confirm NL-to-Cypher test suite passes; QA grounding check active

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `refactor-knowledge-graph-nlp-engineer "Add confidence thresholds and evaluation metrics to NER pipeline"`
2. `refactor-knowledge-graph-nlp-engineer "Pin embedding model version and add index rebuild trigger on model change"`
3. `refactor-knowledge-graph-nlp-engineer "Add retrieval grounding check to QA interface to prevent hallucinations"`

## References

- [knowledge-graph-nlp-engineer-constitution.md](${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/knowledge-graph-nlp-engineer-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/templates/env-config.yaml)
