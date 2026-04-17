# Prompt Template Engineer

Design and build structured prompt management systems with template engines, type-safe loading, caching, input sanitization, prompt poisoning resistance, persona file systems, prompt-as-files architecture, and prompt testing frameworks.

## Status

**Complete** — Constitution (6 hard-stop rules, 10 mandatory patterns, 8 recommended patterns), all 6 workflows, manifest, and changelog delivered.

## Workflows

| Command | Purpose |
|---------|---------|
| `/scaffold-prompt-template-engineer` | Generate complete prompt system: engine, types, file layout, persona, sanitization |
| `/compare-prompt-template-engineer` | Compare template engines, architectures, sanitization strategies |
| `/debug-prompt-template-engineer` | Diagnose template resolution, injection, caching, persona issues |
| `/refactor-prompt-template-engineer` | Extract inline prompts to files, add type safety, sanitization, caching |
| `/test-prompt-template-engineer` | Validate sanitization, type coverage, injection resistance, rendering |
| `/document-prompt-template-engineer` | Generate template catalog, variable reference, architecture docs |

## Key Deliverables

- **Template engine module** — Isolated instance, `noEscape`, multi-path resolution, caching, sanitization
- **Type-safe template name registry** — Union type of valid template names with compile-time checking
- **Typed data interfaces** — One interface per template, no `any` or untyped variable bags
- **Input sanitization pipeline** — Null bytes, control characters, length truncation (OWASP LLM01)
- **Prompt file system layout** — `system/`, `templates/`, `persona/` directory structure
- **Persona file system** — 7-file profile structure (IDENTITY, SOUL, USER, TOOLS, AGENTS, MEMORY, BOOTSTRAP)
- **Prompt composition pattern** — Base + mode-specific append + persona + phase context layering
- **Prompt specification document** — Purpose, model tier, data interface, output format per template

## Constitution Highlights

- **6 hard-stop rules**: No inline prompts, input sanitization on every render, type-safe data, read-only files, user content as data only, isolated engine instance
- **10 mandatory patterns**: Engine setup, name registry, multi-path resolution, caching, sanitization pipeline, file layout, composition, helpers, prompt spec, persona system
- **8 recommended patterns**: Testing harness, version tags, token counting, catalog generator, variable docs, diff tooling, cache invalidation, multi-language support

## Reference Implementation

| File | Role |
|------|------|
| `backend/orchestrator/src/prompt/template-engine.ts` | Core engine: isolated Handlebars, multi-path resolution, caching, sanitization |
| `backend/orchestrator/src/prompt/template-data-types.ts` | 18 typed data interfaces |
| `backend/orchestrator/src/prompt/system-prompt.ts` | System prompt builder with persona composition |
| `backend/service/prompts/templates/*.hbs` | 18 Handlebars template files |
| `backend/service/profiles/default/` | 7 persona files (IDENTITY, SOUL, USER, etc.) |

## Related Archetypes

- `responsible-prompting` — Ethical prompt content (bias, safety, fairness) — not prompt system architecture
- `llm-pipeline-architect` — Pipeline orchestration — consumes templates rendered by this archetype
- `language-model-evaluation` — Model output evaluation — not template engineering
