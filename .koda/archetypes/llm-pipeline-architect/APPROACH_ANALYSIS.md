# LLM Pipeline Architect: Approach Analysis

**Analysis Date**: March 2026
**Source**: `docs/plans/new-archetypes.md` § CREATE NEW #3
**Status**: Pre-creation analysis — constitution and workflows not yet built

---

## 1. Why This Archetype Exists

No existing archetype covers building AI agent orchestration pipelines. `language-model-evaluation` covers evaluating model outputs but not the pipeline that drives multi-phase task execution. This is a rapidly growing domain with no standard patterns — teams building agent systems today are reinventing the same architectural primitives (intent classification, task decomposition, phase evaluation, retry logic, context handoff) from scratch.

Teams that build agent pipelines without a structured approach end up with:

- Monolithic prompt chains with no classification or routing
- No retry or evaluation — phases run once and output is accepted unconditionally
- Context window exhaustion — full conversation history passed to every phase
- No deterministic quality gates — relying entirely on LLM judgment
- Infinite loops when evaluation says "retry" with no guard
- No observability — pipeline failures are silent
- All models treated equally — no purpose-based routing (thinking vs coding vs quick evaluation)

---

## 2. Reference Implementation

BluePearl's orchestration pipeline is the battle-tested reference, representing ~2,500 lines of production code across 10+ modules:

| File | Lines | Role |
|------|-------|------|
| `backend/orchestrator/src/pipeline.ts` | ~977 | Core orchestration: classify → route → plan → execute loop. 7 stages, PhaseExecuteHandler callback, MessageSink, DirectHandler fast-path, compare-first enforcement, phase evaluation loop |
| `backend/orchestrator/src/classify/intent-classifier.ts` | ~120 | QUICK model binary classification (plan/chat) + code-level heuristic fallback |
| `backend/orchestrator/src/classify/routing-analyzer.ts` | ~80 | Infers workflow types from intent (scaffold/refactor/compare) |
| `backend/orchestrator/src/plan/task-planner.ts` | ~200 | THINK model decomposes request into phased plan (max 6 phases), skill name normalization |
| `backend/orchestrator/src/plan/compare-enforcer.ts` | ~60 | Deterministic: if plan has skill phases, first must be `compare` workflow |
| `backend/orchestrator/src/plan/archetype-override.ts` | ~50 | Validates skill names; unknown skills → archetype-architect |
| `backend/orchestrator/src/evaluate/phase-evaluator.ts` | ~150 | QUICK model evaluates sub-agent output; verdicts: proceed/retry/replan/summarize |
| `backend/orchestrator/src/evaluate/loop-guard.ts` | ~60 | Per-step evaluation counter (max 3), global replan counter (max 1) |
| `backend/orchestrator/src/execute/phase-learnings.ts` | ~80 | QUICK model extracts operational learnings; persisted to `.bluepearl/phase-learnings.md` |
| `backend/orchestrator/src/prompt/context-builder.ts` | ~150 | Builds phase-contextualized prompts with completed phase summaries, file manifests, learnings |
| `backend/orchestrator/src/prompt/template-engine.ts` | ~173 | Isolated Handlebars instance, type-safe template registry, multi-path resolution, input sanitization |
| `backend/shared/src/model-tiers.ts` | ~200 | 3-tier model preference with LiteLLM probe logic, purpose-based resolution |

### Key Patterns to Encode

1. **Always-on pipeline** — Every message passes through classify → route → plan → execute; direct chat is a fast-path, not a bypass
2. **Intent classification** — QUICK model binary decision (plan/chat) + code-level heuristic fallback for edge cases
3. **Task decomposition** — THINK model breaks request into max N phases, each with id, instruction, purpose, skill, workflow
4. **Purpose-based model routing** — 12 purpose slots (think, plan, implement, code, quick, chat, etc.) mapped to tiered models
5. **Phase execution loop** — Primary session executes each phase; pipeline controls flow via callbacks
6. **Phase evaluation with verdicts** — proceed, retry, replan, summarize; each with distinct behavior
7. **Deterministic quality gates** — Hard zero-write gate before LLM evaluator (if no files written and code phase, auto-retry)
8. **Loop guards** — Per-step max retries (3) + global replan limit (1); prevents infinite retry/replan loops
9. **Context handoff** — File manifest + phase output briefs passed between phases; no full conversation replay
10. **Cross-phase memory** — QUICK model extracts learnings; persisted to disk; injected into subsequent phases
11. **Compare-first enforcement** — If plan has skill phases, first phase must be `compare` workflow (deterministic, no LLM)
12. **Message sink pattern** — Pipeline injects status updates (plan announcements, phase summaries) into chat stream
13. **Streaming event architecture** — Typed event bus for real-time pipeline status to clients
14. **Graceful degradation** — Pipeline catch block falls back to direct session.prompt() on any failure

---

## 3. Scope Boundaries

### In Scope

- Pipeline entry point architecture (classify → route → plan → execute)
- Intent classification (LLM + code heuristic hybrid)
- Task decomposition / planning (LLM-based, max phase limits)
- Purpose-based model routing (purpose → tier → specific model)
- Phase execution patterns (callback-based, sub-agent isolation)
- Phase evaluation with verdict types (proceed/retry/replan/summarize)
- Loop guards (per-step + global limits)
- Deterministic quality gates (zero-write gate, file count verification)
- Context handoff between phases (file manifests, output briefs, truncation)
- Cross-phase memory / learnings extraction and persistence
- Streaming event architecture (typed event bus, SSE/WebSocket)
- Message sink pattern for injecting status into chat
- Compare-first enforcement pattern
- Plan announcement and phase summary injection
- Pipeline observability (classification events, routing decisions, phase timing)
- Cost-aware model selection (tier-based with fall-up logic)
- Graceful degradation and fallback strategies
- Token budget management per pipeline run

### Out of Scope (Delegated)

- Prompt content quality / ethical guidelines → `responsible-prompting`
- Prompt template engine implementation → `prompt-template-engineer`
- Model evaluation and benchmarking → `language-model-evaluation`
- RAG / retrieval systems → future archetype
- Fine-tuning workflows → `model-architect`
- Agent tool implementation → `automation-scripter`
- Frontend chat UI → `frontend-only`

---

## 4. Industry Standards Alignment

| Practice | Standard/Source | Constitution Section |
|----------|----------------|---------------------|
| Intent classification before routing | LangChain, Semantic Router | Hard-stop: classify every message |
| Multi-model routing by purpose | OpenRouter, LiteLLM patterns | Mandatory pattern |
| Phased task decomposition | ReAct, Plan-and-Execute | Mandatory pattern |
| Output evaluation with retry | LATS, Reflexion | Mandatory pattern |
| Deterministic quality gates | Engineering best practice | Hard-stop rule |
| Context window management | RAG patterns | Mandatory pattern |
| Streaming event architecture | SSE/WebSocket patterns | Mandatory pattern |
| Graceful degradation | Circuit breaker pattern | Mandatory pattern |
| Prompt injection defense | OWASP LLM Top 10 | Hard-stop rule |
| Observability / tracing | OpenTelemetry | Recommended pattern |
| Loop guards / runaway prevention | Engineering best practice | Hard-stop rule |
| Cost tracking | LiteLLM callbacks | Recommended pattern |
| Token budget management | Best practice | Recommended pattern |
| A/B testing models | MLOps | Future enhancement |
| Content guardrails | NeMo Guardrails, Guardrails AI | Future enhancement |

### Gaps Beyond BluePearl Reference (to address in constitution)

| Gap | Priority | Approach |
|-----|----------|----------|
| Token budget per pipeline | High | Add total token counter; abort or switch to cheaper model when budget exceeded |
| Cost tracking per run | Medium | Add model cost lookup table; emit cost events for observability |
| A/B model testing | Low | Add random assignment for model variants in purpose routing |
| Content guardrails | Medium | Add optional pre/post-LLM content filtering hooks |
| Pipeline versioning | Low | Add version field to pipeline config for A/B pipeline testing |
| Parallel phase execution | Medium | Add dependency graph for phases that can run concurrently |
| Human-in-the-loop gates | Medium | Add approval checkpoint between phases for sensitive operations |

---

## 5. Constitution Structure Plan

### Hard-Stop Rules (non-negotiable)

1. **Classify every message** — No message bypasses intent classification; even direct chat is an explicit classification result
2. **Loop guards on every evaluation** — Per-step retry limit (configurable, default 3) and global replan limit (default 1); no unbounded loops
3. **Deterministic gates before LLM evaluation** — At least one non-LLM quality check per phase (e.g., zero-write gate for code phases)
4. **Context handoff, not full replay** — Phases receive summaries and file manifests, not full conversation history
5. **Graceful degradation** — Pipeline failures must fall back to direct execution; never leave user with no response
6. **No hardcoded model names** — All model references via purpose-based resolution; models are configuration, not code
7. **Streaming events for every stage** — Classification, routing, planning, phase start/end, evaluation must emit observable events

### Mandatory Patterns

1. Pipeline entry point (classify → route → plan → execute)
2. Intent classifier (QUICK model + code heuristic)
3. Task planner (THINK model → phased plan with limits)
4. Phase execution loop with callback pattern
5. Phase evaluator with verdict types
6. Loop guard with configurable limits
7. Deterministic quality gate (at least one)
8. Context builder with file manifest + output briefs
9. Message sink for status injection
10. Typed event bus for streaming

### Recommended Patterns

1. Cross-phase memory / learnings extraction
2. Compare-first enforcement
3. Plan announcement injection
4. Phase summary injection
5. Purpose-based model tiering with probe logic
6. Cost tracking per pipeline run
7. Token budget management
8. Human-in-the-loop approval gates

---

## 6. Workflow Plan

| Workflow | Purpose | Key Deliverables |
|----------|---------|-----------------|
| **scaffold** | Full pipeline from scratch | Pipeline entry point, intent classifier, task planner, phase executor, phase evaluator, loop guard, quality gate, context builder, event bus, message sink, model router |
| **compare** | Compare pipeline approaches | Side-by-side of LangChain vs LangGraph vs CrewAI vs custom pipeline vs BluePearl-style callback pattern |
| **refactor** | Improve existing pipeline | Audit current flow → identify missing stages → add classification/evaluation/guards → improve context handoff |
| **test** | Pipeline integration tests | Classification accuracy tests, planner output validation, evaluator verdict tests, loop guard limit tests, quality gate tests, end-to-end pipeline flow tests |
| **debug** | Fix pipeline issues | Silent failures, infinite loops, context exhaustion, wrong model routing, missing events, evaluation always-proceed |
| **document** | Generate pipeline docs | Pipeline flow diagram, stage documentation, model routing table, event catalog, configuration reference |

---

## 7. Keyword Differentiation from Related Archetypes

| Query | Expected Route | Rationale |
|-------|---------------|-----------|
| "Build an AI agent system" | `llm-pipeline-architect` | Core capability |
| "Evaluate my LLM outputs" | `language-model-evaluation` | Output evaluation, not pipeline |
| "Create ethical AI prompts" | `responsible-prompting` | Prompt content, not orchestration |
| "Route messages to different models" | `llm-pipeline-architect` | Model routing |
| "Build a multi-step AI workflow" | `llm-pipeline-architect` | Multi-phase execution |
| "Test my prompt quality" | `language-model-evaluation` | Evaluation focus |
| "Add retry logic to my AI pipeline" | `llm-pipeline-architect` | Phase evaluation |
| "Classify user intent" | `llm-pipeline-architect` | Intent classification |
| "Build a RAG system" | N/A (future archetype) | Retrieval, not orchestration |
| "Fine-tune a model" | `model-architect` | Training, not orchestration |

**Routing conflict risk**: LOW — keywords are distinct (`llm-pipeline`, `agent-orchestration`, `task-planning`, `phase-evaluation`, `loop-guard` vs `language-model-evaluation`'s `grader`, `benchmark`, `eval`).

---

## 8. Implementation Approach

### Phase 1: Constitution

1. Read BluePearl orchestrator source code (pipeline.ts, intent-classifier.ts, task-planner.ts, phase-evaluator.ts, loop-guard.ts, context-builder.ts, phase-learnings.ts)
2. Extract the 7 hard-stop rules from operational experience and bug fixes
3. Define 10 mandatory patterns with architectural diagrams
4. Incorporate industry gaps (token budget, cost tracking, human-in-the-loop)
5. Create refusal template for anti-patterns (no classification, no loop guards, hardcoded models)

### Phase 2: Workflows

1. **scaffold** first — most complex, establishes all 12 deliverables
2. **test** second — validates scaffold output (classification accuracy, loop guard limits)
3. **debug** third — addresses most common pipeline failures from operational experience
4. **compare**, **refactor**, **document** — follow standard patterns

### Phase 3: Validation

1. Run scaffold on a fresh TypeScript project
2. Verify all 12 pipeline components produced and wired together
3. Run test workflow to validate classification, evaluation, and loop guards
4. Run debug workflow against a pipeline with a known infinite-loop bug

---

## 9. Subcomponents Absorbed (from DISCARD list)

The following innovations from `docs/plans/new-archetypes.md` are subcomponents of this archetype and will be covered within its constitution/workflows:

| Innovation | How Covered |
|-----------|-------------|
| Auto-continuation system | Phase execution loop pattern |
| Compare-first enforcement | Deterministic enforcement pattern |
| File-write enforcement (4-layer) | Quality gate pattern |
| File manifest context handoff | Context builder pattern |
| Phase evaluation & retry loop | Phase evaluator + loop guard |
| Dynamic skill creation (archetype override) | Recommended pattern |
| Phase learnings cross-phase memory | Cross-phase memory pattern |
| Execution request synthesis | Plan announcement pattern |
| Purpose-based model routing | Model routing mandatory pattern |

---

## 10. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Framework coupling (TypeScript-specific) | High | Constitution must define patterns generically; scaffold can target TypeScript but patterns are language-agnostic |
| LLM API differences (OpenAI vs Anthropic vs local) | Medium | Purpose-based routing abstracts model selection; use OpenAI-compatible interface as common denominator |
| Rapidly evolving agent frameworks (LangGraph, CrewAI, AutoGen) | Medium | Focus on architectural primitives (classify, plan, evaluate, guard) that transcend any framework |
| Pipeline complexity overwhelming for simple use cases | Medium | Direct-chat fast-path must be first-class; pipeline only activates for multi-phase requests |
| Evaluation quality depends on model capability | Medium | Deterministic gates as first line; LLM evaluation as second layer |

---

*This document guides the creation of the `llm-pipeline-architect` archetype. Review and approve before proceeding with constitution and workflow authoring.*
