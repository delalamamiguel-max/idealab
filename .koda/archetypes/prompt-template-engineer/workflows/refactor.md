---
description: Audit and improve an existing prompt management system by extracting inline strings to files, adding type safety, sanitization, caching, and restructuring directory layout
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

### 2. Inventory Current Prompt System

Scan the codebase to build a complete picture of the existing prompt landscape:

**2.1 Find all inline prompt strings:**

Search for multi-line strings containing LLM instructions:

```text
Patterns to search:
- Template literals with prompt content (backtick strings > 3 lines)
- f-strings / format strings with "You are" / "Analyze" / "Return JSON"
- String constants named *prompt*, *instruction*, *system*
- String concatenation building prompts (a + b + c)
```

**2.2 Find existing template files:**

Search for template files that may already exist:

```text
Extensions: .hbs, .handlebars, .j2, .jinja2, .mustache, .txt, .md
Directories: prompts/, templates/, prompt-templates/
```

**2.3 Check for sanitization:**

Search for any existing input sanitization:

```text
Patterns: sanitize, escape, strip, replace(/[\x00, clean, purify
```

**2.4 Check for type safety:**

Search for typed template data:

```text
Patterns: TemplateData, PromptData, interface.*Data, TypedDict, dataclass
```

**2.5 Generate inventory report:**

```text
PROMPT SYSTEM INVENTORY
───────────────────────────────────────────

Inline Prompt Strings:     {count} found
  - {file}:{line} — {preview} ({length} chars)
  - {file}:{line} — {preview} ({length} chars)
  ...

Existing Template Files:   {count} found
  - {path} ({size} bytes)
  ...

Sanitization:              {present/absent}
  - {location if present}

Type Safety:               {present/absent}
  - {location if present}

Template Caching:          {present/absent}
Template Engine:           {name or "none"}
Persona System:            {present/absent}
Prompt Spec Document:      {present/absent}
```

### 3. Identify Hard-Stop Violations

Check each hard-stop rule against the inventory:

| Rule | Violation | Files Affected |
|------|-----------|---------------|
| 1.1 No inline prompt strings | List all inline strings found | {files} |
| 1.2 Input sanitization on every render | Missing sanitization paths | {files} |
| 1.3 Type-safe template data | Untyped template calls | {files} |
| 1.4 Prompt files read-only | Writable template permissions | {files} |
| 1.5 User content as data | String concatenation of user content | {files} |
| 1.6 Isolated template instance | Global engine state usage | {files} |

### 4. Build Prioritized Refactoring Plan

Organize fixes into three priority levels:

**P1 — Hard-Stop Violations (fix immediately):**

1. Extract inline prompts to template files (Rule 1.1)
2. Add sanitization pipeline to all render paths (Rule 1.2)
3. Fix user content concatenation — move to template data (Rule 1.5)
4. Isolate template engine instance (Rule 1.6)

**P2 — Missing Mandatory Patterns (fix next):**

5. Add type-safe template name registry (Pattern 2.2)
6. Add typed data interfaces per template (Pattern 2.3 / Rule 1.3)
7. Add multi-path template resolution (Pattern 2.3)
8. Add template caching layer (Pattern 2.4)
9. Restructure directory layout (Pattern 2.6)
10. Add prompt composition pattern (Pattern 2.7)

**P3 — Recommended Improvements (fix when possible):**

11. Add prompt specification document (Pattern 2.9)
12. Add persona file system (Pattern 2.10)
13. Add sanitization tests (Pattern 3.1)
14. Add prompt version tags (Pattern 3.2)
15. Add token counting pre-render (Pattern 3.3)

### 5. Execute P1 Refactoring — Extract Inline Prompts

For each inline prompt string found:

**Step 5.1**: Create the template file:

1. Determine template name from the function/context (e.g., `classifyIntent` → `intent-classifier`)
2. Create `templates/{template-name}.hbs` with the prompt content
3. Replace hardcoded variable interpolations with template syntax (`{{variable}}`)
4. Add conditional blocks for optional sections (`{{#if variable}}`)
5. Add version comment at top of template file

**Step 5.2**: Create the typed data interface:

1. Extract all variables referenced in the template
2. Create a TypeScript interface (or Python TypedDict) with proper types
3. Mark optional fields with `?` or `Optional[]`

**Step 5.3**: Replace the inline string with a `renderTemplate` call:

```typescript
// BEFORE:
const prompt = `You are a classifier. Skills: ${skills.join(', ')}`;

// AFTER:
import { renderTemplate } from './template-engine';
const prompt = renderTemplate('intent-classifier', { availableSkills: skills });
```

**Step 5.4**: Add the template name to the `TemplateName` registry.

### 6. Execute P1 Refactoring — Add Sanitization

If no sanitization exists:

1. Create the `sanitizeValue` / `sanitizeData` functions (Pattern 2.5)
2. Wire sanitization into the `renderTemplate` function
3. Set `MAX_INTERPOLATION_LENGTH` (default: 10,000)
4. Add sanitization tests (at minimum: null bytes, control chars, overlength)

If partial sanitization exists:

1. Audit existing sanitization for completeness
2. Add missing steps (null bytes? control chars? length truncation? recursive?)
3. Ensure sanitization runs on ALL render paths, not just some

### 7. Execute P2 Refactoring — Restructure and Add Patterns

**7.1 Directory restructure:**

Move existing template files into the standard layout:

```text
prompts/
├── system/       # Base system prompts
├── templates/    # Parameterized templates
└── persona/      # User-editable persona files (if applicable)
```

Update all file references to use new paths.

**7.2 Add template caching:**

If the engine compiles templates on every render, add a `Map<string, CompiledTemplate>` cache.

**7.3 Add multi-path resolution:**

If templates are loaded from a single hardcoded path, add the env var → relative → absolute fallback chain.

**7.4 Add prompt composition:**

If system prompts are built by string concatenation, refactor to use the layered composition pattern (base + append + persona).

### 8. Validate Refactoring

After all changes:

1. **Type check** — Run `tsc --noEmit` (TypeScript) or `mypy` (Python) to verify type safety
2. **Render test** — Render every template with sample data and verify output
3. **Sanitization test** — Run injection tests with adversarial input
4. **Functional test** — Verify the application still produces correct LLM outputs
5. **Regression check** — Compare rendered prompts before/after refactoring to ensure no unintended changes

### 9. Generate Refactoring Report

```text
PROMPT SYSTEM REFACTORING REPORT
═══════════════════════════════════════════════════

BEFORE                              AFTER
───────────────────────────────────────────────────
Inline prompt strings:  {N}         Template files: {N}
Sanitization:           {Y/N}       Sanitization:   ✅
Type safety:            {Y/N}       Type safety:    ✅
Template caching:       {Y/N}       Template caching: ✅
Prompt composition:     {Y/N}       Prompt composition: ✅

HARD-STOP COMPLIANCE
───────────────────────────────────────────────────
Rule 1.1 No inline strings:    ✅ {N} strings extracted
Rule 1.2 Sanitization:         ✅ Pipeline active on all paths
Rule 1.3 Type-safe data:       ✅ {N} interfaces created
Rule 1.4 Read-only files:      ✅ Permissions documented
Rule 1.5 User content as data: ✅ No concatenation
Rule 1.6 Isolated instance:    ✅ {engine}.create()

FILES MODIFIED: {count}
FILES CREATED:  {count}
```

---

## Error Handling

**Large Codebase**: If there are more than 20 inline prompt strings, batch the extraction into groups of 5 and validate after each batch.

**Mixed Languages**: If the project uses both TypeScript and Python, create separate template engines for each but share the same template files (Handlebars templates work for TS; create Jinja2 equivalents for Python).

**Existing Template Engine**: If the project already uses a template engine (but without sanitization/typing), refactor incrementally — add sanitization first, then typing, then caching.

**Breaking Changes**: Track all import/function signature changes in a migration guide so other developers can update their code.

## Examples

### Example 1: Extract Inline Prompts
```text
/refactor-prompt-template-engineer "
Our TypeScript AI service has ~15 inline prompt strings scattered
across src/ai/. Extract them all to Handlebars templates with
type-safe interfaces and sanitization. Keep the same directory
structure but add prompts/ at the root.
"
```

### Example 2: Add Sanitization to Existing System
```text
/refactor-prompt-template-engineer "
We already use Handlebars templates in templates/ but have no
input sanitization. A security audit flagged prompt injection
risk. Add sanitization to all render paths.
"
```

### Example 3: Full System Modernization
```text
/refactor-prompt-template-engineer "
Our prompt system is a mess — inline strings, no types, no caching,
global Handlebars instance. Do a full refactor to bring it up to
constitution compliance. TypeScript, Handlebars.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/prompt-template-engineer/prompt-template-engineer-constitution.md` Sections I, II
- **Related**: scaffold-prompt-template-engineer, test-prompt-template-engineer
