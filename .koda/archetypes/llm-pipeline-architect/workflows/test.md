---
description: Validate AI agent orchestration pipeline for classification accuracy, loop guard limits, quality gate enforcement, context handoff efficiency, and end-to-end flow correctness
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read validation criteria from:
`${ARCHETYPES_BASEDIR}/llm-pipeline-architect/llm-pipeline-architect-constitution.md`

Focus on Section I (Hard-Stop Rules), Section II (Mandatory Patterns), and Section V (Security and Performance Checklist).

### 2. Identify Test Scope

Extract from $ARGUMENTS:

| Scope | What is Tested |
|-------|---------------|
| **Full** | All 7 hard-stop rules, all 10 mandatory patterns, end-to-end flow |
| **Classification** | Intent classifier accuracy, slash command routing, short-circuit logic |
| **Evaluation** | Phase evaluator verdicts, loop guard limits, deterministic gates |
| **Context** | Context builder efficiency, brief generation, token budget |
| **Integration** | End-to-end pipeline flow with mock sub-agents |
| **Resilience** | Graceful degradation, fallback behavior, error recovery |

### 3. Hard-Stop Rule Tests

#### Test 3.1 — Classify Every Message (Rule 1.1)

```typescript
// Test: Every message type must produce a classification result
describe('Rule 1.1: Classify every message', () => {
  it('classifies greetings as chat with high confidence', async () => {
    const result = await classifyIntent('hello', options);
    expect(result.purpose).toBe('chat');
    expect(result.confidence).toBe('high');
    expect(result.requiresPlanning).toBe(false);
  });

  it('classifies short inputs as chat', async () => {
    const result = await classifyIntent('hi', options);
    expect(result.purpose).toBe('chat');
  });

  it('classifies slash commands as plan', async () => {
    const result = await classifyIntent('/scaffold a REST API', options);
    expect(result.requiresPlanning).toBe(true);
    expect(result.slashCommand).toBe('scaffold');
  });

  it('classifies complex requests as chat (agent decides)', async () => {
    const result = await classifyIntent('Build me a data pipeline with tests', options);
    expect(result.purpose).toBe('chat');
    // Agent will use plan tool if needed
  });

  it('never returns undefined or null classification', async () => {
    const inputs = ['', '  ', 'x', 'hello!', '/unknown-command'];
    for (const input of inputs) {
      const result = await classifyIntent(input, options);
      expect(result).toBeDefined();
      expect(result.purpose).toBeDefined();
    }
  });
});
```

#### Test 3.2 — Loop Guards (Rule 1.2)

```typescript
describe('Rule 1.2: Loop guards on every evaluation', () => {
  it('limits evaluations per step to MAX_EVALUATIONS_PER_STEP', () => {
    const guard = createLoopGuard();
    const stepId = 'phase-1';

    for (let i = 0; i < MAX_EVALUATIONS_PER_STEP; i++) {
      expect(canEvaluate(guard, stepId)).toBe(true);
      recordEvaluation(guard, stepId);
    }

    expect(canEvaluate(guard, stepId)).toBe(false);
  });

  it('tracks evaluations independently per step', () => {
    const guard = createLoopGuard();

    recordEvaluation(guard, 'phase-1');
    recordEvaluation(guard, 'phase-1');

    expect(canEvaluate(guard, 'phase-1')).toBe(true); // 2 < 3
    expect(canEvaluate(guard, 'phase-2')).toBe(true); // 0 < 3
  });

  it('limits replans to MAX_REPLANS_PER_RUN', () => {
    const guard = createLoopGuard();

    for (let i = 0; i < MAX_REPLANS_PER_RUN; i++) {
      expect(canReplan(guard)).toBe(true);
      recordReplan(guard);
    }

    expect(canReplan(guard)).toBe(false);
  });

  it('pipeline terminates even with always-retry evaluator', async () => {
    // Mock evaluator that always returns 'return-to-step'
    const mockEvaluator = async () => ({
      verdict: 'return-to-step' as const,
      feedback: 'Not good enough',
      returnToStepId: 'phase-1',
    });

    // Pipeline must terminate within MAX_EVALUATIONS_PER_STEP iterations
    const result = await runPipelineWithMockEvaluator(mockEvaluator);
    expect(result.phases.length).toBeGreaterThan(0);
    // Should not hang or throw
  });
});
```

#### Test 3.3 — Deterministic Quality Gate (Rule 1.3)

```typescript
describe('Rule 1.3: Deterministic gate before LLM evaluation', () => {
  it('auto-retries implement phase with zero writes', async () => {
    const phase = { id: 'phase-1', purpose: 'implement', instruction: 'Create API' };
    const execResult = { status: 'success', output: 'Done!', explicitWrites: 0 };

    // Pipeline should auto-retry WITHOUT consulting LLM evaluator
    // Verify retry feedback mentions "write tool"
  });

  it('does not gate think-purpose phases', async () => {
    const phase = { id: 'phase-1', purpose: 'think', instruction: 'Analyze approach' };
    const execResult = { status: 'success', output: 'Analysis...', explicitWrites: 0 };

    // Pipeline should proceed — think phases are legitimately read-only
  });

  it('does not gate plan-purpose phases', async () => {
    const phase = { id: 'phase-1', purpose: 'plan', instruction: 'Design architecture' };
    const execResult = { status: 'success', output: 'Plan...', explicitWrites: 0 };

    // Pipeline should proceed — plan phases are legitimately read-only
  });
});
```

#### Test 3.4 — Context Handoff (Rule 1.4)

```typescript
describe('Rule 1.4: Context handoff, not full replay', () => {
  it('phase outputs stored as briefs under 500 chars', () => {
    const phaseOutputs: Record<string, string> = {};
    // After phase completion, verify stored brief is concise
    for (const [id, brief] of Object.entries(phaseOutputs)) {
      expect(brief.length).toBeLessThan(500);
    }
  });

  it('context size stays bounded across 6 phases', () => {
    const contexts: string[] = [];
    // Simulate 6-phase pipeline, measure context at each phase
    for (let i = 0; i < 6; i++) {
      const ctx = buildPhaseContextPrompt(mockPhaseContext(i, 6));
      contexts.push(ctx);
    }
    // Context should not grow unboundedly
    const maxContext = Math.max(...contexts.map(c => c.length));
    expect(maxContext).toBeLessThan(4000); // ~2000 tokens
  });

  it('file manifest contains paths only, not file contents', () => {
    const ctx = buildPhaseContextPrompt(mockPhaseContextWithFiles());
    expect(ctx).toContain('src/pipeline.ts');
    expect(ctx).not.toContain('import {'); // No file contents
  });
});
```

#### Test 3.5 — Graceful Degradation (Rule 1.5)

```typescript
describe('Rule 1.5: Graceful degradation', () => {
  it('falls back to onDirect when pipeline throws', async () => {
    let directCalled = false;
    const config = {
      onDirect: async () => { directCalled = true; },
      // Simulate pipeline failure by providing broken model
    };

    try {
      await runPipeline('test message', brokenConfig);
    } catch {
      // If pipeline throws, the caller must catch and call onDirect
    }

    // The integration layer must ensure directCalled === true
  });

  it('emits pipeline:error event on failure', async () => {
    const events: string[] = [];
    const bus = createMockBus((event) => events.push(event));

    // Trigger pipeline failure
    // Verify 'pipeline:error' is in events
  });
});
```

#### Test 3.6 — No Hardcoded Models (Rule 1.6)

```typescript
describe('Rule 1.6: No hardcoded model names', () => {
  it('pipeline code contains no literal model IDs', () => {
    const pipelineSource = readPipelineSourceFiles();
    const modelPatterns = [
      /gpt-[34]\w*/gi,
      /claude-\w+/gi,
      /gemini-\w+/gi,
      /llama-\w+/gi,
    ];

    for (const pattern of modelPatterns) {
      const matches = pipelineSource.match(pattern) ?? [];
      // Filter out comments and test files
      const codeMatches = matches.filter(m => !isInComment(m));
      expect(codeMatches).toHaveLength(0);
    }
  });

  it('all model references use resolveModelForPurpose', () => {
    // Verify model resolution uses purpose-based lookup
    const quickModel = resolveModelForPurpose('quick', envConfig);
    const thinkModel = resolveModelForPurpose('think', envConfig);
    expect(quickModel).toBeDefined();
    expect(thinkModel).toBeDefined();
  });
});
```

#### Test 3.7 — Streaming Events (Rule 1.7)

```typescript
describe('Rule 1.7: Streaming events for every stage', () => {
  it('emits all 8 event types during a successful run', async () => {
    const events: string[] = [];
    const bus = createEventBus();
    bus.on('*', (event) => events.push(event));

    await runPipeline('Build a REST API', fullConfig);

    expect(events).toContain('pipeline:start');
    expect(events).toContain('pipeline:classified');
    expect(events).toContain('pipeline:planned');
    expect(events).toContain('pipeline:phase-start');
    expect(events).toContain('pipeline:evaluation');
    expect(events).toContain('pipeline:phase-end');
    expect(events).toContain('pipeline:end');
  });

  it('emits pipeline:error on failure', async () => {
    const events: string[] = [];
    const bus = createEventBus();
    bus.on('*', (event) => events.push(event));

    try {
      await runPipeline('test', brokenConfig);
    } catch {}

    expect(events).toContain('pipeline:error');
  });
});
```

### 4. Mandatory Pattern Tests

#### Test 4.1 — Pipeline Flow (Pattern 2.1)

```typescript
describe('Pattern 2.1: Pipeline entry point', () => {
  it('follows classify -> route -> plan -> execute sequence', async () => {
    const stages: string[] = [];
    // Instrument pipeline to record stage order
    const result = await runInstrumentedPipeline('Build a REST API');

    expect(stages[0]).toBe('classify');
    expect(stages[1]).toBe('route');
    expect(stages[2]).toBe('plan');
    expect(stages[3]).toMatch(/^execute/); // execute-phase-1, etc.
  });

  it('direct route bypasses planning', async () => {
    let directCalled = false;
    const config = { onDirect: async () => { directCalled = true; } };

    await runPipeline('hello', config);
    expect(directCalled).toBe(true);
  });
});
```

#### Test 4.2 — Phase Evaluator Verdicts (Pattern 2.5)

```typescript
describe('Pattern 2.5: Phase evaluator verdicts', () => {
  it('returns valid verdict type', async () => {
    const evaluation = await evaluatePhase(mockEvalOptions);
    const validVerdicts = ['proceed', 'return-to-step', 'replan', 'summarize'];
    expect(validVerdicts).toContain(evaluation.verdict);
  });

  it('forces proceed at max iterations', async () => {
    const evaluation = await evaluatePhase({
      ...mockEvalOptions,
      iteration: 3,
      maxIterations: 3,
    });
    expect(evaluation.verdict).toBe('proceed');
  });

  it('defaults to proceed on evaluation failure', async () => {
    // Provide broken model that throws
    const evaluation = await evaluatePhase({
      ...mockEvalOptions,
      model: brokenModel,
    });
    expect(evaluation.verdict).toBe('proceed');
  });
});
```

#### Test 4.3 — While-Loop Execution (Pattern 2.4)

```typescript
describe('Pattern 2.4: While-loop phase execution', () => {
  it('supports retry by holding phase index', async () => {
    // Mock evaluator: return-to-step on first eval, proceed on second
    let evalCount = 0;
    const mockEval = async () => ({
      verdict: (++evalCount === 1) ? 'return-to-step' : 'proceed',
      feedback: 'Retry once',
      returnToStepId: 'phase-1',
    });

    const result = await runPipelineWithMockEvaluator(mockEval);
    // Phase 1 should have been executed twice
  });

  it('supports replan by resetting phase index', async () => {
    // Mock evaluator: replan on first phase
    // Verify pipeline creates new plan and restarts from phase 0
  });
});
```

### 5. Integration Tests

#### Test 5.1 — End-to-End Pipeline Flow

```typescript
describe('End-to-end pipeline', () => {
  it('executes a 3-phase plan successfully', async () => {
    const result = await runPipeline('Build a REST API with tests', fullConfig);

    expect(result.classification).toBeDefined();
    expect(result.routing).toBeDefined();
    expect(result.plan).toBeDefined();
    expect(result.plan.phases.length).toBeGreaterThanOrEqual(1);
    expect(result.plan.phases.length).toBeLessThanOrEqual(6);
    expect(result.phases.length).toBe(result.plan.phases.length);
    expect(result.totalDuration).toBeGreaterThan(0);
  });

  it('empty-workflow safety valve catches invalid plans', async () => {
    // Plan with phases but no workflows should fall back to direct
    const result = await runPipelineWithMockPlanner(emptyWorkflowPlan);
    expect(result.phases).toHaveLength(0);
    // onDirect should have been called
  });
});
```

### 6. Generate Test Report

```text
## Pipeline Validation Report

**Pipeline Under Test**: {pipeline_location}
**Test Date**: {timestamp}
**Test Scope**: {scope}

### Hard-Stop Rule Compliance

| Rule | Test Count | Passed | Failed | Status |
|------|-----------|--------|--------|--------|
| 1.1 Classify every message | {n} | {pass} | {fail} | {PASS/FAIL} |
| 1.2 Loop guards | {n} | {pass} | {fail} | {PASS/FAIL} |
| 1.3 Deterministic gates | {n} | {pass} | {fail} | {PASS/FAIL} |
| 1.4 Context handoff | {n} | {pass} | {fail} | {PASS/FAIL} |
| 1.5 Graceful degradation | {n} | {pass} | {fail} | {PASS/FAIL} |
| 1.6 No hardcoded models | {n} | {pass} | {fail} | {PASS/FAIL} |
| 1.7 Streaming events | {n} | {pass} | {fail} | {PASS/FAIL} |

### Mandatory Pattern Coverage

| Pattern | Tested | Status |
|---------|--------|--------|
| 2.1 Pipeline entry point | {yes/no} | {PASS/FAIL} |
| 2.2 Intent classifier | {yes/no} | {PASS/FAIL} |
| 2.3 Task planner | {yes/no} | {PASS/FAIL} |
| 2.4 While-loop execution | {yes/no} | {PASS/FAIL} |
| 2.5 Phase evaluator | {yes/no} | {PASS/FAIL} |
| 2.6 Loop guard | {yes/no} | {PASS/FAIL} |
| 2.7 Deterministic gate | {yes/no} | {PASS/FAIL} |
| 2.8 Context builder | {yes/no} | {PASS/FAIL} |
| 2.9 Message sink | {yes/no} | {PASS/FAIL} |
| 2.10 Event bus | {yes/no} | {PASS/FAIL} |

### Integration Tests

| Test | Status | Notes |
|------|--------|-------|
| End-to-end 3-phase plan | {PASS/FAIL} | |
| Safety valve (empty workflows) | {PASS/FAIL} | |
| Direct route bypass | {PASS/FAIL} | |

### Overall Verdict: {PASS / PASS WITH WARNINGS / FAIL}

{Summary of findings and recommendations}
```

---

## Error Handling

**No Test Framework**: If the pipeline has no test setup, generate test files using the project's existing test framework (vitest, jest, pytest) or recommend one.

**Mock Complexity**: Provide mock factories for common dependencies (LLM models, event bus, sub-agent sessions) to simplify test setup.

**Existing Tests**: If tests already exist, audit them against the constitution checklist and identify gaps.

## Examples

### Example 1: Full Validation
```text
/test-llm-pipeline-architect "
Run full validation of our pipeline at src/orchestrator/.
Check all 7 hard-stop rules and 10 mandatory patterns.
We use vitest for testing.
"
```

### Example 2: Loop Guard Focus
```text
/test-llm-pipeline-architect "
Our pipeline has loop guards but we're not sure they work correctly.
Test that the guard prevents infinite retries and that replan limits
are enforced. Loop guard is in src/evaluate/loop-guard.ts.
"
```

### Example 3: Classification Accuracy
```text
/test-llm-pipeline-architect "
Test our intent classifier against these message types:
greetings, slash commands, complex requests, empty inputs.
Classifier is in src/classify/intent-classifier.ts.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/llm-pipeline-architect/llm-pipeline-architect-constitution.md` Sections I, II, V
- **Related**: scaffold-llm-pipeline-architect, debug-llm-pipeline-architect
