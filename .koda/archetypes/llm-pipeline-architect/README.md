# LLM Pipeline Architect

Design and build AI agent orchestration pipelines with intent classification, multi-phase task planning, purpose-based model routing, phase evaluation with retry/replan, deterministic quality gates, context handoff, cross-phase memory, and streaming event architectures.

## Status

**Complete** — Constitution, all 6 workflows, manifest, and documentation finalized.

## Workflows

| Workflow | Command | Purpose |
|----------|---------|---------|
| Scaffold | `/scaffold-llm-pipeline-architect` | Generate a complete pipeline from scratch |
| Compare | `/compare-llm-pipeline-architect` | Compare frameworks, architectures, routing strategies |
| Debug | `/debug-llm-pipeline-architect` | Diagnose infinite loops, context exhaustion, silent failures |
| Refactor | `/refactor-llm-pipeline-architect` | Audit and improve an existing pipeline |
| Test | `/test-llm-pipeline-architect` | Validate classification, guards, gates, and flow |
| Document | `/document-llm-pipeline-architect` | Generate flow diagrams, API docs, event catalogs |

## Key Deliverables

- **Pipeline entry point** — Classify → Route → Plan → Execute loop
- **Intent classifier** — Heuristic classification with slash command support
- **Task planner** — THINK model decomposition into bounded phases
- **Phase evaluator** — 4 verdict types: proceed, retry, replan, summarize
- **Loop guard** — Per-step max retries (3) + global replan limit (1)
- **Quality gates** — Deterministic zero-write gate before LLM evaluation
- **Context builder** — Briefs + file manifests, not full replay
- **Event bus** — 8 typed events for streaming observability

## Constitution Highlights

- **7 hard-stop rules** — Classify every message, loop guards, deterministic gates, context handoff, graceful degradation, no hardcoded models, streaming events
- **10 mandatory patterns** — Pipeline entry point, classifier, planner, while-loop execution, evaluator, loop guard, quality gate, context builder, message sink, event bus
- **8 recommended patterns** — Cross-phase learnings, compare-first, plan announcements, phase summaries, model tiering, cost tracking, token budget, human-in-the-loop

## Reference Implementation

BluePearl's orchestration pipeline (~2,500 lines across 10+ modules):

- `backend/orchestrator/src/pipeline.ts` — Core orchestration (994 lines)
- `backend/orchestrator/src/classify/intent-classifier.ts` — Heuristic classification
- `backend/orchestrator/src/plan/task-planner.ts` — THINK model decomposition
- `backend/orchestrator/src/evaluate/phase-evaluator.ts` — QUICK model evaluation
- `backend/orchestrator/src/evaluate/loop-guard.ts` — Per-step + global limits
- `backend/orchestrator/src/prompt/context-builder.ts` — Phase context assembly
- `backend/orchestrator/src/execute/phase-learnings.ts` — Cross-phase memory
- `backend/shared/src/model-tiers.ts` — 3-tier model preference with probe logic

## Related Archetypes

- `language-model-evaluation` — Evaluating model outputs with custom graders (not pipeline orchestration)
- `responsible-prompting` — Ethical prompt content and guardrails (not pipeline architecture)
- `prompt-template-engineer` — Template engine implementation (not pipeline flow)
- `model-architect` — Model training and fine-tuning (not runtime orchestration)
