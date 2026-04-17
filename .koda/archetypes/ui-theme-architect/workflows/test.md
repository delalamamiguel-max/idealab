---
description: Validate semantic token theming system for WCAG contrast compliance, token coverage, mode parity, and system preference detection
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read validation requirements from:
`${ARCHETYPES_BASEDIR}/ui-theme-architect/ui-theme-architect-constitution.md`

Focus on Section I (Hard-Stop Rules) and Section VI (Security and Performance Checklist).

### 2. Identify Test Scope

Determine what to test based on $ARGUMENTS:

| Scope | Tests |
|-------|-------|
| **Contrast** | WCAG 2.1 AA ratio validation for all foreground/background token pairs |
| **Token Parity** | Equal token counts between `:root` and `html.light` blocks |
| **Hardcoded Colors** | Zero palette classes or literal colors in component files |
| **Semantic Naming** | All custom properties use purpose-driven names |
| **System Preference** | matchMedia detection and live change listener present |
| **Framework Registration** | All tokens registered in Tailwind @theme or config |
| **Syntax Tokens** | Syntax highlighting tokens present if code rendering exists |
| **Chrome Theming** | Scrollbar, selection, and focus ring rules present |
| **No-FOUC** | Theme initialization script in head (if SSR/SSG) |
| **Reduced Motion** | prefers-reduced-motion media query present (if animations) |

### 3. Token Parity Validation

Verify that every token defined in dark mode has a corresponding light mode override.

```bash
# Extract token names from :root block
awk '/:root\s*\{/,/^\}/' src/index.css | grep -oE '--[a-z][a-z0-9-]*' | sort > /tmp/dark-tokens.txt

# Extract token names from html.light block
awk '/html\.light\s*\{/,/^\}/' src/index.css | grep -oE '--[a-z][a-z0-9-]*' | sort > /tmp/light-tokens.txt

# Compare — any differences indicate parity violations
diff /tmp/dark-tokens.txt /tmp/light-tokens.txt
```

| Test | Pass Criteria |
|------|--------------|
| Dark token count | ≥ 20 core tokens defined |
| Light token count | ≥ 20 core tokens defined |
| Token parity | diff output is empty (zero mismatches) |
| color-scheme property | Present in both `:root` and `html.light` |

### 4. WCAG Contrast Validation

For each required foreground/background token pair from constitution Section I.3, calculate the contrast ratio.

**Method**: Parse oklch values from the CSS file, convert to relative luminance, compute contrast ratio per WCAG 2.1 formula.

**Required pairs to validate (both dark and light modes)**:

| Pair | Foreground Token | Background Token | Min Ratio |
|------|-----------------|-----------------|-----------|
| 1 | `--foreground` | `--background` | 4.5:1 |
| 2 | `--card-foreground` | `--card` | 4.5:1 |
| 3 | `--popover-foreground` | `--popover` | 4.5:1 |
| 4 | `--primary-foreground` | `--primary` | 4.5:1 |
| 5 | `--muted-foreground` | `--background` | 4.5:1 |
| 6 | `--muted-foreground` | `--muted` | 4.5:1 |
| 7 | `--destructive-foreground` | `--destructive` | 4.5:1 |
| 8 | `--primary` | `--background` | 3:1 |
| 9 | `--border` | `--background` | 3:1 |
| 10 | `--ring` | `--background` | 3:1 |

**Report format per pair**:

```text
[PASS] --foreground on --background (dark): 12.3:1 (required 4.5:1)
[PASS] --foreground on --background (light): 14.1:1 (required 4.5:1)
[FAIL] --muted-foreground on --muted (light): 3.2:1 (required 4.5:1)
```

### 5. Hardcoded Color Scan

Scan all component files for constitution Rule 1.1 violations.

```bash
# Tailwind palette class violations
grep -rn "text-\(blue\|red\|green\|yellow\|purple\|pink\|orange\|slate\|gray\|zinc\|neutral\|stone\)-[0-9]" src/components/ src/features/

# Literal hex values
grep -rn "#[0-9a-fA-F]\{3,8\}" src/components/ src/features/

# Literal rgb/hsl/oklch values (outside of token definition files)
grep -rn "rgb(\|rgba(\|hsl(\|hsla(" src/components/ src/features/

# Inline style color literals
grep -rn "color:\s*['\"]#\|backgroundColor:\s*['\"]#" src/components/ src/features/
```

| Test | Pass Criteria |
|------|--------------|
| Palette class scan | Zero matches in component directories |
| Hex literal scan | Zero matches in component directories |
| RGB/HSL literal scan | Zero matches in component directories |
| Inline style scan | Zero matches in component directories |

**Exception**: Files listed in `THEME_EXCEPTIONS.md` are excluded from failure counts.

### 6. Semantic Naming Validation

Verify all CSS custom properties use purpose-driven names per constitution Rule 1.2.

```bash
# Extract all custom property names from the CSS file
grep -oE '--[a-z][a-z0-9-]*' src/index.css | sort -u

# Check for palette-derived names (violations)
grep -oE '--[a-z][a-z0-9-]*' src/index.css | grep -iE "(blue|red|green|yellow|purple|slate|gray|zinc|stone|neutral|orange|pink)-[0-9]"
```

| Test | Pass Criteria |
|------|--------------|
| Palette name scan | Zero palette-derived token names found |
| Naming convention | All tokens match `--{role}` or `--{role}-{modifier}` pattern |

### 7. System Preference Detection Test

Verify the theme management hook meets constitution Rule 1.4 requirements.

```bash
# Check for matchMedia usage
grep -rn "prefers-color-scheme" src/lib/ src/hooks/

# Check for live change listener
grep -rn "addEventListener.*change" src/lib/ src/hooks/

# Check for three-mode support
grep -rn "'dark'\|'light'\|'system'" src/lib/ src/hooks/
```

| Test | Pass Criteria |
|------|--------------|
| matchMedia query | At least one `prefers-color-scheme` reference found |
| Change listener | At least one `addEventListener('change', ...)` found |
| Three modes | dark, light, and system mode strings all present |

### 8. Framework Registration Test

Verify Tailwind integration per constitution Section II.7.

**Tailwind v4**:

```bash
# Check @theme block contains all core tokens
grep -A50 "@theme" src/index.css | grep -c "color-"
# Expected: ≥ 20 color registrations
```

**Tailwind v3**:

```bash
# Check config has color mappings
grep -c "var(--" tailwind.config.js tailwind.config.ts 2>/dev/null
# Expected: ≥ 20 var() references
```

| Test | Pass Criteria |
|------|--------------|
| Token registration count | ≥ 20 tokens registered with framework |
| No literal colors in config | Zero hex/rgb/hsl values in registration block |

### 9. Chrome Theming Test

Verify scrollbar, selection, and focus ring theming per constitution Section II.5.

```bash
# Check scrollbar theming
grep -n "scrollbar-color\|scrollbar-width" src/index.css

# Check selection theming
grep -n "::selection" src/index.css

# Check focus ring theming
grep -n ":focus-visible" src/index.css
```

| Test | Pass Criteria |
|------|--------------|
| Scrollbar rules | `scrollbar-color` and `scrollbar-width` present |
| Selection rules | `::selection` with semantic token reference present |
| Focus ring rules | `:focus-visible` with `--ring` token reference present |

### 10. Generate Test Report

```text
## Theme Test Report

**Test Date**: {timestamp}
**Project**: {project_name}
**CSS File**: {path_to_token_file}

### Token Parity Tests
| Test | Status |
|------|--------|
| Dark token count (≥20) | {PASS/FAIL} ({count}) |
| Light token count (≥20) | {PASS/FAIL} ({count}) |
| Token parity match | {PASS/FAIL} |
| color-scheme property | {PASS/FAIL} |

### WCAG Contrast Tests (Dark Mode)
| Pair | Ratio | Required | Status |
|------|-------|----------|--------|
| foreground / background | {ratio} | 4.5:1 | {PASS/FAIL} |
| card-foreground / card | {ratio} | 4.5:1 | {PASS/FAIL} |
| primary-foreground / primary | {ratio} | 4.5:1 | {PASS/FAIL} |
| muted-foreground / background | {ratio} | 4.5:1 | {PASS/FAIL} |
| muted-foreground / muted | {ratio} | 4.5:1 | {PASS/FAIL} |
| destructive-fg / destructive | {ratio} | 4.5:1 | {PASS/FAIL} |
| primary / background | {ratio} | 3:1 | {PASS/FAIL} |
| border / background | {ratio} | 3:1 | {PASS/FAIL} |
| ring / background | {ratio} | 3:1 | {PASS/FAIL} |

### WCAG Contrast Tests (Light Mode)
| Pair | Ratio | Required | Status |
|------|-------|----------|--------|
| foreground / background | {ratio} | 4.5:1 | {PASS/FAIL} |
| card-foreground / card | {ratio} | 4.5:1 | {PASS/FAIL} |
| primary-foreground / primary | {ratio} | 4.5:1 | {PASS/FAIL} |
| muted-foreground / background | {ratio} | 4.5:1 | {PASS/FAIL} |
| muted-foreground / muted | {ratio} | 4.5:1 | {PASS/FAIL} |
| destructive-fg / destructive | {ratio} | 4.5:1 | {PASS/FAIL} |
| primary / background | {ratio} | 3:1 | {PASS/FAIL} |
| border / background | {ratio} | 3:1 | {PASS/FAIL} |
| ring / background | {ratio} | 3:1 | {PASS/FAIL} |

### Hardcoded Color Tests
| Test | Status |
|------|--------|
| Palette class scan | {PASS/FAIL} ({count} violations) |
| Hex literal scan | {PASS/FAIL} ({count} violations) |
| RGB/HSL literal scan | {PASS/FAIL} ({count} violations) |

### System Preference Tests
| Test | Status |
|------|--------|
| matchMedia detection | {PASS/FAIL} |
| Live change listener | {PASS/FAIL} |
| Three-mode support | {PASS/FAIL} |

### Framework Registration Tests
| Test | Status |
|------|--------|
| Token count (≥20) | {PASS/FAIL} ({count}) |
| No literals in config | {PASS/FAIL} |

### Chrome Theming Tests
| Test | Status |
|------|--------|
| Scrollbar theming | {PASS/FAIL} |
| Selection theming | {PASS/FAIL} |
| Focus ring theming | {PASS/FAIL} |

---

**Overall**: {PASS_COUNT}/{TOTAL_COUNT} tests passed
**Hard-Stop Violations**: {count}
**Constitution Compliance**: {COMPLIANT / NON-COMPLIANT}
```

---

## Error Handling

**No CSS Token File Found**: Report as critical failure — the project has no theme system. Recommend running `/scaffold-ui-theme-architect` first.

**oklch Conversion Difficulty**: If oklch values cannot be programmatically converted to luminance for contrast calculation, report the raw oklch lightness values and note that lightness differences of ≥ 0.60 between foreground and background generally satisfy 4.5:1 for the sRGB gamut.

**Partial Test Scope**: If $ARGUMENTS specifies only certain tests (e.g., "just check contrast"), run only those tests but note which tests were skipped in the report.

## Examples

### Example 1: Full Validation
```text
/test-ui-theme-architect "
Run complete theme validation on our React app.
Token file is src/index.css. Components in src/components/ and src/features/.
"
```

### Example 2: Contrast Only
```text
/test-ui-theme-architect "
Just validate WCAG contrast ratios for our token values.
We updated the muted-foreground token and want to verify it still passes.
"
```

### Example 3: Post-Refactor Validation
```text
/test-ui-theme-architect "
We just migrated from hardcoded slate palette to semantic tokens.
Verify zero hardcoded colors remain and all tokens are properly paired.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/ui-theme-architect/ui-theme-architect-constitution.md` Sections I, VI
- **Related**: scaffold-ui-theme-architect, debug-ui-theme-architect, refactor-ui-theme-architect
