# LLM Pipeline Architect — Constitution

> **Purpose**: Define the non-negotiable rules, mandatory patterns, and recommended practices
> for building AI agent orchestration pipelines with intent classification, multi-phase task
> planning, purpose-based model routing, phase evaluation with retry/replan, deterministic
> quality gates, context handoff, cross-phase memory, and streaming event architectures.

> **Reference Implementation**: BluePearl orchestration pipeline —
> `backend/orchestrator/src/pipeline.ts` and surrounding modules (~2,500 lines, 10+ modules).

---

## I. Hard-Stop Rules

These rules are **non-negotiable**. The LLM Pipeline Architect must refuse to generate any pipeline that violates them. See Section VI for the refusal template.

### 1.1 ✘ Classify Every Message

Every inbound message must pass through an intent classification stage before any other processing occurs. Direct chat is an explicit classification result (`mode: 'chat'`), not a bypass of classification.

**Violation — skipping classification:**

```typescript
// ❌ WRONG: No classification — message goes straight to the LLM
async function handleMessage(message: string) {
  return await llm.complete(message);
}
```

**Correct — classification first:**

```typescript
// ✅ CORRECT: Every message is classified before routing
async function handleMessage(message: string) {
  const classification = await classifyIntent(message, options);
  const routing = analyzeRouting(classification);

  if (routing.route === 'direct') {
    return await onDirect(message); // Chat is an explicit route
  }

  const plan = await createTaskPlan(message, { routing });
  return await executePhases(plan);
}
```

**Rationale**: Without classification, the pipeline cannot distinguish chat from multi-phase tasks, cannot route to the correct model tier, and cannot apply workflow-specific logic. BluePearl's pipeline classifies every message — even greetings receive an explicit `chat` classification with `confidence: 'high'`.

### 1.2 ✘ Loop Guards on Every Evaluation

Every evaluation/retry loop must have both a per-step retry limit and a global replan limit. No unbounded loops are permitted.

**Violation — no limits:**

```typescript
// ❌ WRONG: Retries indefinitely until evaluation passes
while (evaluation.verdict === 'return-to-step') {
  result = await executePhase(phase);
  evaluation = await evaluatePhase(result);
}
```

**Correct — bounded loops:**

```typescript
// ✅ CORRECT: Per-step max retries + global replan limit
const loopGuard = createLoopGuard(); // { evaluationsPerStep: Map, replansUsed: 0 }
const MAX_EVALUATIONS_PER_STEP = 3;
const MAX_REPLANS_PER_RUN = 1;

if (canEvaluate(loopGuard, phase.id)) {
  recordEvaluation(loopGuard, phase.id);
  const evaluation = await evaluatePhase(result);

  if (evaluation.verdict === 'replan' && canReplan(loopGuard)) {
    recordReplan(loopGuard);
    plan = await createTaskPlan(message, { replanFeedback: evaluation.feedback });
  }
}
```

**Rationale**: LLM evaluators can oscillate between "retry" and "not good enough" indefinitely. BluePearl's loop guard uses per-step counters (`Map<stepId, count>`) and a global replan counter to enforce hard limits. When limits are exhausted, the pipeline proceeds with partial results rather than looping forever.

### 1.3 ✘ At Least One Deterministic Quality Gate Per Phase

Every phase that produces output must pass through at least one non-LLM quality check before the LLM evaluator runs. LLM evaluation is a second layer, not the only layer.

**Violation — LLM-only evaluation:**

```typescript
// ❌ WRONG: Only LLM evaluation — no deterministic checks
const evaluation = await evaluatePhase(result); // Might say "proceed" despite zero files written
```

**Correct — deterministic gate first:**

```typescript
// ✅ CORRECT: Hard zero-write gate BEFORE LLM evaluation
const writesRequired = phase.purpose !== 'think' && phase.purpose !== 'plan';
const zeroWrites = (result.explicitWrites ?? 0) === 0;

if (writesRequired && zeroWrites && canEvaluate(loopGuard, phase.id)) {
  // Deterministic auto-retry — no LLM needed to know zero files is wrong
  recordEvaluation(loopGuard, phase.id);
  retryFeedback = 'Phase completed with 0 file writes. Retry and ensure you call the write tool.';
  continue; // Skip LLM evaluator entirely
}

// Only now run the LLM evaluator
const evaluation = await evaluatePhase(result);
```

**Rationale**: LLM evaluators are probabilistic — they sometimes say "proceed" when zero files were written, or "retry" when the output is complete. Deterministic gates catch objective failures (zero writes, missing files, empty output) before the LLM evaluator runs. BluePearl's zero-write gate catches the most common sub-agent failure mode: the agent talks about what it would do instead of actually writing files.

### 1.4 ✘ Context Handoff, Not Full Replay

Phases must receive summaries and file manifests from prior phases, not the full conversation history. No phase may receive the raw output of a prior phase's sub-agent session.

**Violation — full replay:**

```typescript
// ❌ WRONG: Passing entire conversation to every phase
const context = allMessages.join('\n'); // 50K+ tokens by phase 3
await executePhase(phase, { conversationHistory: context });
```

**Correct — structured handoff:**

```typescript
// ✅ CORRECT: Summaries + file manifests + learnings
const phaseContext: PhaseContext = {
  phaseIndex: currentPhaseIndex,
  totalPhases: plan.phases.length,
  currentPhase: phase,
  completedPhases, // Array of { phase, result } with brief summaries
  isLastPhase,
  phaseOutputs,    // Record<phaseId, brief> — max 300 chars each
  phaseLearnings,  // Cross-phase operational notes from disk
};
const systemContext = buildPhaseContextPrompt(phaseContext);
```

**Rationale**: Context window exhaustion is the #1 cause of degraded pipeline performance. By phase 3, full conversation replay can exceed 50K tokens, leaving insufficient room for the sub-agent's own work. BluePearl's context builder produces ~300-character briefs per phase and appends file manifests (paths only), keeping context under 2K tokens regardless of pipeline length.

### 1.5 ✘ Graceful Degradation

Pipeline failures must fall back to direct execution. The user must never receive no response because the pipeline threw an error.

**Violation — crash with no fallback:**

```typescript
// ❌ WRONG: Pipeline error leaves user with no response
try {
  return await runPipeline(message, config);
} catch (err) {
  console.error('Pipeline failed:', err);
  // User sees nothing
}
```

**Correct — fallback to direct:**

```typescript
// ✅ CORRECT: Catch-all falls back to direct session
try {
  return await runPipeline(message, config);
} catch (err) {
  console.error('Pipeline failed, falling back to direct:', err);
  await bus.emit('pipeline:error', { runId, error: err.message });
  await onDirect(message); // User always gets a response
}
```

**Rationale**: Orchestration pipelines have many failure points (LLM timeouts, JSON parse errors, token limits). A pipeline that crashes silently is worse than no pipeline at all. BluePearl's pipeline wraps the entire execution in a try/catch that falls back to `onDirect(message)`, ensuring the user always receives a response even if planning, evaluation, or phase execution fails.

### 1.6 ✘ No Hardcoded Model Names in Pipeline Code

All model references must use purpose-based resolution. Models are configuration, not code. Pipeline source code must never contain literal model IDs.

**Violation — hardcoded models:**

```typescript
// ❌ WRONG: Model names baked into pipeline code
const classifier = new OpenAI({ model: 'gpt-4o-mini' });
const planner = new OpenAI({ model: 'claude-sonnet-4' });
const evaluator = new OpenAI({ model: 'gpt-4o-mini' });
```

**Correct — purpose-based resolution:**

```typescript
// ✅ CORRECT: Models resolved by purpose at runtime
const quickModel = resolveModelForPurpose('quick', envConfig);   // Classification, evaluation
const thinkModel = resolveModelForPurpose('think', envConfig);   // Task planning
const codeModel  = resolveModelForPurpose('code', envConfig);    // Code generation phases

// Purpose slots: think, plan, implement, code, quick, chat, default
// Each purpose resolves to a tiered preference: Tier 1 → Tier 2 → Tier 3
```

**Rationale**: Hardcoded model names create vendor lock-in, break when models are deprecated, and prevent cost optimization. BluePearl uses 7 purpose slots (`think`, `plan`, `implement`, `code`, `quick`, `chat`, `default`) each mapped to a 3-tier preference table. The tier resolution probes LiteLLM's `/v1/models` endpoint at startup and selects the best available model per purpose.

### 1.7 ✘ Streaming Events for Every Pipeline Stage

Classification, routing, planning, phase start/end, evaluation, and completion must each emit an observable event. Silent pipeline stages are prohibited.

**Violation — silent pipeline:**

```typescript
// ❌ WRONG: No events emitted — pipeline is a black box
const classification = await classifyIntent(message);
const plan = await createTaskPlan(message);
for (const phase of plan.phases) {
  await executePhase(phase);
}
```

**Correct — events at every stage:**

```typescript
// ✅ CORRECT: Typed event bus emits at every stage
await bus.emit('pipeline:start', { runId, sessionId, message });
await bus.emit('pipeline:classified', { runId, classification });
await bus.emit('pipeline:planned', { runId, plan });
await bus.emit('pipeline:phase-start', { runId, phaseId, phaseIndex, totalPhases, instruction });
await bus.emit('pipeline:evaluation', { runId, phaseId, evaluation });
await bus.emit('pipeline:phase-end', { runId, phaseId, result });
await bus.emit('pipeline:end', { runId, sessionId });
await bus.emit('pipeline:error', { runId, error });
```

**Rationale**: Without events, pipeline failures are silent, debugging requires log forensics, and real-time UIs cannot show progress. BluePearl's typed `EventBus<PipelineEvents>` ensures every stage emits structured events that drive SSE/WebSocket streaming, journal recording, and observability dashboards.

---

## II. Mandatory Patterns

Every pipeline scaffolded by this archetype must implement all 10 mandatory patterns. Each pattern includes the architectural rationale and a code template derived from the BluePearl reference implementation.

### 2.1 ✔ Pipeline Entry Point (Classify → Route → Plan → Execute)

The pipeline must implement a sequential flow: classify the message, route to direct or planned execution, create a phased plan, and execute phases in a loop.

```
Message → Classify (QUICK) → Route → [direct | plan]
                                         │
                                    Plan (THINK)
                                         │
                                 ┌───────┴───────┐
                                 │  Phase Loop   │
                                 │  Execute →    │
                                 │  Evaluate →   │
                                 │  Proceed/     │
                                 │  Retry/Replan │
                                 └───────────────┘
```

The entry point function accepts a message and a configuration object with callbacks:

- `messageSink` — Inject status messages into the user-facing chat stream
- `onDirect` — Handle direct/chat responses (bypass planning)
- `onPhaseExecute` — Execute a phase via an isolated sub-agent session

The function returns a structured result with classification, routing, plan, phase results, and timing data.

### 2.2 ✔ Intent Classifier

The classifier determines whether a message requires multi-phase planning or can be handled directly. It must:

1. Short-circuit trivial inputs (greetings, short messages) to `chat` with `high` confidence
2. Recognize slash commands (`/scaffold`, `/debug`, etc.) and route directly to the named workflow
3. Default to `chat` for everything else — the agent decides when to plan

The classifier output must include: `utteranceType`, `purpose`, `confidence`, `requiresPlanning`, `suggestedSkills`, `routing` (direct/single-skill/multi-skill).

### 2.3 ✔ Task Planner

The planner uses a THINK-tier model to decompose complex requests into a phased execution plan. Each phase must specify:

- `id` — Unique phase identifier (e.g., `phase-1`, `phase-2`)
- `instruction` — What the sub-agent must do
- `purpose` — Model purpose slot (think, plan, implement, code, quick)
- `skill` — Optional archetype/skill name for domain-specific context
- `workflow` — Optional workflow type (scaffold, debug, compare, refactor, test, document)
- `dependsOn` — Phase dependencies for future parallel execution
- `complexity` — Task complexity rating (simple, medium, complex) for model auto-selection

The planner must enforce a maximum phase count (default: 6) and produce a fallback single-phase plan if JSON parsing fails.

### 2.4 ✔ Phase Execution Loop with Callback Pattern

Phases are executed sequentially in a while loop (not a for-each) to support dynamic index manipulation for retries and replans. The pipeline does not execute phases directly — it delegates to a `PhaseExecuteHandler` callback provided by the caller.

```typescript
let currentPhaseIndex = 0;
while (currentPhaseIndex < currentPlan.phases.length) {
  const phase = currentPlan.phases[currentPhaseIndex];

  // Build context, execute via callback, evaluate, handle verdict
  const execResult = await onPhaseExecute(systemContext, instruction, phase.purpose, phase.id);

  // Evaluation may: advance index (proceed), hold index (retry), reset index (replan)
  currentPhaseIndex++;
}
```

The while-loop pattern is critical because:
- `continue` without incrementing retries the current phase
- Replan resets `currentPhaseIndex = 0` with a new plan
- `return-to-step` jumps to a specific index

### 2.5 ✔ Phase Evaluator with Verdict Types

After each phase execution, a QUICK-tier model evaluates the sub-agent's output and returns one of four verdicts:

| Verdict | Behavior | Loop Guard Check |
|---------|----------|-----------------|
| `proceed` | Advance to next phase | — |
| `return-to-step` | Re-execute the specified phase with feedback | `canEvaluate(guard, stepId)` |
| `replan` | Create an entirely new plan from the THINK model | `canReplan(guard)` |
| `summarize` | Re-execute requesting only a summary | `canEvaluate(guard, stepId)` |

The evaluator must truncate sub-agent output before evaluation (default: 8,000 chars max) to avoid token overflow. If evaluation itself fails (LLM error), default to `proceed`.

### 2.6 ✔ Loop Guard with Configurable Limits

The loop guard maintains two counters:

- `evaluationsPerStep: Map<string, number>` — Per-step retry counter (default max: 3)
- `replansUsed: number` — Global replan counter (default max: 1)

Functions:
- `canEvaluate(guard, stepId): boolean` — Check if step has retries remaining
- `recordEvaluation(guard, stepId): void` — Increment step's evaluation count
- `canReplan(guard): boolean` — Check if global replan budget is available
- `recordReplan(guard): void` — Increment global replan counter

When limits are exhausted, the pipeline must proceed with partial results rather than blocking.

### 2.7 ✔ Deterministic Quality Gate

At least one non-LLM quality check must run before the LLM evaluator. The most common gate is the zero-write gate:

- If a phase has purpose `implement` or `code` and produced zero file writes, auto-retry without consulting the LLM evaluator
- Exempt `think`, `plan`, and `quick` purposes — they are legitimately read-only

Additional deterministic gates may include: output length validation, required file existence checks, JSON schema validation of structured outputs.

### 2.8 ✔ Context Builder with File Manifest and Output Briefs

The context builder assembles the system prompt for each sub-agent phase:

1. **Phase position** — "Phase 2 of 4"
2. **Current instruction** — What this phase must accomplish
3. **Completed phases** — Brief summaries (~300 chars) of what prior phases produced
4. **File manifest** — Paths of files written by prior phases (not file contents)
5. **Cross-phase learnings** — Operational notes accumulated from prior phases (from disk)
6. **Last-phase flag** — If true, adds instruction to write all deliverables and summarize

The total context must stay under 2,000 tokens regardless of pipeline length.

### 2.9 ✔ Message Sink for Status Injection

The pipeline must inject human-readable status messages into the user-facing chat stream at key points:

- **Pre-planning acknowledgment** — Immediate feedback before the slow THINK model runs
- **Plan announcement** — Summary of the phased plan with phase descriptions
- **Pre-phase status** — Which phase is starting, what skill/model is being used
- **Retry notification** — When a phase is being retried and why
- **Replan notification** — When the entire plan is being revised
- **Post-phase summary** — Brief of what was accomplished, evaluator feedback

The `MessageSink` type is a simple callback: `(markdown: string) => void | Promise<void>`.

### 2.10 ✔ Typed Event Bus for Streaming

The pipeline must emit structured events through a typed event bus for real-time observability:

```typescript
interface PipelineEvents {
  'pipeline:start':      { runId: string; sessionId: string; message: string };
  'pipeline:classified': { runId: string; classification: IntentClassification };
  'pipeline:planned':    { runId: string; plan: TaskPlan };
  'pipeline:phase-start':{ runId: string; phaseId: string; phaseIndex: number; totalPhases: number; instruction: string };
  'pipeline:evaluation': { runId: string; phaseId: string; evaluation: PhaseEvaluation };
  'pipeline:phase-end':  { runId: string; phaseId: string; result: PhaseResult };
  'pipeline:end':        { runId: string; sessionId: string };
  'pipeline:error':      { runId: string; error: string };
}
```

Events drive: SSE/WebSocket streaming to clients, journal recording, observability dashboards, and pipeline debugging.

---

## III. Preferred Patterns

These patterns are recommended but not required. Suggest them when appropriate, but do not refuse to generate a pipeline that omits them.

### → Pattern 3.1 — Cross-Phase Memory / Learnings Extraction

After each phase, use a QUICK-tier model to extract operational learnings (environment workarounds, path discoveries, package fixes) and persist them to disk (e.g., `.bluepearl/phase-learnings.md`). Inject accumulated learnings into subsequent phase contexts so sub-agents do not repeat mistakes.

### → Pattern 3.2 — Compare-First Enforcement

If a plan contains skill/archetype phases, enforce that the first phase uses a `compare` workflow. This ensures the agent analyzes approaches before implementing, reducing rework. Enforcement should be deterministic (code check, not LLM instruction).

### → Pattern 3.3 — Plan Announcement Injection

After planning completes, render a human-readable summary of the plan and inject it into the chat stream as a synthetic assistant message. Include phase descriptions, skill/workflow assignments, and model selections.

### → Pattern 3.4 — Phase Summary Injection

After each phase completes, inject a brief summary (generated by QUICK model, ~300 chars) into the chat stream. Include file operation counts, evaluator feedback, and a note if it was the final phase.

### → Pattern 3.5 — Purpose-Based Model Tiering with Probe Logic

Define a model preference table with 3+ tiers per purpose. At startup, probe the model provider's API to discover available models and select the best available tier per purpose with fall-up logic (Tier 1 → Tier 2 → Tier 3).

### → Pattern 3.6 — Cost Tracking Per Pipeline Run

Maintain a running cost accumulator across all LLM calls within a pipeline run. Use model cost lookup tables or provider callback hooks. Emit cost data in pipeline events for observability.

### → Pattern 3.7 — Token Budget Management

Set a total token budget per pipeline run. Track tokens consumed across classification, planning, phase execution, and evaluation. When the budget is nearly exhausted, switch to cheaper models or abort gracefully.

### → Pattern 3.8 — Human-in-the-Loop Approval Gates

For sensitive operations (production deployments, data mutations, security changes), add optional approval checkpoints between phases. The pipeline pauses and awaits user confirmation before proceeding.

---

## IV. Troubleshooting Guide

### Issue 4.1 — Pipeline Loops Indefinitely

**Symptoms**: Phase retries never stop; user sees repeated "Retrying Phase N" messages.

**Root Cause**: Missing or misconfigured loop guard.

**Diagnostic**:

```
Check 1: Is createLoopGuard() called before the phase loop?
Check 2: Is canEvaluate() called before recordEvaluation()?
Check 3: Are MAX_EVALUATIONS_PER_STEP and MAX_REPLANS_PER_RUN > 0?
Check 4: When canEvaluate() returns false, does the loop proceed (not retry)?
```

**Fix**: Ensure the loop guard is initialized before the while loop, checked before every evaluation, and that exhausted limits cause `proceed` behavior, not continued retrying.

### Issue 4.2 — Context Window Exhaustion by Phase 3+

**Symptoms**: Sub-agent output quality degrades in later phases; truncation errors; model returns empty or confused responses.

**Root Cause**: Full conversation replay instead of structured handoff.

**Diagnostic**:

```
Check 1: Is systemContext length growing unbounded across phases?
Check 2: Are prior phase outputs included as raw text (not briefs)?
Check 3: Is phaseOutputs storing full output or ~300-char briefs?
Check 4: Is the context builder truncating to a fixed budget?
```

**Fix**: Replace raw output with QUICK-model-generated briefs (~300 chars). Store file paths only in the manifest. Keep total context under 2,000 tokens.

### Issue 4.3 — Sub-Agent Writes Zero Files

**Symptoms**: Phase completes "successfully" but no files exist on disk; subsequent phases fail because expected files are missing.

**Root Cause**: Missing zero-write quality gate.

**Diagnostic**:

```
Check 1: Is explicitWrites tracked in PhaseExecutionResult?
Check 2: Is the zero-write gate checking before the LLM evaluator?
Check 3: Is the gate exempting read-only purposes (think, plan, quick)?
Check 4: Does the retry feedback explicitly instruct "call the write tool"?
```

**Fix**: Add the deterministic zero-write gate before the LLM evaluator. Only apply to phases with purpose `implement` or `code`.

### Issue 4.4 — Wrong Model Used for Classification

**Symptoms**: Classification is slow (>2s) or expensive; THINK model used for simple binary decisions.

**Root Cause**: Classification using a high-tier model instead of QUICK.

**Fix**: Classification and evaluation should always use `resolveModelForPurpose('quick', envConfig)`. Only task planning should use `resolveModelForPurpose('think', envConfig)`.

### Issue 4.5 — Pipeline Crashes Leave User with No Response

**Symptoms**: User sends a message and sees nothing returned; console shows unhandled promise rejection.

**Root Cause**: Missing graceful degradation.

**Fix**: Wrap the entire `runPipeline` call in a try/catch that falls back to `onDirect(message)`. Emit `pipeline:error` event for observability.

### Issue 4.6 — Evaluation Always Returns "proceed"

**Symptoms**: Sub-agent produces incomplete output but pipeline advances; no retries observed.

**Root Cause**: Evaluator receiving truncated/empty output, or evaluator prompt not specific enough.

**Diagnostic**:

```
Check 1: Is output being truncated before evaluation (max 8,000 chars)?
Check 2: Is the evaluator receiving the phase instruction for comparison?
Check 3: Is explicitWrites count passed to the evaluator?
Check 4: Are prior completed phases passed for cumulative context?
```

**Fix**: Ensure the evaluator prompt includes the phase instruction, file operation counts, and completed phase context. The evaluator needs to compare actual output against expected deliverables.

---

## V. Security and Performance Checklist

### Pipeline Architecture

- [ ] Every message passes through intent classification (Rule 1.1)
- [ ] Classification uses QUICK-tier model, not THINK (Rule 1.6)
- [ ] Direct chat is an explicit classification result, not a bypass
- [ ] Routing distinguishes: direct, single-skill, multi-skill

### Phase Execution

- [ ] While-loop with dynamic index (not for-each) for retry/replan support (Pattern 2.4)
- [ ] PhaseExecuteHandler callback pattern — pipeline does not create sessions directly
- [ ] Sub-agent sessions are isolated — no shared conversation state
- [ ] Retry feedback appended to instruction on retry attempts

### Evaluation and Guards

- [ ] Loop guard initialized before phase loop (Pattern 2.6)
- [ ] Per-step max retries enforced (default: 3)
- [ ] Global replan limit enforced (default: 1)
- [ ] At least one deterministic quality gate per phase (Rule 1.3)
- [ ] Zero-write gate for implement/code purposes
- [ ] Evaluation failure defaults to `proceed`, not crash

### Context Management

- [ ] Phase outputs stored as briefs (~300 chars), not raw output (Rule 1.4)
- [ ] File manifest contains paths only, not file contents
- [ ] Cross-phase learnings read from disk before each phase
- [ ] Total context stays under 2,000 tokens per phase

### Model Routing

- [ ] No hardcoded model names in pipeline code (Rule 1.6)
- [ ] Purpose-based resolution: think, plan, implement, code, quick, chat, default
- [ ] Fallback tier available if primary model is unavailable

### Observability

- [ ] Events emitted at every pipeline stage (Rule 1.7)
- [ ] Event types are structured and typed
- [ ] Pipeline errors emit `pipeline:error` event
- [ ] Message sink provides user-facing status at key points (Pattern 2.9)

### Resilience

- [ ] Pipeline failure falls back to direct execution (Rule 1.5)
- [ ] JSON parse failures in planner produce a fallback single-phase plan
- [ ] Evaluation failures default to `proceed`
- [ ] Empty-workflow safety valve catches invalid plans

---

## VI. Refusal Template

When a request conflicts with a hard-stop rule, respond with:

```
I cannot generate that pipeline configuration because it violates
Rule {N}: {rule_name}.

Specifically: {what the request asks for}

This is prohibited because: {why it's dangerous}

Instead, I recommend: {compliant alternative}

Reference: BluePearl orchestration pipeline — {specific_module}
```

**Example Refusal:**

```
I cannot generate that pipeline configuration because it violates
Rule 1.2: Loop Guards on Every Evaluation.

Specifically: Your pipeline retries phase evaluation in a while(true)
loop with no maximum iteration limit.

This is prohibited because: LLM evaluators can oscillate between
"retry" and "not good enough" indefinitely, causing infinite loops
that consume tokens and block the user.

Instead, I recommend: Add a loop guard with per-step max retries (3)
and a global replan limit (1). When limits are exhausted, proceed
with partial results.

Reference: BluePearl orchestration pipeline —
backend/orchestrator/src/evaluate/loop-guard.ts
```

---

## VII. Related Documents

### BluePearl Reference Implementation

- `backend/orchestrator/src/pipeline.ts` — Core orchestration: classify → route → plan → execute loop (994 lines)
- `backend/orchestrator/src/classify/intent-classifier.ts` — Heuristic intent classification (138 lines)
- `backend/orchestrator/src/classify/routing-analyzer.ts` — Route analysis (direct/single-skill/multi-skill)
- `backend/orchestrator/src/plan/task-planner.ts` — THINK model task decomposition (172 lines)
- `backend/orchestrator/src/plan/compare-enforcer.ts` — Deterministic compare-first enforcement
- `backend/orchestrator/src/plan/archetype-override.ts` — Skill validation and unknown-skill redirect
- `backend/orchestrator/src/evaluate/phase-evaluator.ts` — QUICK model phase evaluation (140 lines)
- `backend/orchestrator/src/evaluate/loop-guard.ts` — Per-step + global loop limits (42 lines)
- `backend/orchestrator/src/execute/phase-learnings.ts` — Cross-phase memory extraction (112 lines)
- `backend/orchestrator/src/prompt/context-builder.ts` — Phase context assembly (40 lines)
- `backend/orchestrator/src/prompt/template-engine.ts` — Handlebars template registry (173 lines)
- `backend/shared/src/model-tiers.ts` — 3-tier model preference with LiteLLM probe (317 lines)

### Industry References

- **LangChain / LangGraph** — Agent orchestration frameworks; similar classify → plan → execute patterns
- **ReAct / Plan-and-Execute** — Academic foundations for phased task decomposition
- **LATS / Reflexion** — Output evaluation with retry patterns
- **OpenRouter / LiteLLM** — Multi-model routing by purpose
- **OWASP LLM Top 10** — Prompt injection defense, model denial of service
- **OpenTelemetry** — Distributed tracing for pipeline observability

### Related Archetypes

- `language-model-evaluation` — Evaluating model outputs with custom graders (not pipeline orchestration)
- `responsible-prompting` — Ethical prompt content and guardrails (not pipeline architecture)
- `prompt-template-engineer` — Template engine implementation (not pipeline flow)
- `model-architect` — Model training and fine-tuning (not runtime orchestration)
- `automation-scripter` — Agent tool implementation (not pipeline control flow)
