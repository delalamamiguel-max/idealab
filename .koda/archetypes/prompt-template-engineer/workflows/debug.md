---
description: Debug prompt template system failures including template resolution errors, variable undefined issues, prompt injection discoveries, caching staleness, and persona loading problems
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read troubleshooting context from:
`${ARCHETYPES_BASEDIR}/prompt-template-engineer/prompt-template-engineer-constitution.md`

Focus on Section IV (Troubleshooting Guide) and Section I (Hard-Stop Rules) for violation detection.

### 2. Classify Failure

Determine the failure category from $ARGUMENTS:

| Priority | Failure Category | Symptoms |
|----------|-----------------|----------|
| **P0** | Prompt injection detected | LLM ignoring system instructions, unexpected behavior |
| **P0** | Template engine crash | Unhandled exception in `renderTemplate`, application down |
| **P1** | Template not found | `Error: Prompt template not found: /path/to/template.hbs` |
| **P1** | Variable undefined | Empty sections in rendered prompt, missing data |
| **P1** | Sanitization bypass | User input appearing unsanitized in rendered prompt |
| **P2** | Stale cache | Template file changes not reflected in output |
| **P2** | HTML entity encoding | `&amp;`, `&lt;`, `&#x27;` appearing in prompts |
| **P2** | Persona not loading | Agent has no personality, generic responses |
| **P3** | Performance degradation | Slow template rendering, high memory usage |
| **P3** | Helper function error | Custom helper throwing exceptions |

### 3. Execute Diagnostic Procedure

#### 3.1 Prompt Injection Detected (P0)

**Symptoms**: LLM follows injected instructions instead of system prompt. Unexpected output patterns. User-submitted content appearing to override system behavior.

**Diagnostic steps:**

1. **Check sanitization pipeline** — Verify `sanitizeValue` runs on all template data:

   ```typescript
   // Add diagnostic logging before render
   console.log('[DIAG] Pre-sanitize data keys:', Object.keys(data));
   const sanitized = sanitizeData(data as Record<string, unknown>);
   console.log('[DIAG] Post-sanitize sample:', JSON.stringify(sanitized).slice(0, 200));
   ```

2. **Check for string concatenation bypasses** — Search for any code that concatenates user input into prompts outside the template engine:

   ```text
   Search patterns:
   - systemPrompt + userInput
   - `${systemPrompt}${userInput}`
   - prompt.replace(placeholder, userContent)
   - f"...{user_input}..." (Python)
   ```

3. **Check user content placement** — Verify Rule 1.5 compliance. User content must be template data variables, not system prompt fragments:

   ```text
   ✘ VIOLATION: const prompt = basePrompt + '\n' + userFile;
   ✔ CORRECT: renderTemplate('analyzer', { documentContent: sanitize(userFile) });
   ```

4. **Check MAX_INTERPOLATION_LENGTH** — If not set or too high, oversized payloads can push system instructions out of the context window.

5. **Verify template structure** — Ensure user data sections are clearly labeled in the template with boundaries the LLM can distinguish.

#### 3.2 Template Not Found (P1)

**Symptoms**: `Error: Prompt template not found: /path/to/templates/name.hbs`

**Diagnostic steps:**

1. **Verify file exists** at the expected path
2. **Check multi-path resolution** — Log which candidate paths are being tried:

   ```typescript
   console.log('[DIAG] PROMPTS_DIR resolved to:', PROMPTS_DIR);
   console.log('[DIAG] Looking for:', join(PROMPTS_DIR, 'templates', `${name}.hbs`));
   ```

3. **Check environment variable** — Is `BLUEPEARL_PROMPTS_DIR` (or equivalent) set correctly?
4. **Check file extension** — `.hbs` vs `.handlebars` vs `.j2` mismatch
5. **Check TemplateName registry** — Is the template name included in the union type?
6. **In containers** — Verify the COPY instruction includes the templates directory and the path matches the resolution chain

#### 3.3 Variable Undefined (P1)

**Symptoms**: Rendered prompt has empty sections where data should appear. No error thrown.

**Diagnostic steps:**

1. **Check typed interface** — Does the data object match the template's interface?

   ```typescript
   // Add type assertion to catch mismatches
   const data: PhaseEvaluatorData = {
     phaseId: 'p1',
     // TypeScript will show errors for missing required fields
   };
   ```

2. **Check template variable names** — Handlebars variables are case-sensitive. `{{PhaseId}}` ≠ `{{phaseId}}`
3. **Check optional field guards** — Templates should use `{{#if variable}}` for optional fields
4. **Add development-mode strict check**:

   ```typescript
   // Development mode: throw on undefined variables
   if (process.env.NODE_ENV === 'development') {
     hbs.registerHelper('helperMissing', function(/* args */) {
       throw new Error(`Missing template variable: ${arguments[arguments.length - 1].name}`);
     });
   }
   ```

#### 3.4 Stale Cache (P2)

**Symptoms**: Template file changes on disk not reflected in rendered output.

**Diagnostic steps:**

1. **Call `clearTemplateCache()`** — Most common fix
2. **Check if cache is being populated** — Add logging to `compileTemplate`:

   ```typescript
   console.log(`[DIAG] Template '${name}': ${templateCache.has(name) ? 'CACHE HIT' : 'CACHE MISS'}`);
   ```

3. **For development** — Implement file-watcher cache invalidation or disable caching entirely
4. **For production** — Templates should not change at runtime (Rule 1.4). If they are changing, that itself is a violation.

#### 3.5 Persona Not Loading (P2)

**Symptoms**: Agent has no personality, responds with generic defaults, persona-specific content missing.

**Diagnostic steps:**

1. **Check persona directory path** — Verify `personaDir` points to the correct profile directory
2. **Check file permissions** — Application process must be able to read `.md` files
3. **Check for empty files** — `buildSystemPrompt` skips files with empty `.trim()` result
4. **Check template conditional** — Verify `system-prompt.hbs` has `{{#if persona.identity}}` blocks
5. **Check profile resolution** — Is the correct profile being selected (default vs user-specific)?

### 4. Apply Fix

After identifying the root cause, apply the minimal fix:

1. **For P0 (injection)** — Add sanitization to the bypass path immediately. Then audit all render paths.
2. **For P1 (template not found)** — Fix the path resolution or add the missing template file.
3. **For P1 (variable undefined)** — Fix the data interface or add the missing field to the render call.
4. **For P2 (stale cache)** — Call `clearTemplateCache()` and add development-mode auto-invalidation.
5. **For P2 (persona)** — Fix the directory path or file permissions.

### 5. Verify Fix

After applying the fix:

1. **Re-render the template** with the same data that triggered the failure
2. **Run sanitization tests** if the fix involved the sanitization pipeline
3. **Run type checks** (`tsc --noEmit` or `mypy`) if the fix involved data interfaces
4. **Check for regression** — Ensure the fix does not break other templates

---

## Error Handling

**Multiple Failures**: If multiple failure categories are present, address P0 issues first (security), then P1 (functional), then P2/P3 (operational).

**Unknown Failure**: If the failure does not match any known category, add diagnostic logging to the `renderTemplate` function and capture the full render context (template name, data keys, resolved path, cache state).

**Framework-Specific Issues**: If the issue is specific to Handlebars/Jinja2/Mustache internals, consult the engine's documentation. Common pitfalls: Handlebars triple-stash vs double-stash, Jinja2 autoescaping, Mustache lambda scope.

## Examples

### Example 1: Template Not Found in Container
```text
/debug-prompt-template-engineer "
Our prompt system throws 'Prompt template not found: /opt/app/prompts/templates/task-planner.hbs'
in the container but works fine in development. The file exists in our source tree.
"
```

### Example 2: Prompt Injection Discovery
```text
/debug-prompt-template-engineer "
A user uploaded a document that caused our AI to ignore its system prompt and
follow instructions embedded in the document. We use renderTemplate for everything
but the uploaded file content is being concatenated directly.
"
```

### Example 3: Stale Templates in Development
```text
/debug-prompt-template-engineer "
I keep editing my .hbs template files but the rendered output doesn't change.
I have to restart the server every time. How do I fix the caching?
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/prompt-template-engineer/prompt-template-engineer-constitution.md` Section IV
- **Related**: test-prompt-template-engineer, refactor-prompt-template-engineer
