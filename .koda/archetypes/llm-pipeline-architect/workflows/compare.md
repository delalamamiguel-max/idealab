---
description: Compare AI agent orchestration approaches, architectures, and framework choices for pipeline design decisions
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read comparison context from:
`${ARCHETYPES_BASEDIR}/llm-pipeline-architect/llm-pipeline-architect-constitution.md`

Focus on Section II (Mandatory Patterns) for evaluation criteria.

### 2. Identify Comparison Scope

Determine what to compare from $ARGUMENTS:

| Comparison Type | What is Compared | Key Criteria |
|----------------|-----------------|--------------|
| **Framework** | LangChain vs LangGraph vs CrewAI vs Custom | Classify/plan/evaluate support, loop guards, context management |
| **Architecture** | Monolithic vs Pipeline vs Agent Graph | Scalability, testability, observability |
| **Model Routing** | Single model vs Purpose-based vs Cost-optimized | Latency, cost, quality per stage |
| **Evaluation** | LLM-only vs Deterministic+LLM vs Rule-based | Reliability, cost, false positive rate |
| **Context Strategy** | Full replay vs Summarization vs File manifest | Token efficiency, information loss, phase count scaling |
| **Streaming** | SSE vs WebSocket vs Polling vs Callback | Latency, complexity, bidirectional needs |

### 3. Build Comparison Matrix

For each option being compared, evaluate against these criteria:

**Architecture Criteria:**

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Classification support | High | Does it classify intent before routing? |
| Phase decomposition | High | Can it decompose tasks into bounded phases? |
| Evaluation + retry | High | Does it evaluate output and support retry/replan? |
| Loop guards | Critical | Does it prevent infinite evaluation loops? |
| Deterministic gates | High | Does it support non-LLM quality checks? |
| Context handoff | High | How does it pass context between phases? |
| Model routing | Medium | Can it route to different models by purpose? |
| Streaming events | Medium | Does it emit observable events at each stage? |
| Graceful degradation | High | Does it fall back on failure? |
| Extensibility | Medium | How easy to add new stages or modify flow? |

**Operational Criteria:**

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Setup complexity | Medium | Time to get a working pipeline |
| Vendor lock-in | High | Dependency on specific LLM providers |
| Testing surface | Medium | How testable are individual stages? |
| Debugging experience | Medium | How observable are pipeline failures? |
| Community / ecosystem | Low | Available plugins, documentation, examples |
| Token efficiency | High | Token consumption per pipeline run |
| Latency overhead | Medium | Pipeline overhead vs direct LLM call |

### 4. Pre-Built Comparison Tables

#### 4.1 Framework Comparison

| Feature | LangChain | LangGraph | CrewAI | Custom Pipeline |
|---------|-----------|-----------|--------|----------------|
| Intent classification | Manual (chains) | Manual (nodes) | Role-based (implicit) | Full control |
| Task decomposition | SequentialChain | Graph nodes | Task assignment | Planner module |
| Phase evaluation | OutputParser | Conditional edges | Implicit (agent loop) | Evaluator module |
| Loop guards | Manual | Conditional edges | Max iterations config | Loop guard module |
| Deterministic gates | Manual (RunnablePassthrough) | Manual (node logic) | Not built-in | Quality gate module |
| Context handoff | Memory classes | State graph | Shared context object | Context builder |
| Model routing | Model per chain | Model per node | Model per agent | Purpose-based resolver |
| Streaming | Callback handlers | Streaming support | Callback handlers | Event bus |
| Graceful degradation | Try/catch per chain | Fallback edges | Exception handling | Pipeline-level catch |
| Vendor lock-in | Low (adapters) | Low (LangChain based) | Medium | None |
| BluePearl alignment | Partial | Good | Low | Full |

#### 4.2 Model Routing Strategy Comparison

| Strategy | Cost | Latency | Quality | Complexity |
|----------|------|---------|---------|------------|
| Single model (all purposes) | High (overprovisioned) | Consistent | Uniform | Low |
| Purpose-based (think/plan/quick/code) | Optimized | Varies by stage | Matched to task | Medium |
| Complexity-based (simple/medium/complex) | Lowest | Fastest for simple | Risk of under-provisioning | Medium |
| Purpose + Complexity (BluePearl) | Optimal | Optimal | Best fit per phase | High |
| A/B testing with random assignment | Variable | Variable | Data-driven | High |

#### 4.3 Evaluation Strategy Comparison

| Strategy | Reliability | Cost | Speed | False Positive Rate |
|----------|-------------|------|-------|-------------------|
| LLM-only evaluation | Low | High | Slow | High |
| Deterministic gates only | High (for measurable criteria) | None | Instant | Low (but misses nuance) |
| Deterministic + LLM (BluePearl) | High | Medium | Fast (gate first) | Low |
| Human-in-the-loop | Highest | Zero LLM cost | Slowest | Lowest |
| Rule-based with thresholds | Medium | None | Instant | Medium |

#### 4.4 Context Handoff Comparison

| Strategy | Token Efficiency | Information Loss | Scales with Phases | Complexity |
|----------|-----------------|------------------|-------------------|------------|
| Full conversation replay | Poor (grows linearly) | None | Breaks at 3+ phases | Low |
| LLM summarization per phase | Good (~300 tokens/phase) | Some nuance lost | Scales well | Medium |
| File manifest + briefs (BluePearl) | Best (~200 tokens/phase) | Minimal (paths preserved) | Scales indefinitely | Medium |
| Shared state object | Good | None (in-memory) | Memory bound | Low |
| RAG over prior phases | Good | Depends on retrieval | Scales well | High |

### 5. Generate Recommendation

Based on the comparison matrix, produce a structured recommendation:

```text
## Pipeline Architecture Recommendation

**Recommended Approach**: {approach_name}

### Why This Approach

{2-3 sentences explaining the recommendation}

### Alignment with Constitution

| Hard-Stop Rule | Compliance |
|---------------|------------|
| 1.1 Classify every message | {how this approach satisfies it} |
| 1.2 Loop guards | {how this approach satisfies it} |
| 1.3 Deterministic gates | {how this approach satisfies it} |
| 1.4 Context handoff | {how this approach satisfies it} |
| 1.5 Graceful degradation | {how this approach satisfies it} |
| 1.6 No hardcoded models | {how this approach satisfies it} |
| 1.7 Streaming events | {how this approach satisfies it} |

### Trade-offs

| Advantage | Trade-off |
|-----------|-----------|
| {advantage_1} | {trade_off_1} |
| {advantage_2} | {trade_off_2} |

### Migration Path (if applicable)

{Steps to migrate from current approach to recommended approach}
```

---

## Error Handling

**Single Option Provided**: If the user only provides one approach, compare it against the BluePearl reference pipeline pattern and identify gaps.

**Too Many Options**: If more than 4 options are provided, ask the user to prioritize and compare the top 3.

**Non-Pipeline Comparison**: If the comparison is about prompt quality, model evaluation, or other non-pipeline concerns, redirect to the appropriate archetype (responsible-prompting, language-model-evaluation).

## Examples

### Example 1: Framework Choice
```text
/compare-llm-pipeline-architect "
Compare LangGraph vs building a custom pipeline for our
multi-agent system. We need intent classification, phased
planning with max 4 phases, and evaluation with retry.
Currently using TypeScript with OpenAI.
"
```

### Example 2: Evaluation Strategy
```text
/compare-llm-pipeline-architect "
Should we use LLM-only evaluation or add deterministic gates?
Our pipeline has 3 phases: analyze, implement, test.
The implement phase often completes without writing files.
"
```

### Example 3: Context Strategy
```text
/compare-llm-pipeline-architect "
Our pipeline degrades at phase 4+. Compare full conversation
replay vs summarization vs file manifest handoff. We run
6-phase plans regularly.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/llm-pipeline-architect/llm-pipeline-architect-constitution.md` Sections I, II
- **Related**: scaffold-llm-pipeline-architect, refactor-llm-pipeline-architect
