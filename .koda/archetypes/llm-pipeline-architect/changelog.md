# Changelog — LLM Pipeline Architect

## [1.0.0] — 2026-03-02

### Added

- **Constitution** (`llm-pipeline-architect-constitution.md`)
  - 7 hard-stop rules: classify every message, loop guards, deterministic gates, context handoff, graceful degradation, no hardcoded models, streaming events
  - 10 mandatory patterns: pipeline entry point, intent classifier, task planner, while-loop execution, phase evaluator, loop guard, quality gate, context builder, message sink, event bus
  - 8 recommended patterns: cross-phase learnings, compare-first, plan announcements, phase summaries, model tiering, cost tracking, token budget, human-in-the-loop
  - Troubleshooting guide with 6 common issues
  - Security and performance checklist
  - Refusal template with worked example
  - Related documents referencing 12 BluePearl source modules

- **Scaffold workflow** (`scaffold-llm-pipeline-architect.md`)
  - 12-step generation: pipeline entry point, classifier, routing analyzer, task planner, phase evaluator, loop guard, context builder, event bus, model router, cross-phase learnings
  - Post-scaffold checklist for core and optional components
  - 3 examples: full pipeline, minimal pipeline, framework adapter

- **Compare workflow** (`compare-llm-pipeline-architect.md`)
  - 6 comparison types: framework, architecture, model routing, evaluation, context strategy, streaming
  - Pre-built comparison tables: LangChain vs LangGraph vs CrewAI vs Custom
  - Model routing strategy comparison (single vs purpose-based vs complexity-based)
  - Evaluation strategy comparison (LLM-only vs deterministic+LLM)
  - Context handoff comparison (full replay vs summarization vs file manifest)

- **Debug workflow** (`debug-llm-pipeline-architect.md`)
  - 9 failure categories with priority classification
  - Diagnostic procedures: infinite loop, silent failure, context exhaustion, wrong model routing, zero-write phases
  - Fix checklists for each failure category
  - Code-level diagnostic examples from BluePearl reference

- **Refactor workflow** (`refactor-llm-pipeline-architect.md`)
  - 14-point stage inventory audit
  - Hard-stop rule compliance matrix
  - 3-priority refactoring approach (P1: violations, P2: missing patterns, P3: recommendations)
  - 7 incremental refactoring procedures with before/after code
  - Post-refactoring validation checklist

- **Test workflow** (`test-llm-pipeline-architect.md`)
  - Tests for all 7 hard-stop rules with TypeScript test templates
  - Tests for mandatory patterns (pipeline flow, evaluator verdicts, while-loop execution)
  - Integration tests (end-to-end flow, safety valve)
  - Structured test report template

- **Document workflow** (`document-llm-pipeline-architect.md`)
  - Pipeline flow diagram (ASCII)
  - Stage documentation table
  - Type reference with all core interfaces
  - Event catalog with 8 event types and payloads
  - Model routing table with 7 purpose slots
  - Configuration reference with 10 parameters

- **Manifest** (`manifest.yaml`) — 13 keywords, 6 workflow entries
- **README** — Updated with workflow table, key deliverables, constitution highlights, reference implementation
