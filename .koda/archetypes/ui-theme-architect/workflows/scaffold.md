---
description: Design and generate a complete semantic token theming system with dark/light/system mode switching, WCAG contrast compliance, and framework integration
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory

**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Constitution Validation

Read and apply guardrails from:
`${ARCHETYPES_BASEDIR}/ui-theme-architect/ui-theme-architect-constitution.md`

Verify no hard-stop rule violations exist in the user's requirements.

### 2. Gather Theme Requirements

**PROMPT THE USER FOR ALL OF THE FOLLOWING before starting scaffold:**

#### 2.1 Project Context
- **Project Name**: Application or package identifier
- **Framework**: React | Next.js | Remix | Astro | Vue | Svelte | Vanilla
- **CSS Framework**: Tailwind v4 | Tailwind v3 | Vanilla CSS | CSS Modules
- **Existing Codebase**: Greenfield or adding theming to existing project?

#### 2.2 Theme Palette Direction
- **Brand Colors**: AT&T blue, custom brand primary, or neutral?
- **Color Space**: oklch (recommended) | hsl | hex
- **Hue Range**: Blue-purple (BluePearl default), corporate blue, custom hue angle

#### 2.3 Mode Support
- **Default Mode**: Dark-first (recommended) or light-first
- **Modes**: Dark + Light + System (required minimum)
- **Persistence**: localStorage key name (default: `theme-preference`)

#### 2.4 Feature Scope
- **Syntax Highlighting**: Yes/No (required if code rendering present)
- **SVG/Canvas Theming**: Yes/No (required if dynamic SVG/canvas present)
- **No-FOUC Script**: Yes/No (recommended for SSR/SSG)
- **Reduced Motion**: Yes/No (recommended)
- **High Contrast**: Yes/No (optional)
- **Multi-Brand**: Yes/No (optional — for white-label deployments)

#### 2.5 Component Library
- **UI Library**: shadcn/ui | Radix | Headless UI | Custom
- **Variant System**: class-variance-authority | tailwind-variants | manual

**⛔ STOP: Do not proceed until all requirements gathered.**

---

### 3. Generate Token CSS File

Create the main theme CSS file following constitution Section II.1.

**Deliverable**: `src/index.css` or `src/tokens.css`

**Structure**:
1. `:root` block with `color-scheme: dark` and all 20+ core semantic tokens using oklch values
2. `html.light` block with `color-scheme: light` and corresponding overrides for every token
3. Syntax highlighting token blocks (if scope includes code rendering) per Section II.4
4. `@theme` block for Tailwind v4 registration (or note for v3 config) per Section II.7
5. Scrollbar, selection, and focus ring rules per Section II.5
6. Reduced motion media query per Section III.2 (if applicable)
7. High contrast media query per Section III.3 (if applicable)

**Token groups in order**:
- Surface tokens: `--background`, `--foreground`, `--card`, `--card-foreground`, `--popover`, `--popover-foreground`
- Action tokens: `--primary`, `--primary-foreground`, `--secondary`, `--secondary-foreground`
- State tokens: `--muted`, `--muted-foreground`, `--accent`, `--accent-foreground`, `--destructive`, `--destructive-foreground`
- Chrome tokens: `--border`, `--input`, `--ring`, `--radius`
- Extended tokens: `--sidebar`, `--sidebar-foreground`, `--sidebar-border` (if sidebar present)
- Syntax tokens: `--syntax-keyword` through `--syntax-punctuation` (if code rendering)

**Validation**: Count tokens in `:root` and `html.light` — counts must match (constitution Section I.5).

### 4. Generate Theme Application Hook

Create the theme management hook following constitution Section II.2.

**Deliverable**: `src/lib/hooks/use-theme.ts` (or framework equivalent)

**Requirements**:
- Accept `'dark' | 'light' | 'system'` mode parameter
- Toggle `.light` class on `document.documentElement`
- Query `matchMedia('(prefers-color-scheme: light)')` for system mode
- Register persistent `change` listener for real-time OS preference tracking
- Clean up listener on unmount or mode change

### 5. Generate SVG/Canvas Theme Resolution Hook (If Applicable)

Create the runtime color resolver following constitution Section II.3.

**Deliverable**: `src/lib/hooks/use-theme-colors.ts` (or framework equivalent)

**Requirements**:
- Accept array of token names to resolve
- Read computed values via `getComputedStyle`
- Observe `<html>` class mutations via `MutationObserver`
- Return reactive state object with resolved color strings

### 6. Generate No-FOUC Script (If Applicable)

Create the synchronous theme initialization script following constitution Section III.1.

**Deliverable**: Inline `<script>` block for `<head>` (framework-specific placement)

**Requirements**:
- Synchronous execution before first paint
- Read localStorage preference
- Fall back to `matchMedia` system preference
- Add `.light` class if resolved as light mode
- Wrapped in try/catch for private browsing compatibility

### 7. Generate Component Variant Examples

Create 3 example components demonstrating the variant system following constitution Section II.6.

**Deliverables**:
- `src/components/ui/button.tsx` — Button with 6 intent variants (primary, danger, outline, subtle, ghost, link) and 4 size variants
- `src/components/ui/badge.tsx` — Badge with semantic color variants (default, success, warning, destructive, outline)
- `src/components/ui/alert.tsx` — Alert with intent variants (info, success, warning, destructive)

**Validation**: Run `grep -rn "text-blue\|bg-blue\|text-red\|bg-red\|text-slate\|bg-slate" src/components/` — must return zero matches.

### 8. Generate Theme Toggle Component

Create a user-facing theme switcher.

**Deliverable**: `src/components/theme-toggle.tsx`

**Requirements**:
- Three-state toggle: Dark / Light / System
- Reads current mode from application state
- Persists selection to localStorage
- Visual indicator of current mode (icon or label)

### 9. Generate THEME_EXCEPTIONS.md (If Applicable)

If the project has intentional color exceptions (data-viz, brand logos, git indicators), document them.

**Deliverable**: `THEME_EXCEPTIONS.md` at project root

**Structure**:
- Exception description
- Component and file location
- Justification for using fixed colors
- Review date for re-evaluation

### 10. Generate Tailwind Configuration

For Tailwind v3 projects, generate the config file per constitution Section II.7.

**Deliverable**: `tailwind.config.js` or `tailwind.config.ts`

For Tailwind v4 projects, the `@theme` block in the CSS file (Step 3) serves as the configuration.

### 11. Validate and Report

Run constitution compliance checks:

1. **Token parity**: Count tokens in `:root` vs `html.light` — must match
2. **Hardcoded color scan**: `grep -rn "#[0-9a-fA-F]\{3,8\}\|rgb(\|hsl(\|oklch(" src/components/` — should return zero
3. **Semantic naming**: All `--` custom properties use purpose names, not palette names
4. **Framework registration**: `@theme` block or config includes all token names

---

## Post-Scaffold Checklist

```text
✅ Token CSS file with 20+ semantic tokens in dark and light modes
✅ Theme application hook with system preference detection
✅ SVG/canvas theme resolution hook (if applicable)
✅ No-FOUC initialization script (if applicable)
✅ 3 component variant examples using only semantic tokens
✅ Theme toggle component
✅ THEME_EXCEPTIONS.md (if applicable)
✅ Tailwind registration (@theme or config)

🔧 Next Steps:
1. Review token values against your brand palette
2. Run /test-ui-theme-architect to validate WCAG contrast compliance
3. Integrate theme hook at application root
4. Replace any remaining hardcoded colors in existing components
```

---

## Error Handling

**Hard-Stop Violations**: Explain which rule was violated, show the compliant alternative from the constitution, and refuse to generate non-compliant code.

**Incomplete Input**: List missing information from Step 2 requirements and provide the template for the user to fill in.

**Framework Not Supported**: If the requested framework is not React, adapt hook patterns to the framework's reactivity model (Vue composables, Svelte stores, etc.) while maintaining the same architectural requirements.

## Examples

### Example 1: React + Tailwind v4 Greenfield
```text
/scaffold-ui-theme-architect "
New React 19 + Tailwind v4 application.
AT&T blue brand color. Dark-first.
Includes code editor with syntax highlighting.
shadcn/ui components with class-variance-authority.
SSR via Next.js — need no-FOUC script.
"
```

### Example 2: Adding Theme to Existing App
```text
/scaffold-ui-theme-architect "
Existing React app with Tailwind v3.
Currently uses hardcoded slate/blue palette.
Need to migrate to semantic tokens.
No code rendering, no SVG theming needed.
"
```

### Example 3: Multi-Brand Deployment
```text
/scaffold-ui-theme-architect "
Vue 3 + Tailwind v4.
Three brand deployments: AT&T Consumer, AT&T Business, FirstNet.
Each brand needs distinct primary color.
Surface tokens shared across brands.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/ui-theme-architect/ui-theme-architect-constitution.md`
- **Related**: debug-ui-theme-architect, test-ui-theme-architect, refactor-ui-theme-architect
