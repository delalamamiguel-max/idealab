---
description: Design and build a complete AI agent orchestration pipeline with intent classification, task planning, phase execution, evaluation, loop guards, quality gates, context handoff, and streaming events
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read all rules and patterns from:
`${ARCHETYPES_BASEDIR}/llm-pipeline-architect/llm-pipeline-architect-constitution.md`

Focus on Section I (Hard-Stop Rules 1.1-1.7) and Section II (Mandatory Patterns 2.1-2.10).

### 2. Gather Requirements

Extract from $ARGUMENTS:

| Requirement | Description | Default |
|------------|-------------|---------|
| **Language** | TypeScript, Python, or other | TypeScript |
| **LLM Provider** | OpenAI, Anthropic, LiteLLM proxy, or custom | OpenAI-compatible |
| **Framework** | Standalone, LangChain adapter, or custom | Standalone |
| **Phase Limit** | Maximum phases per plan | 6 |
| **Retry Limit** | Max evaluations per step | 3 |
| **Replan Limit** | Max replans per run | 1 |
| **Model Purposes** | Which purpose slots to support | think, plan, implement, code, quick, chat |
| **Streaming** | SSE, WebSocket, or callback-only | SSE |
| **Skill System** | Archetype/skill integration | Optional |

If requirements are incomplete, ask:

```
To scaffold your pipeline, I need:
1. Language: TypeScript or Python?
2. LLM provider: OpenAI, Anthropic, LiteLLM, or custom?
3. How should phases stream status? SSE, WebSocket, or callbacks?
4. Do you need skill/archetype integration for domain-specific phases?
5. Any custom quality gates beyond the zero-write gate?
```

### 3. Generate Pipeline Entry Point

Create the core orchestration module implementing Pattern 2.1:

**File**: `src/pipeline.ts` (or `pipeline.py`)

Must include:
1. Type definitions: `MessageSink`, `DirectHandler`, `PhaseExecuteHandler`, `PhaseExecutionResult`, `PipelineConfig`, `PipelineResult`
2. `runPipeline(message, config)` function with the full flow:
   - Stage 1: Intent Classification (QUICK model) — Rule 1.1
   - Stage 2: Routing Analysis (direct / single-skill / multi-skill)
   - Stage 3: Task Planning (THINK model)
   - Stage 3b: Empty-workflow safety valve
   - Stage 4: Compare-first enforcement (if skill system enabled)
   - Stage 5: Plan announcement via message sink
   - Stage 6: Phase execution loop (while-loop, not for-each) — Pattern 2.4
   - Stage 7: Completion and result assembly
3. Try/catch wrapping the entire pipeline with fallback to `onDirect` — Rule 1.5
4. Event emission at every stage — Rule 1.7

**Validation**: After generation, verify:
- No hardcoded model names (Rule 1.6)
- Loop guard initialized before phase loop (Rule 1.2)
- At least one deterministic gate before LLM evaluation (Rule 1.3)
- Context handoff uses briefs, not raw output (Rule 1.4)

### 4. Generate Intent Classifier

Create the classification module implementing Pattern 2.2:

**File**: `src/classify/intent-classifier.ts`

Must include:
1. Non-actionable phrase regex for short-circuit (greetings, thanks, etc.)
2. Slash command detection and routing
3. Default-to-chat behavior (agent decides when to plan)
4. Structured output: `IntentClassification` with `utteranceType`, `purpose`, `confidence`, `requiresPlanning`, `suggestedSkills`, `routing`

### 5. Generate Routing Analyzer

**File**: `src/classify/routing-analyzer.ts`

Must include:
1. Route determination from classification: `direct`, `single-skill`, `multi-skill`
2. Workflow type inference: scaffold, refactor, compare, test, debug, document
3. Skill suggestion extraction

### 6. Generate Task Planner

Create the planning module implementing Pattern 2.3:

**File**: `src/plan/task-planner.ts`

Must include:
1. THINK model prompt that produces JSON phased plans
2. Phase schema: id, instruction, purpose, skill, workflow, dependsOn, complexity
3. Maximum phase limit enforcement (default: 6)
4. Fallback single-phase plan on JSON parse failure
5. Skill name normalization (lowercase, trim, handle common variants)
6. Optional auto-select model resolution per phase based on complexity

### 7. Generate Phase Evaluator

Create the evaluation module implementing Pattern 2.5:

**File**: `src/evaluate/phase-evaluator.ts`

Must include:
1. QUICK model evaluation with structured JSON output
2. Four verdict types: proceed, return-to-step, replan, summarize
3. Output truncation before evaluation (max 8,000 chars)
4. Completed phases context for cumulative evaluation
5. File operation counts (explicitWrites, fileOps) in evaluation context
6. Fallback to `proceed` on evaluation failure

### 8. Generate Loop Guard

Create the loop guard implementing Pattern 2.6:

**File**: `src/evaluate/loop-guard.ts`

Must include:
1. `LoopGuardState` type with `evaluationsPerStep: Map` and `replansUsed: number`
2. `createLoopGuard()` factory
3. `canEvaluate(guard, stepId)` and `recordEvaluation(guard, stepId)`
4. `canReplan(guard)` and `recordReplan(guard)`
5. Configurable limits with sensible defaults (3 per step, 1 replan)

### 9. Generate Context Builder

Create the context assembly module implementing Pattern 2.8:

**File**: `src/prompt/context-builder.ts`

Must include:
1. `PhaseContext` type with phaseIndex, totalPhases, currentPhase, completedPhases, isLastPhase, phaseOutputs, phaseLearnings
2. `buildPhaseContextPrompt(ctx)` function that assembles:
   - Phase position and instruction
   - Completed phase briefs (~300 chars each)
   - File manifest (paths only)
   - Cross-phase learnings (from disk)
   - Last-phase instruction if applicable

### 10. Generate Event Bus and Types

Create the event system implementing Pattern 2.10:

**File**: `src/events/event-bus.ts` and `src/types.ts`

Must include:
1. `PipelineEvents` interface with all 8 event types
2. `EventBus<T>` generic with `emit(event, data)` and `on(event, handler)`
3. Type definitions for: IntentClassification, RoutingDecision, TaskPlan, PlannedPhase, PhaseResult, PhaseEvaluation, EvaluationVerdict, ModelPurpose

### 11. Generate Model Router (if purpose-based routing requested)

**File**: `src/models/model-router.ts`

Must include:
1. Purpose slots: think, plan, implement, code, quick, chat, default
2. `resolveModelForPurpose(purpose, config)` function
3. Configuration-based model mapping (no hardcoded model names — Rule 1.6)
4. Optional tier probing for LiteLLM-based setups

### 12. Generate Cross-Phase Learnings (if requested)

**File**: `src/execute/phase-learnings.ts`

Must include:
1. `readPhaseLearnings(cwd)` — read accumulated learnings from disk
2. `extractAndAppendLearnings(cwd, phaseId, output, model)` — QUICK model extraction + append
3. Learnings file path (e.g., `.pipeline/phase-learnings.md`)
4. Non-fatal error handling (learnings failure must not block pipeline)

---

## Post-Scaffold Checklist

```text
Core Components (required):
  [ ] Pipeline entry point with classify -> route -> plan -> execute flow
  [ ] Intent classifier with short-circuit and slash command support
  [ ] Routing analyzer (direct / single-skill / multi-skill)
  [ ] Task planner with phase limit and fallback plan
  [ ] Phase evaluator with 4 verdict types
  [ ] Loop guard with per-step and global limits
  [ ] At least one deterministic quality gate (zero-write gate)
  [ ] Context builder with briefs and file manifests
  [ ] Message sink for status injection
  [ ] Typed event bus with all 8 event types
  [ ] Model router with purpose-based resolution

Optional Components:
  [ ] Cross-phase learnings extraction
  [ ] Compare-first enforcement
  [ ] Plan announcement rendering
  [ ] Phase summary rendering
  [ ] Token budget management
  [ ] Cost tracking

Next Steps:
  1. Run /test-llm-pipeline-architect to validate all components
  2. Run /document-llm-pipeline-architect for flow diagrams and API docs
```

---

## Error Handling

**Missing LLM Provider**: If the user does not specify a provider, default to OpenAI-compatible interface and note that any provider speaking the OpenAI chat completions API will work.

**Framework Coupling**: If the user requests a specific framework (LangChain, LangGraph), adapt the patterns to that framework's idioms while preserving all hard-stop rules. The architectural primitives (classify, plan, evaluate, guard) transcend any framework.

**Simple Use Case**: If the user's request is too simple for a full pipeline (e.g., "just call the LLM"), recommend the direct-chat fast-path pattern and offer to scaffold a minimal pipeline that can grow.

## Examples

### Example 1: Full Pipeline
```text
/scaffold-llm-pipeline-architect "
Build a complete AI agent orchestration pipeline in TypeScript.
LLM provider: LiteLLM proxy at localhost:4000.
Need all 12 components including cross-phase learnings.
Streaming via SSE to a React frontend.
"
```

### Example 2: Minimal Pipeline
```text
/scaffold-llm-pipeline-architect "
I need a simple pipeline that classifies user messages and routes
them to either direct chat or a multi-step planner.
Python with OpenAI. No skill system needed.
"
```

### Example 3: Framework Adapter
```text
/scaffold-llm-pipeline-architect "
Add evaluation and loop guards to our existing LangGraph pipeline.
We already have classification and planning.
Need: phase evaluator, loop guard, zero-write gate, event bus.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/llm-pipeline-architect/llm-pipeline-architect-constitution.md` Sections I, II
- **Related**: compare-llm-pipeline-architect, test-llm-pipeline-architect, debug-llm-pipeline-architect
