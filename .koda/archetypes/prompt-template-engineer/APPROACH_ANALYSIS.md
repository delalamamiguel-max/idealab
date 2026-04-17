# Prompt Template Engineer: Approach Analysis

**Analysis Date**: March 2026
**Source**: `docs/plans/new-archetypes.md` § CREATE NEW #4
**Status**: Pre-creation analysis — constitution and workflows not yet built

---

## 1. Why This Archetype Exists

`responsible-prompting` focuses on **ethical prompt content** — bias detection, safety guardrails, fairness evaluation. It does not cover the engineering discipline of building structured prompt management systems. Prompt template engineering is a distinct concern that involves:

- Template engine selection and configuration (Handlebars, Jinja2, Mustache, custom)
- Type-safe template data interfaces (compile-time errors for missing/wrong variables)
- Multi-path template resolution (env var → relative → absolute fallback chain)
- Template caching for performance
- Input sanitization against prompt injection (null bytes, control characters, length truncation)
- Prompt-as-files architecture (not inline strings in code)
- Persona file systems (user-editable identity layers loaded at runtime)
- Prompt composition and chaining (base + mode-specific append + phase context)
- Prompt versioning and A/B testing
- Prompt testing frameworks (expected output assertions)

Teams that embed prompts as inline strings end up with:

- Unmaintainable prompt spaghetti scattered across codebase
- No type safety — template variables are string-interpolated with no validation
- Prompt injection vulnerabilities — user input concatenated directly into system prompts
- No caching — same template re-parsed on every call
- No testing — prompt changes deployed blind with no regression checks
- No versioning — prompt history lost in git diffs of code files
- No persona customization — hardcoded identity that can't be adjusted per user

---

## 2. Reference Implementation

BluePearl's prompt management system serves as the battle-tested reference:

| File | Lines | Role |
|------|-------|------|
| `backend/orchestrator/src/prompt/template-engine.ts` | ~173 | Core engine: isolated Handlebars instance, type-safe template name registry (18 named templates), multi-path resolution, template caching via Map, input sanitization (null bytes, control chars, 10K truncation), custom helpers (eq, add, gt, formatDuration, toLocaleString) |
| `backend/orchestrator/src/prompt/template-data-types.ts` | ~200 | Typed data interfaces: each template has a corresponding TypeScript interface; compile-time type checking for template data |
| `backend/service/prompts/system/base.md` | ~40 | Base system prompt — identity, core principles |
| `backend/service/prompts/system/append-coding.md` | ~20 | Mode-specific append for coding context |
| `backend/service/prompts/system/append-working.md` | ~15 | Mode-specific append for working context |
| `backend/service/prompts/templates/*.hbs` | ~18 files | Handlebars templates for pipeline stages: intent-classifier, task-planner, phase-evaluator, phase-context, skill-prompt, plan-announcement, phase-summary, journal-summary, system-prompt, etc. |
| `docs/prompting/prompt-reference.md` | ~227 | Full template specification: purpose, model tier, data interface, output format, skip conditions per template |

### Key Patterns to Encode

1. **Isolated template instance** — No global Handlebars state; create dedicated instance per engine to prevent cross-contamination
2. **Type-safe template name registry** — Union type of valid template names; compile-time errors for typos or missing templates
3. **Multi-path resolution** — Template file lookup chain: env var → `__dirname`-relative → `process.cwd()`-relative → container absolute paths
4. **Template caching** — `Map<string, CompiledTemplate>` prevents re-parsing on every render
5. **Input sanitization pipeline** — Strip null bytes → remove control characters → truncate to max length (10K default)
6. **`noEscape: true`** — HTML entity encoding is meaningless in LLM context; disable it
7. **Custom helpers** — Application-specific helpers registered on the isolated instance (eq, add, gt, formatDuration)
8. **Prompt-as-files** — `system/` for base prompts, `templates/` for Handlebars, `persona/` for user-editable files
9. **Prompt composition** — Base system prompt + mode-specific append + persona files; layered, not concatenated
10. **Persona system** — 7-file profile structure (USER.md, SOUL.md, IDENTITY.md, STYLE.md, BOUNDARIES.md, TOOLS.md, KNOWLEDGE.md) loaded at runtime via SDK's agentsFilesOverride
11. **Prompt poisoning resistance** — Templates read-only (440 permissions), user workspace files loaded as context data (never as system prompt fragments), template variables sanitized
12. **Prompt specification document** — Each template documented with purpose, model tier, data interface, output format, skip conditions

---

## 3. Scope Boundaries

### In Scope

- Template engine selection and configuration (Handlebars, Jinja2, Mustache, custom)
- Type-safe template data interfaces
- Multi-path template file resolution
- Template caching (Map, LRU, or equivalent)
- Input sanitization pipeline (null bytes, control chars, length limits)
- Prompt-as-files directory structure (`system/`, `templates/`, `persona/`)
- Prompt composition patterns (base + append + context layering)
- Persona file system architecture (user-editable identity files)
- Prompt poisoning resistance (file permissions, data placement, variable escaping)
- Custom template helpers
- Prompt specification documentation (purpose, model, interface, format per template)
- Prompt testing frameworks (expected output assertions, regression tests)
- Prompt versioning strategies (git-based, metadata DB, version tags)
- Token counting pre-render (cost control)
- Prompt catalog generation (visual documentation from templates)

### Out of Scope (Delegated)

- Ethical prompt content (bias, safety, fairness) → `responsible-prompting`
- LLM pipeline orchestration → `llm-pipeline-architect`
- Model evaluation and benchmarking → `language-model-evaluation`
- RAG / retrieval augmented generation → future archetype
- Fine-tuning data preparation → `model-architect`
- Frontend prompt input UI → `frontend-only`

---

## 4. Industry Standards Alignment

| Practice | Standard/Source | Constitution Section |
|----------|----------------|---------------------|
| Template-based prompts | LangChain, PromptLayer, Humanloop | Hard-stop: no inline prompt strings |
| Type-safe template data | TypeScript/Python typing best practice | Mandatory pattern |
| Template caching | Performance best practice | Mandatory pattern |
| Input sanitization | OWASP LLM Top 10 (LLM01: Prompt Injection) | Hard-stop rule |
| Prompt-as-files | Maintainability best practice | Hard-stop rule |
| Persona/role separation | System prompt patterns | Mandatory pattern |
| Prompt versioning | MLOps, PromptLayer | Recommended pattern |
| Prompt testing framework | PromptFoo, DeepEval, Humanloop | Recommended pattern |
| Prompt registry/catalog | Enterprise patterns (Humanloop, PromptLayer) | Recommended pattern |
| Token counting pre-render | Cost control best practice | Recommended pattern |
| Prompt composition (chaining) | LangChain LCEL, DSPy | Mandatory pattern |
| A/B prompt testing | Experimentation best practice | Future enhancement |

### Gaps Beyond BluePearl Reference (to address in constitution)

| Gap | Priority | Approach |
|-----|----------|----------|
| Prompt testing framework | High | Add PromptFoo/DeepEval integration for expected output assertions |
| Explicit prompt version tags | Medium | Add version metadata to template files or companion manifest |
| Token counting pre-render | Medium | Add tiktoken/tokenizer integration to estimate cost before LLM call |
| Prompt registry/catalog | Low | Add metadata DB or manifest file for template discovery and documentation |
| A/B prompt testing | Low | Add random variant selection with metrics tracking |
| Multi-language template support | Low | Add Jinja2 (Python) and Mustache patterns alongside Handlebars |
| Prompt diff tooling | Low | Add side-by-side prompt version comparison for review |

---

## 5. Constitution Structure Plan

### Hard-Stop Rules (non-negotiable)

1. **No inline prompt strings** — All prompts must be external files (templates or static markdown); never embedded in code
2. **Input sanitization on every render** — All user-provided template variables must pass through sanitization (null bytes, control chars, length truncation)
3. **Type-safe template data** — Every template must have a corresponding typed data interface; no `any` or untyped variable bags
4. **Prompt files read-only in production** — Template files must have restricted permissions (440 or lower); never writable at runtime
5. **User content as data, never as prompt** — User workspace files loaded as context data variables, never concatenated into system prompt fragments
6. **Isolated template instance** — No global template engine state; each engine instance is independent

### Mandatory Patterns

1. Template engine setup (isolated instance, `noEscape` for LLM context)
2. Type-safe template name registry (union type, compile-time validation)
3. Multi-path template resolution (env var → relative → absolute chain)
4. Template caching layer (Map or LRU)
5. Input sanitization pipeline (null bytes → control chars → truncation)
6. Prompt file system layout (`system/`, `templates/`, `persona/`)
7. Prompt composition (base + mode-specific append + persona + phase context)
8. Custom helper registration
9. Prompt specification document per template
10. Persona file system (multi-file profile structure)

### Recommended Patterns

1. Prompt testing harness (expected output assertions)
2. Prompt version tags / metadata
3. Token counting pre-render
4. Prompt catalog documentation generator
5. Template variable documentation (auto-extracted from typed interfaces)
6. Prompt diff/review tooling

---

## 6. Workflow Plan

| Workflow | Purpose | Key Deliverables |
|----------|---------|-----------------|
| **scaffold** | Full prompt system from scratch | Template engine with type-safe registry, multi-path resolution, caching, sanitization pipeline, file system layout (`system/`, `templates/`, `persona/`), typed data interfaces, custom helpers, 3 example templates, prompt specification doc, persona file structure |
| **compare** | Compare prompt management approaches | Side-by-side of Handlebars vs Jinja2 vs Mustache vs LangChain PromptTemplate vs DSPy signatures vs raw string interpolation |
| **refactor** | Improve existing prompt system | Audit inline strings → extract to files, add type safety, add sanitization, add caching, restructure directory layout |
| **test** | Prompt quality + injection tests | Sanitization validation (null bytes, control chars, overlength), type interface coverage, prompt injection attack tests, template rendering correctness tests |
| **debug** | Fix prompt issues | Template not found (path resolution), variable undefined (type mismatch), prompt injection discovered, caching stale, persona not loading |
| **document** | Generate prompt catalog docs | Visual token catalog per template, variable reference table, composition diagram, persona file documentation |

---

## 7. Keyword Differentiation from `responsible-prompting`

| Query | Expected Route | Rationale |
|-------|---------------|-----------|
| "Build a prompt template system" | `prompt-template-engineer` | Core capability |
| "Check my prompts for bias" | `responsible-prompting` | Ethical content |
| "Add type safety to my prompts" | `prompt-template-engineer` | Engineering pattern |
| "Create a persona file system" | `prompt-template-engineer` | Persona architecture |
| "Prevent prompt injection" | `prompt-template-engineer` | Sanitization engineering |
| "Ensure AI fairness in prompts" | `responsible-prompting` | Ethical evaluation |
| "Set up Handlebars for my prompts" | `prompt-template-engineer` | Template engine |
| "Test my prompt outputs" | `prompt-template-engineer` | Prompt testing |
| "Add safety guardrails to AI" | `responsible-prompting` | Content safety |
| "Version control my prompts" | `prompt-template-engineer` | Versioning |
| "Create a prompt catalog" | `prompt-template-engineer` | Prompt registry |

**Routing conflict risk**: LOW — keywords are distinct (`prompt-template`, `template-engine`, `sanitization`, `type-safe-prompts`, `prompt-catalog` vs `responsible-prompting`'s `bias`, `fairness`, `safety`, `guardrails`).

---

## 8. Implementation Approach

### Phase 1: Constitution

1. Read BluePearl reference implementation files (template-engine.ts, template-data-types.ts, prompt-reference.md, system/ and templates/ directories)
2. Extract 6 hard-stop rules from operational experience
3. Define 10 mandatory patterns with code templates (TypeScript primary, Python secondary)
4. Incorporate industry gaps (prompt testing, versioning, token counting)
5. Create refusal template for anti-patterns (inline strings, untyped variables, unsanitized input)

### Phase 2: Workflows

1. **scaffold** first — most complex, establishes all deliverables (engine, types, files, persona, examples)
2. **test** second — validates scaffold output (sanitization tests, type coverage, injection tests)
3. **refactor** third — most common real-world use case (extracting inline prompts to files)
4. **compare**, **debug**, **document** — follow standard patterns

### Phase 3: Validation

1. Run scaffold on a fresh TypeScript project
2. Verify all deliverables produced: engine, type interfaces, file layout, 3 example templates, persona structure, spec doc
3. Run test workflow to validate sanitization pipeline
4. Run refactor workflow on a project with inline prompt strings

---

## 9. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Language coupling (TypeScript Handlebars focus) | Medium | Provide Jinja2 (Python) and Mustache alternatives; patterns are language-agnostic |
| Overlap with `responsible-prompting` on injection | Low | Clear scope: PTE handles sanitization engineering; RP handles content ethics |
| Template engine choice becoming outdated | Low | Focus on patterns (caching, typing, resolution) not specific engine APIs |
| Over-engineering for simple projects | Medium | Provide "minimal" scaffold variant with just file layout + basic sanitization |
| Prompt testing tools rapidly evolving | Low | Reference patterns (assertions, regression) rather than specific tools |

---

*This document guides the creation of the `prompt-template-engineer` archetype. Review and approve before proceeding with constitution and workflow authoring.*
