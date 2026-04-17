---
description: Generate a complete prompt management system with template engine, type-safe registry, multi-path resolution, caching, sanitization pipeline, prompt-as-files layout, persona file structure, and prompt specification documentation
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read all rules and patterns from:
`${ARCHETYPES_BASEDIR}/prompt-template-engineer/prompt-template-engineer-constitution.md`

Focus on Section I (Hard-Stop Rules 1.1–1.6) and Section II (Mandatory Patterns 2.1–2.10).

### 2. Gather Requirements

Extract from $ARGUMENTS:

| Requirement | Description | Default |
|------------|-------------|---------|
| **Language** | TypeScript, Python, or other | TypeScript |
| **Template engine** | Handlebars, Jinja2, Mustache, or custom | Handlebars |
| **Project path** | Where to scaffold the prompt system | `src/prompt/` |
| **Prompts directory** | Where template and system files live | `prompts/` |
| **Max interpolation length** | Truncation limit for sanitization | 10,000 |
| **Persona support** | Whether to generate persona file system | Yes |
| **Template count** | Number of example templates to generate | 3 |
| **Prompt spec doc** | Whether to generate prompt specification document | Yes |

### 3. Generate Template Engine Module

Create the core template engine with all mandatory patterns:

**File**: `{project_path}/template-engine.ts` (or `.py`)

**Must include** (constitution compliance):

- [ ] Isolated engine instance — `Handlebars.create()` or `jinja2.Environment()` (Rule 1.6)
- [ ] `noEscape: true` or `autoescape=False` (Pattern 2.1)
- [ ] Multi-path resolution function with env var → relative → absolute chain (Pattern 2.3)
- [ ] Template cache via `Map<string, CompiledTemplate>` (Pattern 2.4)
- [ ] `sanitizeValue` recursive function: null bytes → control chars → truncation (Pattern 2.5)
- [ ] `sanitizeData` wrapper for object-level sanitization
- [ ] `renderTemplate<T>(name: TemplateName, data: T)` public API (Pattern 2.1)
- [ ] `loadSystemPrompt(append?: string)` for base + mode-specific prompt loading
- [ ] `clearTemplateCache()` for development hot-reload (Pattern 3.7)
- [ ] Custom helper registration on isolated instance (Pattern 2.8)

**Custom helpers to register:**

| Helper | Signature | Purpose |
|--------|-----------|---------|
| `eq` | `(a, b) => a === b` | Equality in conditionals |
| `add` | `(a, b) => a + b` | Arithmetic (phase indexing) |
| `gt` | `(a, b) => a > b` | Greater-than comparison |
| `formatDuration` | `(ms) => string` | Human-readable time |
| `toLocaleString` | `(n) => string` | Number formatting |

### 4. Generate Type-Safe Template Data Interfaces

Create typed data interfaces for each template:

**File**: `{project_path}/template-data-types.ts` (or `.py` with dataclasses/TypedDict)

**Must include** (constitution compliance):

- [ ] One interface per template (Rule 1.3)
- [ ] All fields typed — no `any` or `unknown` for template variables
- [ ] Optional fields marked with `?` (TypeScript) or `Optional[]` (Python)
- [ ] JSDoc/docstring comments for non-obvious fields
- [ ] Export all interfaces for consumer use

**For each example template, generate:**

```typescript
// Example: intent-classifier template data
export interface IntentClassifierData {
  availableSkills?: string[];
}

// Example: system-prompt template data
export interface SystemPromptData {
  skills: Array<{ name: string; category: string; description: string }>;
  sessionName?: string;
  profileName?: string;
  modelId?: string;
}
```

### 5. Generate Type-Safe Template Name Registry

Add a union type of all valid template names:

**In template engine module:**

```typescript
export type TemplateName =
  | 'system-prompt'
  | 'intent-classifier'
  | 'task-planner';
  // ... one entry per template file

// compileTemplate accepts ONLY valid template names
function compileTemplate(name: TemplateName): Handlebars.TemplateDelegate { ... }
```

### 6. Generate Prompt File System Layout

Create the directory structure (Pattern 2.6):

```text
{prompts_directory}/
├── system/
│   ├── base.md                    # Core identity and principles
│   ├── append-coding.md           # Mode-specific coding context
│   └── append-working.md          # Mode-specific working context
├── templates/
│   ├── {template-1}.hbs           # First example template
│   ├── {template-2}.hbs           # Second example template
│   └── {template-3}.hbs           # Third example template
└── persona/ (if persona support enabled)
    └── default/
        ├── IDENTITY.md
        ├── SOUL.md
        ├── USER.md
        ├── TOOLS.md
        ├── AGENTS.md
        ├── MEMORY.md
        └── BOOTSTRAP.md
```

**For each system file**, generate meaningful starter content appropriate to the project domain.

**For each template file**, generate a complete Handlebars/Jinja2 template with:

- Version comment at top
- Clear section structure
- Conditional blocks for optional data
- Usage of registered helpers where appropriate

### 7. Generate System Prompt Builder

Create the prompt composition module (Pattern 2.7):

**File**: `{project_path}/system-prompt.ts` (or `.py`)

**Must include:**

- [ ] `buildSystemPrompt(config)` function
- [ ] Base prompt loading from `system/base.md`
- [ ] Mode-specific append loading (coding, working, etc.)
- [ ] Persona file loading from profile directory
- [ ] Alphabetical sorting of persona files
- [ ] Section separators between persona layers (`--- FILENAME ---`)
- [ ] Graceful fallback if persona directory is missing

### 8. Generate Persona File System (if enabled)

Create the default profile with 7 persona files (Pattern 2.10):

| File | Content to Generate |
|------|-------------------|
| `IDENTITY.md` | Agent identity — name, pronouns, role, tone |
| `SOUL.md` | Core values and emotional foundation |
| `USER.md` | Placeholder for user information |
| `TOOLS.md` | Tool usage guidelines |
| `AGENTS.md` | Sub-agent delegation rules |
| `MEMORY.md` | Persistent context placeholder |
| `BOOTSTRAP.md` | First-run initialization instructions |

Each file should contain meaningful starter content, not empty placeholders.

### 9. Generate Example Templates

Create 3 example templates demonstrating different patterns:

**Template 1 — Simple classifier** (minimal data, JSON output):

```handlebars
{{!-- version: 1.0.0 --}}
You are a classifier. Analyze the input and return JSON.

{{#if availableSkills.length}}
Available skills: {{#each availableSkills}}{{this}}{{#unless @last}}, {{/unless}}{{/each}}
{{/if}}

Respond with ONLY a JSON object.
```

**Template 2 — Complex evaluator** (rich data, conditional blocks, helpers):

```handlebars
{{!-- version: 1.0.0 --}}
Evaluate the output of Phase {{add phaseIndex 1}} of {{totalPhases}}.

## Instruction
{{{instruction}}}

## Output to Evaluate
{{{output}}}

{{#if (gt turnsUsed 5)}}
⚠️ This phase used {{turnsUsed}} turns, which is above average.
{{/if}}

Duration: {{formatDuration duration}}
```

**Template 3 — System prompt** (persona integration, conditional sections):

A complete system prompt template with conditional persona blocks, skill listing, and session state.

### 10. Generate Prompt Specification Document

Create a specification document for all generated templates:

**File**: `{prompts_directory}/PROMPT_SPEC.md`

**For each template, document:**

| Field | Content |
|-------|---------|
| Template name | Matches `TemplateName` entry |
| Purpose | What the prompt instructs the LLM to do |
| Model tier | Which model purpose slot (think, quick, code, etc.) |
| Data interface | Interface name and link to type definition |
| Output format | Expected LLM output format |
| Skip conditions | When the template should not be rendered |
| Token estimate | Approximate rendered token count |

### 11. Generate Sanitization Tests

Create a test file validating the sanitization pipeline:

**File**: `{project_path}/__tests__/sanitization.test.ts` (or `test_sanitization.py`)

**Test cases:**

- [ ] Null bytes stripped from strings
- [ ] Control characters removed (preserving `\n`, `\t`, `\r`)
- [ ] Overlength strings truncated with `… [truncated]` suffix
- [ ] Nested objects sanitized recursively
- [ ] Arrays sanitized element-by-element
- [ ] Numbers, booleans, null pass through unchanged
- [ ] Adversarial prompt injection attempt is neutralized

### 12. Post-Scaffold Checklist

Verify all mandatory components were generated:

**Core Components:**

- [ ] Template engine module with isolated instance
- [ ] Type-safe template name registry (union type or enum)
- [ ] Typed data interfaces (one per template)
- [ ] Multi-path template resolution
- [ ] Template caching layer
- [ ] Input sanitization pipeline
- [ ] System prompt builder with composition pattern
- [ ] `clearTemplateCache()` function

**File System:**

- [ ] `system/` directory with base.md and append files
- [ ] `templates/` directory with example templates
- [ ] `persona/` directory with default profile (if enabled)

**Documentation:**

- [ ] Prompt specification document (PROMPT_SPEC.md)
- [ ] Sanitization test file

**Hard-Stop Rule Compliance:**

- [ ] No inline prompt strings in generated code (Rule 1.1)
- [ ] Sanitization runs on every `renderTemplate` call (Rule 1.2)
- [ ] Every template has a typed data interface (Rule 1.3)
- [ ] File permissions guidance included (Rule 1.4)
- [ ] User content loaded as data variables (Rule 1.5)
- [ ] Isolated engine instance (Rule 1.6)

---

## Error Handling

**Missing Template Engine Library**: If Handlebars/Jinja2 is not installed, provide installation instructions and add to the project's dependency file.

**TypeScript vs Python**: Adapt all code patterns to the target language. TypeScript uses Handlebars with `TemplateName` union types; Python uses Jinja2 with `TemplateName` enum and `TypedDict` data classes.

**Existing Prompt System**: If the project already has prompts, ask whether to migrate existing prompts into the new structure or generate alongside them.

## Examples

### Example 1: Full TypeScript Prompt System
```text
/scaffold-prompt-template-engineer "
Create a complete prompt management system for our TypeScript
AI agent. We need Handlebars templates with type-safe data
interfaces, sanitization, and a persona file system. Place
the engine in src/prompt/ and templates in service/prompts/.
"
```

### Example 2: Python Minimal Setup
```text
/scaffold-prompt-template-engineer "
Set up a Jinja2 prompt system for our Python FastAPI service.
Minimal setup — just the engine, sanitization, and 3 example
templates. No persona system needed. Target: src/prompts/.
"
```

### Example 3: Add to Existing Project
```text
/scaffold-prompt-template-engineer "
We have inline prompts scattered across our codebase. Create
the prompt infrastructure (engine, types, file layout) so we
can migrate prompts out of code. TypeScript, Handlebars.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/prompt-template-engineer/prompt-template-engineer-constitution.md` Sections I, II
- **Related**: refactor-prompt-template-engineer, test-prompt-template-engineer
