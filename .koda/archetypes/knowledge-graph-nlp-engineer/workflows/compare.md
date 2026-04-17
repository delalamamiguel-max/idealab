---
description: Compare two Knowledge Graph NLP Engineer implementations or approaches (Knowledge Graph NLP Engineer)
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

### 3. Parse Comparison Request
Extract from $ARGUMENTS:
- Comparison type: NER models, embedding models, disambiguation strategies, NL-to-Cypher approaches, QA architectures, or full pipeline implementations
- Candidate A and Candidate B descriptions
- Evaluation criteria: accuracy, latency, cost, hallucination rate, maintainability

### 4. Build Comparison Matrix
For each candidate evaluate:
- **NER accuracy**: precision/recall on domain-specific entity types
- **Disambiguation quality**: duplicate entity rate on benchmark corpus
- **Embedding quality**: cosine similarity on semantic pair evaluation set
- **NL-to-Cypher coverage**: percentage of evaluation queries producing correct Cypher
- **QA grounding rate**: percentage of answers traceable to graph data (no hallucinations)
- **Pipeline throughput**: documents processed per second at target batch size
- **Constitution compliance**: confidence thresholds, model pinning, grounding check all present

### 5. Apply Domain-Specific Criteria
- **Scientific literature**: prioritise NER recall for domain entities (genes, compounds, diseases)
- **Enterprise search**: prioritise NL-to-Cypher coverage and QA grounding
- **Real-time ingestion**: prioritise pipeline throughput and low-latency embedding
- **Compliance/legal**: prioritise disambiguation accuracy and audit trail

### 6. Produce Recommendation
- Select preferred approach with constitution-backed justification
- Summarise accuracy vs throughput trade-offs
- Recommend confidence threshold and model version starting points

## Error Handling

- If `validate_env.py` fails, install missing dependencies and retry.
- If constitution file is missing, halt and report.
- Log all validation failures with step number and remediation advice.

## Examples

1. `compare-knowledge-graph-nlp-engineer "spaCy NER vs transformer-based NER for biomedical entity extraction"`
2. `compare-knowledge-graph-nlp-engineer "OpenAI embeddings vs sentence-transformers for semantic search over knowledge graph"`
3. `compare-knowledge-graph-nlp-engineer "Template-based NL-to-Cypher vs LLM-based NL-to-Cypher for enterprise search"`

## References

- [knowledge-graph-nlp-engineer-constitution.md](${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/knowledge-graph-nlp-engineer-constitution.md)
- [env-config.yaml](${ARCHETYPES_BASEDIR}/knowledge-graph-nlp-engineer/templates/env-config.yaml)
