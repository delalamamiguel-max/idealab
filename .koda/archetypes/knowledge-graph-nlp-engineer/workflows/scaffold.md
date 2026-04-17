---
description: Initialize a new Knowledge Graph NLP Engineer project with required structure and configuration (Knowledge Graph NLP Engineer)
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

### 3. Parse Input
Extract from $ARGUMENTS: document sources, entity types of interest, target graph model, search requirements, QA interface needs, embedding model preference.

### 4. Validate NLP Constraints
- ✘ Reject NER without confidence thresholds
- ✘ Require entity disambiguation strategy
- ✘ Demand embedding model versioning
- ✘ Block ungrounded QA interfaces

### 5. Generate NLP-KG Pipeline
Produce:
- NER pipeline configuration
- Text-to-graph mapping rules
- Semantic search index setup
- NL-to-Cypher translation templates
- `docs/NLP_PIPELINE.md`

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `scaffold-knowledge-graph-nlp-engineer "Set up a new knowledge graph project"`
2. `scaffold-knowledge-graph-nlp-engineer "Review existing implementation for best practices"`

## References

- [knowledge-graph-nlp-engineer-constitution.md](${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/knowledge-graph-nlp-engineer-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/templates/env-config.yaml)
