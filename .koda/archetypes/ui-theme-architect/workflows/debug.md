---
description: Diagnose and fix theme inconsistencies including flash-of-wrong-theme, missing dark/light overrides, SVG color failures, and contrast violations
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read troubleshooting guidance from:
`${ARCHETYPES_BASEDIR}/ui-theme-architect/ui-theme-architect-constitution.md`

Focus on Section V (Troubleshooting Guide).

### 2. Identify Problem Category

Categorize the reported issue based on $ARGUMENTS:

| Category | Symptoms | Common Causes |
|----------|----------|---------------|
| **FOUC / Flash** | Page flashes wrong theme on load | Missing no-FOUC script, script after CSS, hydration mismatch |
| **SVG/Canvas Colors** | Charts or icons ignore theme toggle | Hardcoded fill/stroke, missing MutationObserver, stale getComputedStyle |
| **Contrast Failure** | Text unreadable, accessibility audit fails | Token values too close in lightness, missing pair validation |
| **Token Parity** | UI broken in one mode only | Token defined in `:root` but missing from `html.light` or vice versa |
| **Tailwind Utilities** | `bg-background` not applying styles | Missing `@theme` registration, stale Tailwind cache, wrong config |
| **System Preference** | App ignores OS dark/light toggle | Missing matchMedia listener, listener cleaned up early, no system mode |
| **Scrollbar/Selection** | Browser chrome clashes with dark theme | Missing scrollbar-color rule, no ::selection override |
| **Syntax Highlighting** | Code blocks show wrong colors after toggle | Syntax tokens missing from light override, editor not re-rendering |

### 3. Collect Diagnostic Information

**For FOUC Issues:**

```bash
# Check if no-FOUC script exists in HTML head
grep -n "prefers-color-scheme\|classList.add.*light\|theme" index.html public/index.html src/index.html 2>/dev/null

# Check script position relative to CSS
grep -n "<script\|<link.*css\|<style" index.html public/index.html 2>/dev/null
```

**For Token Parity Issues:**

```bash
# Count custom properties in each theme block
# Extract lines between :root { and the closing } , count -- prefixed lines
awk '/:root/,/^}/' src/index.css | grep -c "^\s*--"
awk '/html\.light/,/^}/' src/index.css | grep -c "^\s*--"

# Find tokens in :root but not in html.light (and vice versa)
diff <(awk '/:root/,/^}/' src/index.css | grep -oP '--[\w-]+' | sort) \
     <(awk '/html\.light/,/^}/' src/index.css | grep -oP '--[\w-]+' | sort)
```

**For Hardcoded Color Issues:**

```bash
# Scan components for literal color values
grep -rn "text-blue\|bg-blue\|text-red\|bg-red\|text-slate\|bg-slate\|text-gray\|bg-gray" src/components/
grep -rn "#[0-9a-fA-F]\{3,8\}" src/components/
grep -rn "rgb(\|hsl(" src/components/
```

**For System Preference Issues:**

```bash
# Check if matchMedia is used in the codebase
grep -rn "prefers-color-scheme" src/
grep -rn "matchMedia" src/
grep -rn "addEventListener.*change" src/lib/hooks/
```

**For Tailwind Registration Issues:**

```bash
# Check @theme block exists (Tailwind v4)
grep -A5 "@theme" src/index.css

# Check tailwind.config (Tailwind v3)
grep -A10 "colors:" tailwind.config.js tailwind.config.ts 2>/dev/null
```

### 4. Common Issues and Solutions

#### 4.1 Flash of Wrong Theme on Page Load

**Symptom**: Dark theme flashes briefly before switching to the user's saved light preference (or vice versa).

**Diagnosis**: Check whether the no-FOUC script exists and whether it executes before any CSS loads.

**Solution**: Add the synchronous script from constitution Section III.1 inside `<head>` before any `<link>` or `<style>` tags. The script must be inline (not an external file) so it executes immediately. For Next.js, use `dangerouslySetInnerHTML` in a custom `_document.tsx` or `next/script` with `strategy="beforeInteractive"`.

#### 4.2 SVG Elements Not Updating on Theme Toggle

**Symptom**: SVG icons, chart bars, or diagram strokes retain their initial color when the user switches themes.

**Diagnosis**: Check SVG elements for hardcoded `fill` or `stroke` attributes. Check if `useResolvedThemeColors` hook is used.

**Solution**:
- For simple SVGs: Replace `fill="#0057b8"` with `fill="currentColor"` and style the parent with `text-primary`
- For complex SVGs (charts, data-viz): Use the `useResolvedThemeColors` hook from constitution Section II.3 to read CSS variable values at runtime and re-render on theme change

#### 4.3 Contrast Ratio Failure in One Mode

**Symptom**: Text passes contrast in dark mode but fails in light mode (common) or vice versa.

**Diagnosis**: The oklch lightness values for the failing mode are too close between the foreground and background tokens.

**Solution**: Adjust the oklch lightness channel. For dark mode body text, foreground lightness should be ≥ 0.85 against a background with lightness ≤ 0.20. For light mode, foreground lightness should be ≤ 0.25 against a background with lightness ≥ 0.95. Use an oklch contrast calculator to verify before committing changes.

#### 4.4 Missing Token in One Theme Mode

**Symptom**: A component looks correct in dark mode but text disappears or turns an unexpected color in light mode.

**Diagnosis**: A token exists in `:root` but has no override in `html.light`. The light mode inherits the dark value, which may be near-white text on a near-white background.

**Solution**: Add the missing token to the `html.light` block. Run the token parity check from Step 3 to catch all mismatches at once.

#### 4.5 Tailwind Utilities Not Generating

**Symptom**: `bg-background` renders as plain text in the DOM with no corresponding CSS rule.

**Diagnosis**: The token is not registered in Tailwind's theme system.

**Solution**:
- Tailwind v4: Verify the `@theme` block in the CSS file includes `--color-background: var(--background);`
- Tailwind v3: Verify `tailwind.config.js` has `colors: { background: 'var(--background)' }` in `theme.extend`
- After config changes, restart the Tailwind dev server to clear the class scanning cache

#### 4.6 System Preference Changes Not Detected

**Symptom**: User changes OS from dark to light (or light to dark) but the app doesn't respond.

**Diagnosis**: Either the `matchMedia` listener was never registered, or it was cleaned up too early.

**Solution**: Verify the theme hook is mounted at the application root level (e.g., in `App.tsx` or `layout.tsx`), not inside a lazy-loaded route component. Ensure the `addEventListener('change', handler)` is in the `system` mode branch and the cleanup function only runs on mode change or unmount.

### 5. Generate Debug Report

After diagnosis, provide a structured report:

```text
## Theme Debug Report

**Issue Category**: {category from Step 2}
**Root Cause**: {one-sentence root cause}
**Affected Mode**: Dark / Light / Both / System

**Diagnostic Commands Run**:
- {command_1}: {result_summary}
- {command_2}: {result_summary}

**Files Modified**:
- {file_path}: {what was changed and why}

**Solution Applied**:
{step_by_step_description}

**Verification**:
{how to confirm the fix works}

**Prevention**:
{how to prevent this issue from recurring — e.g., add token parity check to CI}

**Constitution Reference**: Section {section_number}
```

---

## Error Handling

**Cannot Reproduce**: Ask the user for their OS theme setting, browser, and the exact steps to trigger the issue. Theme bugs are often mode-specific and require testing in both dark and light.

**Multiple Issues**: Categorize each issue separately, prioritize by severity (hard-stop violations first), and fix them in sequence.

## Examples

### Example 1: FOUC Bug
```text
/debug-ui-theme-architect "
Page flashes dark for a moment before switching to light mode.
Using Next.js 14 with app router. Theme preference stored in localStorage.
"
```

### Example 2: SVG Color Bug
```text
/debug-ui-theme-architect "
Chart SVGs in the dashboard don't change color when I toggle dark mode.
Using Recharts with custom SVG bars. React 19 + Tailwind v4.
"
```

### Example 3: Contrast Failure
```text
/debug-ui-theme-architect "
Lighthouse reports contrast failures on muted text in light mode.
The text is using text-muted-foreground on bg-background.
Dark mode passes fine.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/ui-theme-architect/ui-theme-architect-constitution.md` Section V
- **Related**: scaffold-ui-theme-architect, test-ui-theme-architect, refactor-ui-theme-architect
