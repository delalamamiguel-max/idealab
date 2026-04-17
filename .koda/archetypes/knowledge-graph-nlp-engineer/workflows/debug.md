---
description: Analyse and resolve issues in a Knowledge Graph NLP Engineer implementation (Knowledge Graph NLP Engineer)
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

### 3. Identify Issue Category
Classify from $ARGUMENTS:
- **NER quality**: entities not extracted, wrong types assigned, low precision/recall
- **Entity disambiguation failure**: same entity resolving to multiple graph nodes
- **Embedding drift**: semantic search returning irrelevant results, cosine similarity degraded
- **NL-to-Cypher error**: natural language query producing invalid or incorrect Cypher
- **QA hallucination**: question answering returning ungrounded answers not traceable to graph data
- **Pipeline throughput**: slow text processing, batch ingestion timeouts

### 4. Diagnose Root Cause

**NER quality failures:**
- Check NER model confidence scores — verify threshold is applied before accepting entities
- Inspect entity type mapping: confirm extracted types match target graph node labels
- Evaluate on 20 representative samples and measure precision/recall against expected output

**Entity disambiguation failures:**
- Verify disambiguation strategy is applied (string match, embedding similarity, context window)
- Check for missing canonical identifiers on target nodes
- Run `MATCH (n:Entity) WHERE n.name = '<disputed_name>' RETURN count(n)` to count duplicates

**Embedding drift:**
- Check embedding model name and version against what was used at index build time
- Re-embed a sample set and compare cosine similarity against known good pairs
- Rebuild search index if model has changed since last indexing run

**NL-to-Cypher errors:**
- Log the generated Cypher and run `EXPLAIN` to check syntax and execution plan
- Verify NL-to-Cypher template covers the entity types and relationships present in the query
- Add the failing query to the template test suite

**QA hallucinations:**
- Trace the answer back through the graph: confirm cited nodes/relationships exist
- Verify retrieval step returns relevant subgraph before generating answer
- Enable answer grounding check: if no supporting evidence found, return "no data found"

### 5. Apply Fix and Verify
- Apply targeted fix for identified root cause
- Re-run the failing query or pipeline step and confirm expected output
- Log resolution: root cause, fix applied, evaluation metrics before/after

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `debug-knowledge-graph-nlp-engineer "NER pipeline extracting Person entities with confidence below threshold"`
2. `debug-knowledge-graph-nlp-engineer "Semantic search returning irrelevant results after embedding model upgrade"`
3. `debug-knowledge-graph-nlp-engineer "NL-to-Cypher translation producing syntax errors for compound relationship queries"`

## References

- [knowledge-graph-nlp-engineer-constitution.md](${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/knowledge-graph-nlp-engineer-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/templates/env-config.yaml)
