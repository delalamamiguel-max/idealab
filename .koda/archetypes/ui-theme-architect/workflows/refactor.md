---
description: Migrate existing applications to semantic token theming by auditing hardcoded colors, extracting tokens, and replacing references across components
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read refactoring guardrails from:
`${ARCHETYPES_BASEDIR}/ui-theme-architect/ui-theme-architect-constitution.md`

Focus on Section I (Hard-Stop Rules) and Section II (Mandatory Patterns).

### 2. Audit Current Color Usage

Scan the codebase for all color references that need migration:

**2.1 Hardcoded Tailwind Palette Classes**

```bash
# Find all Tailwind palette color usages in components
grep -rn "text-\(blue\|red\|green\|yellow\|purple\|pink\|orange\|slate\|gray\|zinc\|neutral\|stone\)-" src/components/ src/features/ src/pages/
grep -rn "bg-\(blue\|red\|green\|yellow\|purple\|pink\|orange\|slate\|gray\|zinc\|neutral\|stone\)-" src/components/ src/features/ src/pages/
grep -rn "border-\(blue\|red\|green\|yellow\|purple\|pink\|orange\|slate\|gray\|zinc\|neutral\|stone\)-" src/components/ src/features/ src/pages/
```

**2.2 Literal Color Values**

```bash
# Find hex, rgb, hsl, oklch literals in component files
grep -rn "#[0-9a-fA-F]\{3,8\}" src/components/ src/features/
grep -rn "rgb(\|rgba(" src/components/ src/features/
grep -rn "hsl(\|hsla(" src/components/ src/features/
```

**2.3 Inline Style Color Values**

```bash
# Find inline style objects with color properties
grep -rn "color:\s*['\"]#\|backgroundColor:\s*['\"]#\|borderColor:\s*['\"]#" src/
```

**2.4 CSS File Hardcoded Colors**

```bash
# Find literal colors in CSS/SCSS files (excluding token definitions)
grep -rn "color:\s*#\|background:\s*#\|border.*:\s*#" src/*.css src/**/*.css 2>/dev/null
```

### 3. Generate Audit Report

Produce a structured inventory:

```text
## Color Audit Report

### Summary
- Total files with hardcoded colors: {count}
- Total hardcoded color references: {count}
- Tailwind palette classes: {count}
- Literal hex/rgb/hsl values: {count}
- Inline style colors: {count}

### By Semantic Role (Proposed Mapping)
| Current Usage | Occurrences | Proposed Token |
|--------------|-------------|----------------|
| bg-slate-900, bg-gray-900 | {n} | bg-background |
| text-white, text-slate-100 | {n} | text-foreground |
| text-blue-400, text-blue-500 | {n} | text-primary |
| bg-blue-600 | {n} | bg-primary |
| text-slate-400, text-gray-400 | {n} | text-muted-foreground |
| border-slate-700 | {n} | border-border |
| bg-red-600 | {n} | bg-destructive |
| ... | ... | ... |

### Intentional Exceptions (Do Not Migrate)
| Usage | File | Justification |
|-------|------|---------------|
| Data-viz categorical colors | charts/*.tsx | Fixed palette for chart legibility |
| Brand logo colors | logo.tsx | Corporate brand identity |
```

**Present audit to user for approval before proceeding.**

### 4. Create Token CSS File

If no token system exists yet, generate the complete token CSS file following constitution Section II.1.

If a partial token system exists, extend it to cover all 20 core tokens from constitution Section IV.1 and add the light mode override block.

**Verify**: Token parity between `:root` and `html.light` blocks.

### 5. Create or Update Tailwind Registration

**Tailwind v4**: Add `@theme` block to the CSS file per constitution Section II.7.

**Tailwind v3**: Update `tailwind.config.js` to map all semantic tokens per constitution Section II.7.

### 6. Migrate Component Colors

Apply the token mapping from the audit report. Process files in this order:

1. **Layout components** (app shell, sidebar, header, footer) — highest visual impact
2. **Shared UI primitives** (buttons, badges, alerts, inputs) — most reuse
3. **Feature components** (pages, panels, modals) — largest file count
4. **One-off components** (specialized widgets) — lowest priority

**Migration rules**:

- `bg-slate-900` / `bg-gray-900` → `bg-background`
- `text-white` / `text-slate-100` → `text-foreground`
- `text-blue-400` / `text-blue-500` → `text-primary`
- `bg-blue-600` / `bg-blue-700` → `bg-primary`
- `text-slate-400` / `text-gray-400` → `text-muted-foreground`
- `bg-slate-800` / `bg-gray-800` → `bg-card` or `bg-muted`
- `border-slate-700` / `border-gray-700` → `border-border`
- `text-red-500` / `text-red-400` → `text-destructive`
- `bg-red-600` → `bg-destructive`
- Hover states: `hover:bg-slate-800` → `hover:bg-accent`
- Focus rings: `ring-blue-500` → `ring-ring`

**Important**: Do NOT blindly replace — verify each mapping makes semantic sense for the component's purpose.

### 7. Add Theme Hook

If no theme management exists, create the theme application hook per constitution Section II.2.

Mount it at the application root (e.g., `App.tsx`, `layout.tsx`, or `_app.tsx`).

### 8. Add SVG/Canvas Theme Resolution (If Needed)

Scan for SVGs with hardcoded fill/stroke values:

```bash
grep -rn "fill=\"#\|stroke=\"#\|fill: '#\|stroke: '#" src/
```

For static SVGs: Replace with `fill="currentColor"` and apply text color utility on parent.

For dynamic SVGs (charts, graphs): Integrate the `useResolvedThemeColors` hook from constitution Section II.3.

### 9. Document Exceptions

Create `THEME_EXCEPTIONS.md` for any color references that intentionally remain hardcoded. Each exception must include the file path, justification, and a review date.

### 10. Validate Refactoring

Run post-refactoring validation:

```bash
# Re-run the hardcoded color scan — should return zero for components
grep -rn "text-blue\|bg-blue\|text-red\|bg-red\|text-slate\|bg-slate" src/components/ src/features/

# Verify token parity
awk '/:root/,/^}/' src/index.css | grep -c "^\s*--"
awk '/html\.light/,/^}/' src/index.css | grep -c "^\s*--"

# Visual check: toggle between dark and light modes
```

---

## Post-Refactor Checklist

```text
✅ All palette classes replaced with semantic token utilities
✅ All literal color values extracted to CSS custom properties
✅ Token CSS file with complete dark and light blocks
✅ Tailwind registration updated
✅ Theme hook mounted at application root
✅ SVG/canvas elements use currentColor or theme resolution hook
✅ Exceptions documented in THEME_EXCEPTIONS.md
✅ Zero hardcoded colors remaining in component scans

🔧 Next Steps:
1. Run /test-ui-theme-architect to validate WCAG contrast
2. Test all pages in both dark and light modes
3. Test system preference detection
```

---

## Error Handling

**Massive Codebase (500+ files)**: Break migration into phases by directory. Complete layout and shared components first, then feature directories one at a time. Track progress in the audit report.

**Ambiguous Mapping**: When a palette color could map to multiple semantic tokens (e.g., `bg-gray-800` could be `bg-card` or `bg-muted`), ask the user to clarify the component's purpose before choosing.

**Third-Party Components**: Components from external libraries that use hardcoded colors should be documented in `THEME_EXCEPTIONS.md` and wrapped with themed containers where possible.

## Examples

### Example 1: Full Migration
```text
/refactor-ui-theme-architect "
Migrate our React dashboard from hardcoded Tailwind slate palette
to semantic tokens. Currently uses dark mode only — need to add
light mode support. About 150 component files.
"
```

### Example 2: Partial Token System
```text
/refactor-ui-theme-architect "
We already have --primary and --background defined but the rest of our
components still use text-gray-400, bg-slate-800, etc.
Need to complete the token system and migrate remaining components.
"
```

### Example 3: Framework Upgrade
```text
/refactor-ui-theme-architect "
Upgrading from Tailwind v3 to v4. Need to convert our tailwind.config.js
color definitions to @theme block and ensure all semantic tokens are
registered correctly.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/ui-theme-architect/ui-theme-architect-constitution.md` Sections I, II
- **Related**: scaffold-ui-theme-architect, test-ui-theme-architect, debug-ui-theme-architect
