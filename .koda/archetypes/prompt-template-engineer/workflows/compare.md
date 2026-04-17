---
description: Compare prompt management approaches, template engines, and architecture patterns for prompt system design decisions
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read comparison context from:
`${ARCHETYPES_BASEDIR}/prompt-template-engineer/prompt-template-engineer-constitution.md`

Focus on Section II (Mandatory Patterns) for evaluation criteria.

### 2. Identify Comparison Scope

Determine what to compare from $ARGUMENTS:

| Comparison Type | What is Compared | Key Criteria |
|----------------|-----------------|--------------|
| **Template engine** | Handlebars vs Jinja2 vs Mustache vs Nunjucks vs custom | Type safety, helpers, logic-less, caching |
| **Architecture** | Prompt-as-files vs inline strings vs database-backed vs hybrid | Maintainability, version control, deployment |
| **Sanitization** | Regex pipeline vs library-based vs schema validation | Coverage, performance, false positives |
| **Caching** | Map vs LRU vs no-cache vs file-watcher | Memory, staleness, development experience |
| **Persona system** | Multi-file vs single-file vs database vs none | Flexibility, user editability, composability |
| **Prompt testing** | PromptFoo vs DeepEval vs custom assertions vs none | Coverage, CI integration, cost |

### 3. Build Comparison Matrix

For each option being compared, evaluate against these criteria:

**Architecture Criteria:**

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Type safety | Critical | Compile-time checks for template variables |
| Input sanitization | Critical | Prompt injection resistance |
| Template caching | High | Performance of repeated renders |
| Multi-path resolution | High | Works across dev, container, CI environments |
| Prompt-as-files | High | Templates in external files, not code |
| Persona support | Medium | User-customizable identity layers |
| Custom helpers | Medium | Application-specific template logic |
| Prompt composition | High | Layered assembly (base + append + persona) |
| HTML escape handling | Medium | Correct for LLM context (disable encoding) |
| Isolation | High | No global state contamination |

**Operational Criteria:**

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Language ecosystem | High | Native support in TypeScript/Python |
| Learning curve | Medium | Time to adopt for prompt engineers |
| Community / docs | Low | Available resources and examples |
| Testing integration | Medium | Ease of testing rendered prompts |
| Version control | Medium | Prompt change tracking in git |
| Token counting | Low | Pre-render cost estimation |
| A/B testing support | Low | Variant selection with metrics |

### 4. Pre-Built Comparison Tables

#### 4.1 Template Engine Comparison

| Feature | Handlebars | Jinja2 | Mustache | Nunjucks | Raw Strings |
|---------|-----------|--------|----------|----------|-------------|
| Language | JS/TS | Python | Any | JS/TS | Any |
| Logic-less | Yes (limited) | No (full logic) | Yes (strict) | No (full logic) | N/A |
| Isolated instance | `Handlebars.create()` | `jinja2.Environment()` | N/A (stateless) | `nunjucks.configure()` | N/A |
| Custom helpers | `registerHelper()` | Filters + extensions | Lambdas only | Filters + extensions | N/A |
| `noEscape` support | `{ noEscape: true }` | `autoescape=False` | Default (no escape) | `autoescape: false` | N/A |
| Conditional blocks | `{{#if}}` | `{% if %}` | `{{#section}}` | `{% if %}` | Ternary/if |
| Iteration | `{{#each}}` | `{% for %}` | `{{#list}}` | `{% for %}` | `.map()` |
| Compile + cache | Native | Native | Native | Native | N/A |
| Type safety (TS) | Via typed wrapper | N/A (Python) | Via typed wrapper | Via typed wrapper | Manual |
| Prompt injection risk | Low (with sanitize) | Low (with sanitize) | Low (with sanitize) | Low (with sanitize) | **High** |
| BluePearl alignment | **Full** | Good (Python) | Partial | Good | None |

#### 4.2 Architecture Comparison

| Strategy | Maintainability | Version Control | Deployment | Performance | Team Workflow |
|----------|----------------|-----------------|------------|-------------|---------------|
| Prompt-as-files (BluePearl) | Excellent | Git diffs per file | Deploy with app | Cache on first use | Prompt engineers edit files directly |
| Inline strings | Poor | Buried in code diffs | Deploy with app | No cache needed | Developers only |
| Database-backed | Good | DB versioning | Separate deploy | Query per render | Admin UI for editing |
| Hybrid (files + DB override) | Good | Files in git, overrides in DB | Two-step deploy | Cache with invalidation | Both teams |

#### 4.3 Sanitization Strategy Comparison

| Strategy | Coverage | Performance | False Positives | Complexity |
|----------|----------|-------------|----------------|------------|
| Regex pipeline (BluePearl) | Good (null, control, length) | Fast (O(n)) | Very low | Low |
| Schema validation (Zod/Pydantic) | Excellent (type + pattern) | Medium | Low | Medium |
| Library-based (DOMPurify etc.) | HTML-focused (wrong domain) | Medium | High for LLM | Low |
| No sanitization | None | Zero overhead | N/A | None |
| LLM-based detection | Variable | Slow (LLM call) | Medium | High |

#### 4.4 Persona System Comparison

| Strategy | Flexibility | User Editability | Composability | Complexity |
|----------|-------------|------------------|---------------|------------|
| Multi-file profiles (BluePearl) | Excellent | Edit individual aspects | Mix-and-match files | Medium |
| Single-file persona | Low | Edit entire persona at once | No mixing | Low |
| Database-backed fields | Good | Admin UI | Field-level composition | High |
| No persona system | None | Hardcoded identity | None | None |

### 5. Generate Recommendation

Based on the comparison matrix, produce a structured recommendation:

```text
## Prompt System Architecture Recommendation

**Recommended Approach**: {approach_name}

### Why This Approach

{2-3 sentences explaining the recommendation}

### Alignment with Constitution

| Hard-Stop Rule | Compliance |
|---------------|------------|
| 1.1 No inline prompt strings | {how approach satisfies it} |
| 1.2 Input sanitization | {how approach satisfies it} |
| 1.3 Type-safe template data | {how approach satisfies it} |
| 1.4 Read-only prompt files | {how approach satisfies it} |
| 1.5 User content as data | {how approach satisfies it} |
| 1.6 Isolated instance | {how approach satisfies it} |

### Trade-offs

| Advantage | Trade-off |
|-----------|-----------|
| {advantage_1} | {trade_off_1} |
| {advantage_2} | {trade_off_2} |

### Migration Path (if applicable)

{Steps to migrate from current approach to recommended approach}
```

---

## Error Handling

**Single Option Provided**: If the user provides only one approach, compare it against the BluePearl reference pattern and identify gaps.

**Non-Template Comparison**: If the comparison is about ethical prompt content or model evaluation, redirect to `responsible-prompting` or `language-model-evaluation`.

**Language Mismatch**: If comparing engines across languages (Handlebars vs Jinja2), note that the architectural patterns (caching, sanitization, typing, file layout) are language-agnostic — only the engine API differs.

## Examples

### Example 1: Template Engine Choice
```text
/compare-prompt-template-engineer "
Compare Handlebars vs Jinja2 for our prompt system. We have a
TypeScript backend but some Python microservices. Need type safety,
caching, and sanitization.
"
```

### Example 2: Architecture Decision
```text
/compare-prompt-template-engineer "
Should we use prompt-as-files or database-backed prompts?
We have a team of 5 prompt engineers who need to edit prompts
without deploying code. Currently using inline strings.
"
```

### Example 3: Sanitization Strategy
```text
/compare-prompt-template-engineer "
Compare regex sanitization pipeline vs Zod schema validation
for our prompt template data. We need to prevent prompt injection
and validate all template variables.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/prompt-template-engineer/prompt-template-engineer-constitution.md` Sections I, II
- **Related**: scaffold-prompt-template-engineer, refactor-prompt-template-engineer
