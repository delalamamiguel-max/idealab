---
description: Generate comprehensive documentation for AI agent orchestration pipeline including flow diagrams, stage documentation, model routing tables, event catalogs, and configuration references
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read documentation context from:
`${ARCHETYPES_BASEDIR}/llm-pipeline-architect/llm-pipeline-architect-constitution.md`

Focus on Section II (Mandatory Patterns) for component descriptions and Section VII (Related Documents) for reference links.

### 2. Identify Documentation Scope

Extract from $ARGUMENTS:

| Document Type | Description |
|--------------|-------------|
| **Full package** | All documents listed below |
| **Architecture overview** | Pipeline flow diagram + stage descriptions |
| **API reference** | Type definitions, function signatures, config options |
| **Event catalog** | All pipeline events with payload schemas |
| **Model routing table** | Purpose slots, tier preferences, probe logic |
| **Operations guide** | Deployment, configuration, monitoring, troubleshooting |
| **Developer guide** | How to extend, add stages, customize evaluation |

### 3. Generate Pipeline Flow Diagram

Create an ASCII or Mermaid diagram of the pipeline flow:

```text
Pipeline Flow Diagram
=====================

    ┌─────────────┐
    │   Message    │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Classify   │ ◄── QUICK model
    │  (Stage 1)  │     Short-circuit: greetings, slash commands
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │   Route     │     direct → onDirect callback (fast-path)
    │  (Stage 2)  │     single-skill / multi-skill → continue
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │    Plan     │ ◄── THINK model
    │  (Stage 3)  │     Decompose into phases (max 6)
    └──────┬──────┘     Fallback: single-phase plan on JSON error
           │
    ┌──────▼──────┐
    │  Enforce    │     Compare-first: if skills present,
    │  (Stage 4)  │     first phase must be compare workflow
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Announce   │     Inject plan summary into chat stream
    │  (Stage 5)  │     via MessageSink callback
    └──────┬──────┘
           │
    ┌──────▼──────────────────────────────────┐
    │         Phase Execution Loop            │
    │         (Stage 6)                       │
    │                                         │
    │  ┌───────────┐                          │
    │  │ Build Ctx │ Phase context + skill    │
    │  │           │ context + learnings      │
    │  └─────┬─────┘                          │
    │        │                                │
    │  ┌─────▼─────┐                          │
    │  │  Execute  │ Via PhaseExecuteHandler   │
    │  │  Phase    │ callback (sub-agent)      │
    │  └─────┬─────┘                          │
    │        │                                │
    │  ┌─────▼─────┐                          │
    │  │ Zero-Write│ Deterministic gate       │
    │  │   Gate    │ (implement/code only)    │
    │  └─────┬─────┘                          │
    │        │                                │
    │  ┌─────▼─────┐                          │
    │  │ Evaluate  │ ◄── QUICK model          │
    │  │  Phase    │     Verdicts:            │
    │  └─────┬─────┘     proceed / retry /    │
    │        │           replan / summarize   │
    │        │                                │
    │  ┌─────▼─────┐                          │
    │  │Loop Guard │ Per-step: max 3          │
    │  │  Check    │ Global replan: max 1     │
    │  └─────┬─────┘                          │
    │        │                                │
    │  ┌─────▼─────┐                          │
    │  │ Summarize │ QUICK model brief        │
    │  │ + Learn   │ + learnings extraction   │
    │  └─────┬─────┘                          │
    │        │                                │
    │   Next phase or done                    │
    └─────────────────────────────────────────┘
           │
    ┌──────▼──────┐
    │  Complete   │     Assemble PipelineResult
    │  (Stage 7)  │     Emit pipeline:end event
    └─────────────┘
```

### 4. Generate Stage Documentation

For each pipeline stage, document:

| Stage | Module | Model Tier | Input | Output | Events Emitted |
|-------|--------|-----------|-------|--------|----------------|
| 1. Classify | intent-classifier | QUICK | Raw message | IntentClassification | pipeline:classified |
| 2. Route | routing-analyzer | None (code) | IntentClassification | RoutingDecision | — |
| 3. Plan | task-planner | THINK | Message + routing | TaskPlan | pipeline:planned |
| 4. Enforce | compare-enforcer | None (code) | TaskPlan | TaskPlan (modified) | — |
| 5. Announce | template-engine | None (render) | TaskPlan | Markdown string | — (via messageSink) |
| 6. Execute | pipeline (loop) | Per-phase purpose | PhaseContext + instruction | PhaseExecutionResult | pipeline:phase-start, pipeline:evaluation, pipeline:phase-end |
| 7. Complete | pipeline | None | All results | PipelineResult | pipeline:end |

### 5. Generate Type Reference

Document all core types:

```typescript
// Intent Classification
interface IntentClassification {
  utteranceType: 'imperative' | 'declarative' | 'interrogative';
  purpose: 'plan' | 'chat';
  confidence: 'high' | 'medium' | 'low';
  requiresPlanning: boolean;
  suggestedSkills: string[];
  routing: 'direct' | 'single-skill' | 'multi-skill';
  slashCommand?: string;
  slashCommandArgs?: string;
}

// Task Plan
interface TaskPlan {
  summary: string;
  phases: PlannedPhase[];
  branchStrategy: BranchStrategy;
}

interface PlannedPhase {
  id: string;
  instruction: string;
  purpose: ModelPurpose;
  skill?: string;
  workflow?: WorkflowType;
  dependsOn: string[];
  canParallelize: boolean;
  complexity?: TaskComplexity;
  autoSelectedModel?: string;
}

// Phase Evaluation
interface PhaseEvaluation {
  verdict: EvaluationVerdict;
  feedback: string;
  iteration: number;
  maxIterations: number;
  returnToStepId?: string;
}

type EvaluationVerdict = 'proceed' | 'return-to-step' | 'replan' | 'summarize';

// Pipeline Result
interface PipelineResult {
  runId: string;
  classification: IntentClassification;
  routing: RoutingDecision;
  plan?: TaskPlan;
  phases: PhaseResult[];
  phaseOutputs: Record<string, string>;
  totalDuration: number;
  compareEnforced: boolean;
  skillOverrides: Array<{ phaseId: string; originalSkill: string; newSkill: string; reason: string }>;
}
```

### 6. Generate Event Catalog

Document every pipeline event with its payload:

| Event | When Emitted | Payload Fields |
|-------|-------------|---------------|
| `pipeline:start` | Pipeline begins processing | runId, sessionId, message |
| `pipeline:classified` | After intent classification | runId, classification |
| `pipeline:planned` | After task planning (and after replan) | runId, plan |
| `pipeline:phase-start` | Before each phase executes | runId, phaseId, phaseIndex, totalPhases, instruction |
| `pipeline:evaluation` | After phase evaluation | runId, phaseId, evaluation |
| `pipeline:phase-end` | After phase completes | runId, phaseId, result |
| `pipeline:end` | Pipeline finishes successfully | runId, sessionId |
| `pipeline:error` | Pipeline encounters an error | runId, error |

### 7. Generate Model Routing Table

Document purpose-based model assignment:

| Purpose | Used By | Tier 1 (Preferred) | Tier 2 (Fallback) | Tier 3 (Safe) |
|---------|---------|-------------------|-------------------|---------------|
| `think` | Task planner | {tier1_model} | {tier2_model} | {tier3_model} |
| `plan` | Plan refinement | {tier1_model} | {tier2_model} | {tier3_model} |
| `implement` | Code generation phases | {tier1_model} | {tier2_model} | {tier3_model} |
| `code` | Focused coding tasks | {tier1_model} | {tier2_model} | {tier3_model} |
| `quick` | Classification, evaluation, briefs, learnings | {tier1_model} | {tier2_model} | {tier3_model} |
| `chat` | Direct conversation | {tier1_model} | {tier2_model} | {tier3_model} |
| `default` | Unspecified purpose | {tier1_model} | {tier2_model} | {tier3_model} |

**Tier Resolution Logic**: At startup, probe the model provider's API (`/v1/models`). For each purpose, select the highest available tier. If Tier 1 is unavailable, fall up to Tier 2, then Tier 3.

### 8. Generate Configuration Reference

Document all configurable parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `maxPhasesPerPlan` | number | 6 | Maximum phases the planner can create |
| `maxEvaluationsPerStep` | number | 3 | Per-step retry limit before forced proceed |
| `maxReplansPerRun` | number | 1 | Global replan limit per pipeline run |
| `maxOutputCharsForEval` | number | 8000 | Truncation limit for evaluator input |
| `maxBriefChars` | number | 300 | Target length for phase output briefs |
| `contextTokenBudget` | number | 2000 | Max tokens for phase context prompt |
| `learningsFilePath` | string | `.bluepearl/phase-learnings.md` | Cross-phase memory file location |
| `enableCompareFirst` | boolean | true | Enforce compare-first workflow ordering |
| `enableAutoSelect` | boolean | true | Auto-select models by complexity |
| `enableLearnings` | boolean | true | Extract cross-phase learnings |

### 9. Generate Operations Guide (if full package)

Include:

- **Deployment**: How to deploy the pipeline as part of a service
- **Monitoring**: Which events to observe, what metrics to track
- **Alerting**: When to alert (infinite loops detected, pipeline errors, high latency)
- **Troubleshooting**: Link to constitution Section IV and debug workflow
- **Scaling**: How the pipeline behaves under concurrent requests

### 10. Assemble Documentation Package

Combine all generated documents into a coherent package:

```text
Documentation Package:
  docs/
    pipeline-architecture.md      — Flow diagram + stage descriptions
    pipeline-api-reference.md     — Type definitions + function signatures
    pipeline-event-catalog.md     — All events with payloads
    pipeline-model-routing.md     — Purpose slots + tier tables
    pipeline-configuration.md     — All configurable parameters
    pipeline-operations-guide.md  — Deploy, monitor, troubleshoot
    pipeline-developer-guide.md   — Extend, customize, add stages
```

---

## Error Handling

**No Pipeline Code**: If the user has not yet scaffolded a pipeline, generate documentation for the reference architecture from the constitution. Note that specific implementation details will need to be updated after scaffolding.

**Partial Pipeline**: If only some components exist, document what exists and mark missing components with "Not Yet Implemented" placeholders.

**Framework-Specific**: Adapt documentation to the framework (LangChain, LangGraph, etc.) while maintaining the same architectural concepts.

## Examples

### Example 1: Full Documentation Package
```text
/document-llm-pipeline-architect "
Generate full documentation for our pipeline at
backend/orchestrator/src/. Include flow diagrams, API reference,
event catalog, and operations guide.
"
```

### Example 2: Event Catalog Only
```text
/document-llm-pipeline-architect "
Generate an event catalog for our pipeline. We need to know
every event type, when it fires, and what data it carries.
Pipeline is in src/pipeline.ts.
"
```

### Example 3: Model Routing Documentation
```text
/document-llm-pipeline-architect "
Document our model routing strategy. We use LiteLLM with
3-tier model preferences. Need a table showing which model
is used for each pipeline stage and purpose.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/llm-pipeline-architect/llm-pipeline-architect-constitution.md` Sections II, VII
- **Related**: scaffold-llm-pipeline-architect, compare-llm-pipeline-architect
