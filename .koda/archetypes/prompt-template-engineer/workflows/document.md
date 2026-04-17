---
description: Generate comprehensive token documentation including visual catalog, contrast ratio tables, usage examples, and architecture guides
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read documentation context from:
`${ARCHETYPES_BASEDIR}/prompt-template-engineer/prompt-template-engineer-constitution.md`

Focus on Section II (Mandatory Patterns) for system components and Section VII (Related Documents) for reference files.

### 2. Identify Documentation Scope

Extract from $ARGUMENTS:

| Parameter | Description | Default |
|-----------|-------------|---------|
| **Target path** | Path to the prompt system | Auto-detect |
| **Doc output** | Where to write documentation | `docs/prompts/` |
| **Doc scope** | Full docs or specific section | Full |
| **Format** | Markdown, HTML, or both | Markdown |

### 3. Generate Architecture Overview

Create an architecture document showing the prompt system components and data flow:

**File**: `{doc_output}/architecture.md`

**Content:**

```text
# Prompt System Architecture

## Component Diagram

┌─────────────────────────────────────────────────────────────────┐
│                    Application Code                              │
│                                                                  │
│   renderTemplate('intent-classifier', data)                      │
│         │                                                        │
│         ▼                                                        │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              Template Engine Module                       │   │
│   │                                                          │   │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │   │
│   │  │  Sanitize     │→│  Resolve     │→│  Compile     │   │   │
│   │  │  (Rule 1.2)   │  │  (Pattern 2.3)│  │  + Cache    │   │   │
│   │  └──────────────┘  └──────────────┘  │  (Pattern 2.4)│   │   │
│   │                                       └──────┬───────┘   │   │
│   │                                              │            │   │
│   │                                       ┌──────▼───────┐   │   │
│   │                                       │   Render     │   │   │
│   │                                       │  (noEscape)  │   │   │
│   │                                       └──────────────┘   │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

## File System Layout

prompts/
├── system/           ← Static base prompts (base.md, append-*.md)
├── templates/        ← Parameterized .hbs templates (18 files)
└── persona/          ← User-editable identity layers (7 files per profile)
```

Include:

- Data flow from `renderTemplate()` call through sanitization → resolution → cache → compile → render
- File system layout with directory purposes
- Composition order for system prompts (base → append → persona → phase → skill)
- Security boundaries (sanitization, read-only files, isolated instance)

### 4. Generate Template Catalog

Create a visual catalog documenting every template:

**File**: `{doc_output}/template-catalog.md`

**For each template, document:**

| Field | Content |
|-------|---------|
| **Template name** | Matches `TemplateName` union type |
| **File path** | Relative path to the `.hbs` file |
| **Purpose** | What the prompt instructs the LLM to do |
| **Model tier** | Which purpose slot (think, quick, code, etc.) |
| **Data interface** | Interface name with field listing |
| **Required fields** | Fields that must be provided |
| **Optional fields** | Fields that may be omitted |
| **Helpers used** | Custom helpers referenced in the template |
| **Output format** | Expected LLM response format (JSON, markdown, free text) |
| **Token estimate** | Approximate rendered size |
| **Skip conditions** | When this template should not be rendered |

**Example entry:**

```text
## intent-classifier

| Property | Value |
|----------|-------|
| File | `templates/intent-classifier.hbs` |
| Purpose | Classify user message as "chat" or "plan" |
| Model tier | QUICK |
| Interface | `IntentClassifierData` |
| Output | JSON: `{ "mode": "chat"|"plan", "confidence": "high"|"medium"|"low" }` |
| Token est. | ~150 tokens |

### Data Interface

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| availableSkills | string[] | No | List of available archetype skills |

### Helpers Used

None

### Template Preview

(First 10 lines of the template)
```

### 5. Generate Variable Reference

Create a comprehensive reference of all template variables:

**File**: `{doc_output}/variable-reference.md`

**For each typed data interface, generate:**

```text
## PhaseEvaluatorData

Used by: `phase-evaluator.hbs`

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| phaseId | string | Yes | Unique phase identifier |
| phaseInstruction | string | Yes | What the phase was supposed to do |
| output | string | Yes | Raw sub-agent output to evaluate |
| phaseResult | string | Yes | Structured phase execution result |
| turnsUsed | number | Yes | Number of conversation turns used |
| duration | number | Yes | Phase execution time in milliseconds |
| iteration | number | Yes | Current evaluation iteration (1-based) |
| maxIterations | number | Yes | Maximum allowed iterations |
| explicitWrites | number | No | Count of file write/edit tool calls |
| fileOps | number | No | Count of all file-mutating tool calls |
```

### 6. Generate Sanitization Documentation

Create documentation for the sanitization pipeline:

**File**: `{doc_output}/sanitization.md`

**Content:**

- What is sanitized and why (OWASP LLM01 reference)
- The sanitization pipeline steps (null bytes → control chars → truncation)
- Character ranges preserved vs stripped
- `MAX_INTERPOLATION_LENGTH` configuration
- Recursive behavior for nested objects and arrays
- Examples of adversarial inputs and how they are neutralized
- Integration point (`renderTemplate` calls `sanitizeData` before every render)

### 7. Generate Persona System Documentation

If the persona system exists, document it:

**File**: `{doc_output}/persona-system.md`

**Content:**

- Purpose of the persona system (user-customizable identity)
- Profile directory structure (`profiles/{profile-name}/`)
- File-by-file documentation (IDENTITY.md, SOUL.md, USER.md, etc.)
- How persona files are loaded into the system prompt
- How to create custom profiles
- Composition order (alphabetical sort → section separators → injection into template)
- Security considerations (persona files as data variables, not system prompt fragments)

### 8. Generate Helper Function Reference

Document all registered template helpers:

**File**: `{doc_output}/helpers.md`

**For each helper:**

| Helper | Signature | Purpose | Example Usage |
|--------|-----------|---------|---------------|
| `eq` | `(a, b) → boolean` | Equality comparison | `{{#if (eq purpose "think")}}` |
| `add` | `(a, b) → number` | Addition | `Phase {{add phaseIndex 1}} of {{totalPhases}}` |
| `gt` | `(a, b) → boolean` | Greater-than | `{{#if (gt turnsUsed 5)}}` |
| `formatDuration` | `(ms) → string` | Time formatting | `{{formatDuration duration}}` → "2.3s" |
| `toLocaleString` | `(n) → string` | Number formatting | `{{toLocaleString totalTokens}}` → "1,234" |

### 9. Generate Configuration Reference

Document all configurable parameters:

**File**: `{doc_output}/configuration.md`

| Parameter | Default | Environment Variable | Description |
|-----------|---------|---------------------|-------------|
| Prompts directory | Auto-resolved | `BLUEPEARL_PROMPTS_DIR` | Root directory for prompt files |
| Max interpolation length | 10,000 | — | Maximum string length before truncation |
| HTML escape | Disabled | — | `noEscape: true` for LLM context |
| Cache strategy | Map (unbounded) | — | Compiled template cache |
| Template extension | `.hbs` | — | File extension for template lookup |
| Persona directory | `profiles/default/` | — | Path to active profile |

### 10. Generate Quick Start Guide

Create a getting-started document:

**File**: `{doc_output}/quickstart.md`

**Content:**

1. How to render a template (`renderTemplate('name', data)`)
2. How to add a new template (create file, add interface, register name)
3. How to modify an existing template (edit file, clear cache in dev)
4. How to add a custom helper (register on isolated instance)
5. How to create a custom persona profile (copy default, edit files)
6. Common pitfalls (stale cache, missing `noEscape`, untyped data)

---

## Error Handling

**No Prompt System Found**: If the target path has no prompt system, generate documentation templates with placeholder content and notes about what each section would contain after scaffolding.

**Partial Documentation**: If some documentation already exists, merge with existing content rather than overwriting. Flag sections that need updating.

**Large Template Count**: If there are more than 20 templates, generate the catalog in batches and include a summary table at the top for quick navigation.

## Examples

### Example 1: Full Documentation Suite
```text
/document-prompt-template-engineer "
Generate complete documentation for our prompt system.
Engine is in src/prompt/, templates in service/prompts/.
Output docs to docs/prompts/. Include architecture, catalog,
variable reference, and sanitization docs.
"
```

### Example 2: Template Catalog Only
```text
/document-prompt-template-engineer "
Generate just the template catalog for our 18 Handlebars
templates in service/prompts/templates/. Include data
interfaces, helpers used, and token estimates.
"
```

### Example 3: Security Documentation
```text
/document-prompt-template-engineer "
Generate security-focused documentation for our prompt system:
sanitization pipeline, file permissions, injection resistance,
and user content boundaries. For security audit compliance.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/prompt-template-engineer/prompt-template-engineer-constitution.md` Sections II, V, VII
- **Related**: scaffold-prompt-template-engineer, test-prompt-template-engineer
