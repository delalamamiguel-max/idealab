---
description: Validate a Knowledge Graph NLP Engineer implementation for correctness and best practices (Knowledge Graph NLP Engineer)
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

### 3. Validate NER Pipeline
- Confirm NER model name and version are pinned in `templates/env-config.yaml`
- Run NER pipeline on labeled evaluation set (minimum 20 samples)
- Assert precision ≥ target and recall ≥ target as defined in `docs/NLP_PIPELINE.md`
- Verify confidence threshold is applied and low-confidence entities are rejected

### 4. Validate Entity Disambiguation
- Confirm canonical identifier property exists on all entity node labels
- Run disambiguation pipeline on a set of known duplicate entity names
- Verify each resolves to the correct canonical node (not creating duplicates)
- Check fallback behaviour is defined: create new / merge / flag for review

### 5. Validate Embedding Models
- Confirm embedding model name and version match the stored index version
- Run cosine similarity on known semantically close entity pairs — assert score ≥ threshold
- Run cosine similarity on known dissimilar pairs — assert score ≤ threshold
- Verify semantic search returns correct top-3 results for evaluation queries

### 6. Validate NL-to-Cypher
- Run NL-to-Cypher test suite; assert all queries produce valid, executable Cypher
- Verify generated Cypher uses EXPLAIN cleanly (no syntax errors)
- Test at least one query per supported entity type and relationship type

### 7. Validate QA Grounding
- Submit test questions with known answers in the graph — verify answers are returned and traceable to source nodes
- Submit test questions with no data in graph — verify "no data found" response (not a hallucinated answer)

### 8. Constitution Hard-Stop Compliance
- ✘ No NER without validation — verify confidence threshold is applied
- ✘ No ungrounded answers — verify grounding check is active in QA
- ✘ No unpinned embedding models — verify version is locked in config

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `test-knowledge-graph-nlp-engineer "Validate NER precision/recall against labeled evaluation dataset"`
2. `test-knowledge-graph-nlp-engineer "Check embedding model version consistency and semantic search quality"`
3. `test-knowledge-graph-nlp-engineer "Verify QA interface never returns ungrounded answers"`

## References

- [knowledge-graph-nlp-engineer-constitution.md](${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/knowledge-graph-nlp-engineer-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/templates/env-config.yaml)
