---
description: Audit and improve an existing AI agent orchestration pipeline by adding missing stages, strengthening evaluation, and improving context handoff
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read refactoring criteria from:
`${ARCHETYPES_BASEDIR}/llm-pipeline-architect/llm-pipeline-architect-constitution.md`

Focus on Section I (Hard-Stop Rules), Section II (Mandatory Patterns), and Section V (Security and Performance Checklist).

### 2. Audit Current Pipeline

Scan the existing pipeline code and identify which components exist:

**Stage Inventory:**

| Stage | Status | File/Location | Notes |
|-------|--------|--------------|-------|
| Intent classification | Present / Missing / Partial | | |
| Routing analysis | Present / Missing / Partial | | |
| Task planning | Present / Missing / Partial | | |
| Compare-first enforcement | Present / Missing / Partial | | |
| Phase execution loop | Present / Missing / Partial | | |
| Phase evaluation | Present / Missing / Partial | | |
| Loop guard | Present / Missing / Partial | | |
| Deterministic quality gate | Present / Missing / Partial | | |
| Context builder | Present / Missing / Partial | | |
| Message sink | Present / Missing / Partial | | |
| Event bus | Present / Missing / Partial | | |
| Model router | Present / Missing / Partial | | |
| Cross-phase learnings | Present / Missing / Partial | | |
| Graceful degradation | Present / Missing / Partial | | |

### 3. Check Hard-Stop Rule Compliance

For each hard-stop rule, determine compliance status:

| Rule | Status | Evidence |
|------|--------|----------|
| 1.1 Classify every message | Compliant / Violation | |
| 1.2 Loop guards on every evaluation | Compliant / Violation | |
| 1.3 Deterministic gate per phase | Compliant / Violation | |
| 1.4 Context handoff, not full replay | Compliant / Violation | |
| 1.5 Graceful degradation | Compliant / Violation | |
| 1.6 No hardcoded model names | Compliant / Violation | |
| 1.7 Streaming events for every stage | Compliant / Violation | |

**Hard-stop violations must be fixed first** — they are non-negotiable.

### 4. Identify Refactoring Priorities

Based on the audit, categorize improvements:

**Priority 1 — Hard-Stop Violations** (must fix):

- Missing classification stage → Add intent classifier module
- No loop guards → Add loop guard with per-step and global limits
- No deterministic gates → Add zero-write gate before LLM evaluation
- Full conversation replay → Replace with context builder using briefs
- No fallback on failure → Add try/catch with onDirect fallback
- Hardcoded model names → Replace with purpose-based resolution
- No events emitted → Add typed event bus with all 8 event types

**Priority 2 — Missing Mandatory Patterns** (should fix):

- Missing evaluation → Add phase evaluator with 4 verdict types
- For-each loop instead of while → Convert to while-loop with dynamic index
- No message sink → Add status injection at key pipeline points
- No file manifest in context → Add writtenFiles tracking to phase results

**Priority 3 — Recommended Improvements** (nice to have):

- No cross-phase learnings → Add QUICK model extraction + disk persistence
- No compare-first → Add deterministic enforcement
- No cost tracking → Add token/cost accumulator
- No plan announcements → Add rendered plan summary injection

### 5. Apply Refactoring (Incremental)

Apply changes in priority order. For each change:

1. **Identify the minimal edit** — Change only what is necessary
2. **Preserve existing behavior** — Do not break working functionality
3. **Add, do not replace** — Layer new stages onto existing flow
4. **Test after each change** — Verify the pipeline still runs

#### 5.1 Add Missing Classification

If the pipeline processes messages without classification:

```typescript
// Before: message goes directly to planning/execution
async function handleMessage(message: string) {
  const plan = await createPlan(message);
  // ...
}

// After: classification gates every message
async function handleMessage(message: string) {
  const classification = await classifyIntent(message, { model: quickModel });
  const routing = analyzeRouting(classification);

  if (routing.route === 'direct') {
    return await onDirect(message);
  }

  const plan = await createTaskPlan(message, { routing });
  // ...
}
```

#### 5.2 Add Loop Guards to Existing Evaluation

If evaluation exists but without guards:

```typescript
// Before: unbounded retry loop
while (evaluation.verdict !== 'proceed') {
  result = await executePhase(phase);
  evaluation = await evaluatePhase(result);
}

// After: guarded evaluation
const loopGuard = createLoopGuard();

if (canEvaluate(loopGuard, phase.id)) {
  recordEvaluation(loopGuard, phase.id);
  const evaluation = await evaluatePhase(result);

  if (evaluation.verdict === 'return-to-step' && canEvaluate(loopGuard, phase.id)) {
    retryFeedback = evaluation.feedback;
    continue; // Retry with feedback
  }
  // Exhausted retries → proceed with partial result
}
```

#### 5.3 Add Deterministic Quality Gate

If LLM evaluation runs without pre-checks:

```typescript
// Insert BEFORE the LLM evaluator call
const writesRequired = phase.purpose !== 'think' && phase.purpose !== 'plan';
const zeroWrites = (execResult.explicitWrites ?? 0) === 0;

if (writesRequired && zeroWrites && canEvaluate(loopGuard, phase.id)) {
  recordEvaluation(loopGuard, phase.id);
  retryFeedback = 'Phase completed with 0 file writes. Use the write tool for every output file.';
  continue;
}

// Existing LLM evaluation runs only after deterministic gate passes
```

#### 5.4 Replace Full Replay with Context Builder

If phases receive full conversation history:

```typescript
// Before: raw output passed to next phase
const context = previousPhaseOutputs.join('\n');

// After: structured briefs + file manifest
const phaseContext = buildPhaseContextPrompt({
  phaseIndex: currentPhaseIndex,
  totalPhases: plan.phases.length,
  currentPhase: phase,
  completedPhases,
  isLastPhase,
  phaseOutputs,     // Record<phaseId, brief ~300 chars>
  phaseLearnings,   // From disk
});
```

#### 5.5 Add Graceful Degradation

If pipeline errors are unhandled:

```typescript
// Wrap the entire pipeline call
try {
  return await runPipeline(message, config);
} catch (err) {
  console.error('[pipeline] Failed, falling back to direct:', err);
  await bus.emit('pipeline:error', { runId, error: err.message });
  await onDirect(message); // User always gets a response
}
```

#### 5.6 Replace Hardcoded Models

If model names appear in pipeline code:

```typescript
// Before: hardcoded
const model = new OpenAI({ model: 'gpt-4o-mini' });

// After: purpose-based resolution
const model = resolveModelForPurpose('quick', envConfig);
```

#### 5.7 Add Event Bus

If pipeline stages emit no events:

```typescript
// Add emit calls at each stage
await bus.emit('pipeline:start', { runId, sessionId, message });
await bus.emit('pipeline:classified', { runId, classification });
await bus.emit('pipeline:planned', { runId, plan });
// ... per phase: phase-start, evaluation, phase-end
await bus.emit('pipeline:end', { runId, sessionId });
```

### 6. Post-Refactoring Validation

After all changes, run the full checklist from Constitution Section V:

```text
Post-Refactoring Validation:
  [ ] All 7 hard-stop rules satisfied
  [ ] All 10 mandatory patterns present (or justified omission)
  [ ] Pipeline runs end-to-end without errors
  [ ] Graceful degradation tested (simulate LLM timeout)
  [ ] Loop guard tested (simulate always-retry evaluator)
  [ ] Context size stays bounded across 4+ phases
  [ ] Events emitted at every stage
  [ ] No hardcoded model names in pipeline code
```

### 7. Generate Refactoring Summary

```text
## Pipeline Refactoring Summary

### Changes Applied

| Priority | Change | Files Modified |
|----------|--------|---------------|
| P1 | {change_description} | {files} |
| P2 | {change_description} | {files} |
| P3 | {change_description} | {files} |

### Hard-Stop Compliance (After)

| Rule | Before | After |
|------|--------|-------|
| 1.1 Classify every message | {status} | Compliant |
| 1.2 Loop guards | {status} | Compliant |
| ... | ... | ... |

### Remaining Recommendations

{List of recommended patterns not yet implemented}
```

---

## Error Handling

**No Pipeline Code Provided**: Ask the user to share the pipeline entry point, evaluation loop, and context builder modules.

**Framework-Specific Pipeline**: Adapt refactoring patterns to framework idioms (LangChain chains, LangGraph nodes, CrewAI agents) while preserving hard-stop rule compliance.

**Minimal Pipeline**: If the pipeline is very simple (no evaluation, no phases), recommend starting with `/scaffold-llm-pipeline-architect` to generate a complete baseline, then migrating existing logic into the scaffold.

## Examples

### Example 1: Add Guards to Existing Pipeline
```text
/refactor-llm-pipeline-architect "
Our pipeline has evaluation but no loop guards. The evaluator
sometimes gets stuck returning 'retry' forever. Add loop guards
with max 3 retries per step and 1 replan per run.
"
```

### Example 2: Fix Context Exhaustion
```text
/refactor-llm-pipeline-architect "
Pipeline works for 2 phases but degrades at phase 4+. We pass
full conversation history to each sub-agent. Refactor to use
structured context handoff with briefs and file manifests.
"
```

### Example 3: Full Compliance Audit
```text
/refactor-llm-pipeline-architect "
Audit our existing agent pipeline against the constitution.
Pipeline code is in src/orchestrator/. Identify all violations
and apply fixes in priority order.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/llm-pipeline-architect/llm-pipeline-architect-constitution.md` Sections I, II, V
- **Related**: scaffold-llm-pipeline-architect, debug-llm-pipeline-architect, test-llm-pipeline-architect
