---
description: Compare semantic token theming approaches, CSS architecture strategies, and framework integration options
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read comparison criteria from:
`${ARCHETYPES_BASEDIR}/ui-theme-architect/ui-theme-architect-constitution.md`

### 2. Identify Comparison Type

Based on $ARGUMENTS, determine what to compare:

| Comparison Type | Examples |
|-----------------|----------|
| **Token Architecture** | CSS custom properties vs CSS-in-JS theme objects vs Style Dictionary |
| **Color Spaces** | oklch vs hsl vs hex vs display-p3 for token values |
| **Framework Integration** | Tailwind v4 `@theme` vs Tailwind v3 config vs vanilla CSS |
| **Mode Switching** | Class toggle (`html.light`) vs `data-theme` attribute vs media query only |
| **Theme Persistence** | localStorage vs cookie vs server-side session |
| **Variant Systems** | class-variance-authority vs tailwind-variants vs manual className merging |
| **Contrast Validation** | axe-core vs Lighthouse vs custom oklch luminance calculator |

### 3. Define Comparison Criteria

Apply constitution-based evaluation criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **WCAG Compliance** | High | Ability to enforce and validate contrast ratios |
| **Mode Completeness** | High | Support for dark, light, and system modes |
| **Token Portability** | High | Framework independence — can tokens move between projects? |
| **Performance** | Medium | Runtime cost, CSS bundle size, paint triggers |
| **Developer Experience** | Medium | Authoring ease, IDE support, debugging |
| **Constitution Alignment** | High | Compliance with hard-stop rules and mandatory patterns |

### 4. Analyze Option A

For the first approach, evaluate:

```markdown
## Option A: {name}

### Description
{Brief description of the approach}

### WCAG Compliance
- Contrast validation: {how contrast is checked}
- Automated testing: {tooling support}

### Mode Support
- Dark/light/system: {supported modes}
- Live system preference: {real-time OS tracking}
- No-FOUC: {flash prevention approach}

### Token Portability
- Framework dependence: {locked to specific framework?}
- CSS inspectability: {visible in browser DevTools?}
- Migration path: {effort to move to different framework}

### Performance
- Runtime cost: {CSS-only vs JavaScript-dependent}
- Bundle size impact: {additional bytes}
- Paint triggers: {theme switch repaint cost}

### Developer Experience
- IDE support: {autocomplete, type safety}
- Debugging: {DevTools visibility}
- Learning curve: {adoption difficulty}

### Constitution Compliance
- Hard-stop violations: {count and details}
- Mandatory pattern coverage: {coverage percentage}
```

### 5. Analyze Option B

Evaluate the second approach using the same template as Step 4.

### 6. Generate Comparison Matrix

```markdown
## Comparison Matrix

| Criterion | Option A | Option B | Winner |
|-----------|----------|----------|--------|
| **WCAG Compliance** | | | |
| Contrast validation | {a} | {b} | {winner} |
| Automated testing support | {a} | {b} | {winner} |
| **Mode Support** | | | |
| Dark/light/system | {a} | {b} | {winner} |
| Live system preference | {a} | {b} | {winner} |
| No-FOUC capability | {a} | {b} | {winner} |
| **Token Portability** | | | |
| Framework independence | {a} | {b} | {winner} |
| DevTools inspectability | {a} | {b} | {winner} |
| **Performance** | | | |
| Runtime cost | {a} | {b} | {winner} |
| Bundle size | {a} | {b} | {winner} |
| **Developer Experience** | | | |
| IDE support | {a} | {b} | {winner} |
| Learning curve | {a} | {b} | {winner} |
| **Constitution Compliance** | | | |
| Hard-stop alignment | {a} | {b} | {winner} |

**Overall Score**: Option A: {score}/10, Option B: {score}/10
```

### 7. Provide Recommendation

```markdown
## Recommendation

### Recommended: {Option A or B}

**Rationale**:
{Why this option aligns with constitution requirements and project needs}

### When to Choose Option A
- {scenario}
- {scenario}

### When to Choose Option B
- {scenario}
- {scenario}

### Migration Path (if applicable)
{Steps to move from one approach to the other}
```

---

## Common Comparisons

### CSS Custom Properties vs CSS-in-JS Theme Objects

| Aspect | CSS Custom Properties | CSS-in-JS (styled-components, Emotion) |
|--------|----------------------|----------------------------------------|
| DevTools inspectable | Yes — visible in Elements panel | No — computed at runtime |
| Framework portable | Yes — works with any framework | No — locked to specific library |
| Bundle size | Zero JS overhead | Adds 8-15KB runtime |
| Mode switching cost | CSS repaint only | JS re-render + CSS repaint |
| Constitution compliance | Full | Violates Rule 1.6 (CSS as source of truth) |
| **Recommendation** | **Preferred** | Acceptable only if existing codebase requires it |

### oklch vs hsl vs hex for Token Values

| Aspect | oklch | hsl | hex |
|--------|-------|-----|-----|
| Perceptual uniformity | Excellent — equal lightness steps look equal | Poor — lightness varies by hue | None |
| Programmatic mixing | `color-mix(in oklch, ...)` | `color-mix(in hsl, ...)` | Requires conversion |
| Contrast prediction | Lightness channel directly maps to luminance | Lightness unreliable across hues | Manual calculation |
| Browser support | All evergreen (2024+) | Universal | Universal |
| **Recommendation** | **Preferred for new projects** | Acceptable for legacy compat | Avoid for token definitions |

### Tailwind v4 `@theme` vs Tailwind v3 Config

| Aspect | Tailwind v4 `@theme` | Tailwind v3 `tailwind.config.js` |
|--------|---------------------|----------------------------------|
| Configuration format | CSS (co-located with tokens) | JavaScript (separate file) |
| Token proximity | Same file as custom properties | Different file from CSS |
| Hot reload | Instant (CSS-native) | Requires config file watcher |
| Migration effort | Rewrite config as `@theme` block | Already in place |
| **Recommendation** | **Preferred for new projects** | Keep if already using v3 |

### Class Toggle vs Data Attribute for Mode Switching

| Aspect | `html.light` class | `[data-theme="light"]` attribute |
|--------|--------------------|---------------------------------|
| Tailwind support | Native `dark:` variant with `darkMode: 'class'` | Requires custom variant |
| CSS specificity | Class selector (0,1,0) | Attribute selector (0,1,0) — equal |
| JavaScript API | `classList.add/remove` | `dataset.theme = 'light'` |
| Multi-theme support | Binary (light/dark only) | Arbitrary (supports 3+ themes) |
| BluePearl pattern | Yes — proven in production | Not used |
| **Recommendation** | **Preferred for dark/light** | Better for 3+ distinct themes |

---

## Error Handling

**Incomplete Comparison Request**: Ask which two specific approaches to compare. Provide the comparison type table from Step 2 for reference.

**Constitutional Violation in Option**: Flag the violation clearly and note it as a disadvantage in the comparison matrix.

## Examples

### Example 1: Architecture Comparison
```text
/compare-ui-theme-architect "
Compare CSS custom properties with dark/light class toggle
vs styled-components ThemeProvider approach
for a new React application
"
```

### Example 2: Color Space Comparison
```text
/compare-ui-theme-architect "
Compare oklch vs hsl for defining our semantic token values.
We need perceptually uniform lightness steps for generating
accessible foreground/background pairs.
"
```

### Example 3: Framework Integration
```text
/compare-ui-theme-architect "
Compare Tailwind v4 @theme registration approach
vs Tailwind v3 config approach.
We are upgrading from v3 to v4 and want to know the migration effort.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/ui-theme-architect/ui-theme-architect-constitution.md`
- **Related**: scaffold-ui-theme-architect, refactor-ui-theme-architect
