---
description: Debug AI agent orchestration pipeline failures including infinite loops, context exhaustion, wrong model routing, missing events, and evaluation issues
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read diagnostic context from:
`${ARCHETYPES_BASEDIR}/llm-pipeline-architect/llm-pipeline-architect-constitution.md`

Focus on Section IV (Troubleshooting Guide) and Section I (Hard-Stop Rules).

### 2. Classify the Failure

Determine the failure category from $ARGUMENTS:

| Category | Symptoms | Priority |
|----------|----------|----------|
| **Infinite loop** | Pipeline never completes; repeated retry messages; token budget exhausted | Critical |
| **Silent failure** | User sends message, no response returned; no error in logs | Critical |
| **Context exhaustion** | Output quality degrades in later phases; truncation errors; confused responses | High |
| **Wrong model routing** | Classification slow/expensive; THINK model used for evaluation; wrong tier | High |
| **Zero-write phases** | Phases complete "successfully" but no files on disk; downstream failures | High |
| **Evaluation always-proceed** | Sub-agent produces poor output but pipeline advances; no retries | Medium |
| **Missing events** | Pipeline runs but no streaming updates; UI shows no progress | Medium |
| **Plan parse failure** | Planner produces invalid JSON; always falls back to single-phase plan | Medium |
| **Skill routing failure** | Archetype not found; skill prompt empty; wrong workflow loaded | Low |

### 3. Diagnostic Procedures

#### 3.1 Infinite Loop Diagnosis

**Symptoms**: Pipeline never completes; "Retrying Phase N" repeated endlessly; token costs spike.

**Check loop guard initialization:**

```typescript
// Verify loop guard is created BEFORE the while loop
const loopGuard = createLoopGuard();
let currentPhaseIndex = 0;

while (currentPhaseIndex < plan.phases.length) {
  // Is canEvaluate() called before every evaluation?
  if (canEvaluate(loopGuard, phase.id)) {
    recordEvaluation(loopGuard, phase.id);
    // ...
  }
  // When canEvaluate returns false, does the loop PROCEED (not retry)?
}
```

**Check for missing index increment:**

```typescript
// Common bug: continue without incrementing causes infinite retry
if (evaluation.verdict === 'return-to-step') {
  retryFeedback = evaluation.feedback;
  continue; // ✅ Correct IF canEvaluate will eventually return false
}

// After evaluation handling, is currentPhaseIndex incremented?
currentPhaseIndex++; // Must exist outside all continue paths
```

**Check replan limit:**

```typescript
// Is canReplan checked before creating a new plan?
if (evaluation.verdict === 'replan' && canReplan(loopGuard)) {
  recordReplan(loopGuard);
  // Replan resets currentPhaseIndex = 0, so guard is the only protection
}
```

**Fix checklist:**
- [ ] `createLoopGuard()` called before phase loop
- [ ] `canEvaluate()` checked before `recordEvaluation()`
- [ ] `canReplan()` checked before `recordReplan()`
- [ ] `MAX_EVALUATIONS_PER_STEP` and `MAX_REPLANS_PER_RUN` are positive integers
- [ ] When limits exhausted, verdict falls through to `proceed`
- [ ] `currentPhaseIndex++` is reached on non-retry paths

#### 3.2 Silent Failure Diagnosis

**Symptoms**: User sends message, sees no response; no error in console; pipeline appears to start but never completes.

**Check graceful degradation:**

```typescript
// Is the entire pipeline wrapped in try/catch with onDirect fallback?
try {
  return await runPipeline(message, config);
} catch (err) {
  // Does this catch block exist?
  // Does it call onDirect(message)?
  // Does it emit pipeline:error event?
  await bus.emit('pipeline:error', { runId, error: err.message });
  await onDirect(message);
}
```

**Check callback wiring:**

```typescript
// Are all three callbacks provided in PipelineConfig?
const config: PipelineConfig = {
  messageSink: (md) => { /* Is this function defined? */ },
  onDirect: (msg) => { /* Does this reach the user? */ },
  onPhaseExecute: async (ctx, instr, purpose, phaseId) => {
    // Does this actually execute and return a result?
  },
};
```

**Check classification blocking:**

```typescript
// Is classifyIntent awaiting an LLM call that times out?
// Check if the QUICK model is reachable
const quickModel = resolveModelForPurpose('quick', envConfig);
// Is the model endpoint responding? Is the API key valid?
```

**Fix checklist:**
- [ ] Pipeline has try/catch with `onDirect` fallback (Rule 1.5)
- [ ] `messageSink`, `onDirect`, `onPhaseExecute` all provided
- [ ] Classification model is reachable (check API key, endpoint)
- [ ] `pipeline:error` event is emitted on failure
- [ ] No unhandled promise rejections in async callbacks

#### 3.3 Context Exhaustion Diagnosis

**Symptoms**: Phase 3+ output quality drops; model returns confused or truncated responses; token limit errors.

**Measure context growth:**

```typescript
// Log context size at each phase
console.log(`Phase ${phase.id} context: ${systemContext.length} chars`);

// Is it growing linearly with phase count?
// Phase 1: ~500 chars (good)
// Phase 2: ~800 chars (good)
// Phase 3: ~15000 chars (BAD — full replay detected)
```

**Check phase output storage:**

```typescript
// Are phaseOutputs storing raw output or briefs?
phaseOutputs[phase.id] = execResult.output;      // ❌ Raw (could be 10K+)
phaseOutputs[phase.id] = phaseBrief;              // ✅ Brief (~300 chars)
```

**Check context builder:**

```typescript
// Is buildPhaseContextPrompt using briefs or raw output?
// Does it include file contents (bad) or file paths only (good)?
```

**Fix checklist:**
- [ ] Phase outputs stored as briefs (~300 chars), not raw output (Rule 1.4)
- [ ] File manifest contains paths only, not file contents
- [ ] Context builder has a token budget cap
- [ ] Cross-phase learnings are brief and instruction-oriented

#### 3.4 Wrong Model Routing Diagnosis

**Symptoms**: Classification takes >2 seconds; evaluation is expensive; planning uses cheap model.

**Check purpose assignments:**

```typescript
// Classification should use QUICK, not THINK
const quickModel = resolveModelForPurpose('quick', envConfig);  // ✅
const thinkModel = resolveModelForPurpose('think', envConfig);  // ❌ for classification

// Planning should use THINK, not QUICK
const plan = await createTaskPlan(message, { model: thinkModel }); // ✅

// Evaluation should use QUICK, not IMPLEMENT
const eval = await evaluatePhase({ model: quickModel });           // ✅
```

**Check for hardcoded model names:**

```typescript
// Search codebase for literal model IDs (Rule 1.6 violation)
// grep -rn "gpt-4\|claude\|gemini\|llama" src/
// Any matches in pipeline code = violation
```

**Fix checklist:**
- [ ] Classification uses `quick` purpose
- [ ] Planning uses `think` purpose
- [ ] Evaluation uses `quick` purpose
- [ ] Phase execution uses purpose from plan (implement, code, etc.)
- [ ] No hardcoded model names in pipeline code (Rule 1.6)

#### 3.5 Zero-Write Phase Diagnosis

**Symptoms**: Phase reports success but `explicitWrites === 0`; downstream phases can't find expected files.

**Check quality gate presence:**

```typescript
// Is the zero-write gate implemented before LLM evaluation?
const writesRequired = phase.purpose !== 'think' && phase.purpose !== 'plan';
const zeroWrites = (execResult.explicitWrites ?? 0) === 0;

if (writesRequired && zeroWrites) {
  // Auto-retry with explicit feedback
  retryFeedback = 'Phase completed with 0 file writes. Use the write tool.';
  continue;
}
```

**Check write tracking:**

```typescript
// Is PhaseExecutionResult tracking write counts?
interface PhaseExecutionResult {
  explicitWrites?: number;  // Must be populated by the sub-agent callback
  fileOps?: number;
  writtenFiles?: string[];
}
```

**Fix checklist:**
- [ ] Zero-write gate exists before LLM evaluation (Rule 1.3)
- [ ] Gate exempts read-only purposes (think, plan, quick)
- [ ] `explicitWrites` populated by PhaseExecuteHandler callback
- [ ] Retry feedback explicitly says "call the write tool"

### 4. Apply Fix

After identifying root cause, apply the minimal fix following the constitution's rules. Verify the fix does not introduce new violations.

### 5. Verify Fix

After applying the fix:

1. Reproduce the original failure scenario
2. Confirm the failure no longer occurs
3. Check that no new issues were introduced
4. Verify all 7 hard-stop rules still hold (Section I)
5. Run `/test-llm-pipeline-architect` if available

---

## Error Handling

**Multiple Failures**: If the user reports multiple symptoms, prioritize by category priority (Critical > High > Medium > Low). Fix one at a time.

**Framework-Specific Bugs**: If the pipeline uses LangChain/LangGraph, adapt the diagnostic procedures to that framework's idioms while checking the same architectural invariants.

**Missing Source Code**: If the user does not provide pipeline source, ask for:
1. The pipeline entry point module
2. The evaluation/retry loop code
3. The context builder logic
4. Any error messages or logs

## Examples

### Example 1: Infinite Loop
```text
/debug-llm-pipeline-architect "
Our pipeline keeps retrying phase 2 forever. The evaluator says
'return-to-step' but it never stops. We have 6 phases and phase 2
is 'implement the API routes'. Logs show 50+ evaluation attempts.
"
```

### Example 2: Context Exhaustion
```text
/debug-llm-pipeline-architect "
Pipeline works great for 2-phase plans but phase 4+ produces
garbage output. The model seems confused about what was already
done. We pass full conversation history to each phase.
"
```

### Example 3: Silent Failure
```text
/debug-llm-pipeline-architect "
User sends a message and the pipeline starts (we see the
classification log) but then nothing happens. No error, no
response, no events. The frontend just spins.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/llm-pipeline-architect/llm-pipeline-architect-constitution.md` Sections I, IV
- **Related**: scaffold-llm-pipeline-architect, test-llm-pipeline-architect, refactor-llm-pipeline-architect
