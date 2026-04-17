# Changelog — Prompt Template Engineer

## [1.0.0] — 2026-03-02

### Added

- **Constitution** (`prompt-template-engineer-constitution.md`)
  - 6 hard-stop rules: no inline prompt strings, input sanitization on every render, type-safe template data, prompt files read-only, user content as data only, isolated template engine instance
  - 10 mandatory patterns: engine setup, type-safe name registry, multi-path resolution, template caching, sanitization pipeline, prompt file system layout, prompt composition, custom helpers, prompt specification document, persona file system
  - 8 recommended patterns: testing harness, version tags, token counting pre-render, catalog generator, variable documentation, diff/review tooling, cache invalidation strategy, multi-language template support
  - Troubleshooting guide with 6 common issues
  - Security and performance checklist (24 items)
  - Refusal template with worked example
  - Related documents referencing 9 BluePearl source files and 7 industry references

- **Scaffold workflow** (`scaffold-prompt-template-engineer.md`)
  - 12-step generation: engine module, data interfaces, name registry, file layout, system prompt builder, persona files, example templates, prompt spec doc, sanitization tests
  - Post-scaffold checklist for core, file system, and documentation components
  - 3 examples: full TypeScript system, Python minimal, add to existing project

- **Compare workflow** (`compare-prompt-template-engineer.md`)
  - 6 comparison types: template engine, architecture, sanitization, caching, persona system, prompt testing
  - Pre-built tables: Handlebars vs Jinja2 vs Mustache vs Nunjucks vs raw strings
  - Architecture comparison: prompt-as-files vs inline vs database-backed vs hybrid
  - Sanitization strategy comparison: regex pipeline vs schema validation vs library-based
  - Persona system comparison: multi-file vs single-file vs database-backed

- **Debug workflow** (`debug-prompt-template-engineer.md`)
  - 10 failure categories with priority classification (P0–P3)
  - Diagnostic procedures: prompt injection, template not found, variable undefined, stale cache, persona loading
  - Code-level diagnostic examples with logging patterns
  - Fix checklists per failure category

- **Refactor workflow** (`refactor-prompt-template-engineer.md`)
  - 5-step codebase inventory (inline strings, existing templates, sanitization, type safety)
  - Hard-stop violation identification matrix
  - 3-priority refactoring plan (P1: violations, P2: missing patterns, P3: improvements)
  - Step-by-step inline prompt extraction procedure with before/after code
  - Post-refactoring validation and report template

- **Test workflow** (`test-prompt-template-engineer.md`)
  - Tests for all 6 hard-stop rules with TypeScript test templates
  - Tests for mandatory patterns (engine setup, name registry, resolution, caching, layout)
  - Prompt injection resistance tests (null bytes, oversized payloads, nested objects, control chars)
  - Template rendering correctness tests (complete data, optional fields, custom helpers)
  - Structured test report template

- **Document workflow** (`document-prompt-template-engineer.md`)
  - Architecture overview with component diagram
  - Template catalog with per-template documentation
  - Variable reference extracted from typed interfaces
  - Sanitization pipeline documentation
  - Persona system documentation
  - Helper function reference
  - Configuration reference
  - Quick start guide

- **Manifest** (`manifest.yaml`) — 13 keywords, 6 workflow entries
- **README** — Updated with workflow table, key deliverables, constitution highlights, reference implementation
