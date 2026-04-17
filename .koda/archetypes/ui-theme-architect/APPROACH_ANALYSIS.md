# UI Theme Architect: Approach Analysis

**Analysis Date**: March 2026
**Source**: `docs/plans/new-archetypes.md` § CREATE NEW #1
**Status**: Pre-creation analysis — constitution and workflows not yet built

---

## 1. Why This Archetype Exists

`frontend-only` covers generic frontend scaffolding (React, routing, state, styling, testing) but has **no specific guidance** for building a comprehensive semantic token theming system. Theming is a cross-cutting concern that touches every component, requires careful accessibility compliance, and has its own set of industry standards (W3C Design Tokens, WCAG 2.1 AA contrast, `prefers-color-scheme`, `prefers-reduced-motion`).

Teams that attempt theming without a structured approach end up with:
- Hardcoded colors scattered across hundreds of components
- Dark mode as an afterthought with `dark:` prefix explosion
- No contrast validation → WCAG failures
- SVG/canvas elements that ignore theme changes
- Flash of unstyled content (FOUC) on page load
- No system preference detection

---

## 2. Reference Implementation

BluePearl's own frontend theming system serves as the battle-tested reference:

| File | Lines | Role |
|------|-------|------|
| `frontend/src/index.css` | ~334 | Complete semantic token system: `:root` dark default, `html.light` overrides, 40+ CSS custom properties, `@theme` Tailwind v4 registration, scrollbar/selection/focus theming, 25 Lexical syntax highlighting tokens |
| `frontend/src/lib/hooks/use-theme.ts` | ~30 | Theme application hook: reads Zustand store, `matchMedia` listener for system preference, `.light` class toggle on `<html>` |
| `frontend/src/lib/hooks/use-theme-colors.ts` | ~60 | SVG theme resolution: `getComputedStyle` for CSS vars, `MutationObserver` on `<html>` class changes, oklch channel value handling |
| `frontend/src/components/ui/*.tsx` | ~200 | shadcn/ui primitives with variant systems using only semantic tokens |

### Key Patterns to Encode

1. **Dark-first CSS variables** — `:root` defines dark theme (default), `html.light` overrides only changed values
2. **Semantic naming** — `--background`, `--foreground`, `--muted`, `--border`, `--primary` (not `--blue-500`)
3. **Tailwind v4 `@theme` registration** — CSS vars become first-class utilities (`bg-background`, `text-foreground`)
4. **Zero hardcoded colors in components** — all use semantic tokens; intentional exceptions documented
5. **System preference with live listener** — `matchMedia('(prefers-color-scheme: light)')` + `addEventListener('change')`
6. **SVG/canvas runtime resolution** — `getComputedStyle` + `MutationObserver` for theme-aware non-CSS rendering
7. **Syntax highlighting tokens** — 25 tokens for code blocks, inline code, Lexical editor
8. **Categorical exceptions** — data-viz, skill categories, git branches use fixed colors for distinction (documented)

---

## 3. Scope Boundaries

### In Scope
- CSS custom property semantic token systems
- Dark/light/system mode switching with live preference detection
- `@theme` registration for Tailwind v4 (or equivalent CSS-in-JS integration)
- WCAG 2.1 AA contrast validation for all token pairs
- Syntax highlighting token sets (code blocks, inline code)
- SVG/canvas theme-aware rendering hooks
- Scrollbar, selection highlight, focus ring, modal backdrop theming
- Reduced motion support (`prefers-reduced-motion`)
- High contrast mode (`prefers-contrast`)
- No-FOUC loading patterns (SSR `<script>` in `<head>`)
- Token documentation generation
- Component variant token patterns (Radix/shadcn style)

### Out of Scope (Delegated)
- Component library scaffolding → `frontend-only`
- Full application routing/state → `frontend-only`
- Brand identity design → human design team
- Icon library selection → `frontend-only`
- Backend API design → `backend-only`

---

## 4. Industry Standards Alignment

| Practice | Standard/Source | Constitution Section |
|----------|----------------|---------------------|
| CSS custom properties for theming | W3C, Material Design 3 | Hard-stop: all colors via tokens |
| System preference detection | `prefers-color-scheme` spec | Mandatory pattern |
| Semantic design tokens | W3C Design Tokens Community Group | Token naming rules |
| No-FOUC theme loading | Next.js/Remix patterns | Scaffold deliverable |
| WCAG 2.1 AA color contrast | W3C WCAG 2.1 | Test workflow gate |
| Reduced motion support | `prefers-reduced-motion` spec | Mandatory pattern |
| High contrast mode | `prefers-contrast` spec | Optional enhancement |
| Token documentation | Style Dictionary / Figma Tokens | Document workflow |
| CSS `color-mix()` for variants | CSS Color Level 5 | Advanced pattern |
| Component variant tokens | Radix/shadcn pattern | Mandatory pattern |

### Gaps in BluePearl Reference (to address in constitution)

| Gap | Priority | Approach |
|-----|----------|----------|
| No-FOUC SSR script | Medium | Add `<script>` pattern that reads `localStorage` before first paint |
| WCAG contrast validation | High | Add automated contrast checker as test workflow gate |
| `prefers-reduced-motion` | Medium | Add motion-safe/motion-reduce token layer |
| `prefers-contrast` | Low | Add high-contrast token overrides |
| Token documentation generator | Medium | Parse CSS vars → generate visual token catalog |
| Multi-brand support | Low | Token layer abstraction for brand switching |

---

## 5. Constitution Structure Plan

### Hard-Stop Rules (non-negotiable)
1. **No hardcoded colors** — every color value must reference a CSS custom property
2. **Semantic naming only** — no `--blue-500`; use `--primary`, `--muted-foreground`
3. **Contrast compliance** — all foreground/background token pairs must meet WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large text)
4. **System preference respected** — `prefers-color-scheme` must be detected and honored
5. **Dark and light themes complete** — no token may exist in one mode without the other

### Mandatory Patterns
1. Token system architecture (`:root` defaults + override class)
2. Theme hook with system preference detection + live listener
3. SVG/canvas theme resolution hook
4. Syntax highlighting token set
5. Scrollbar/selection/focus theming
6. Component variant system using tokens

### Recommended Patterns
1. No-FOUC loading script
2. Reduced motion layer
3. High contrast layer
4. Token documentation page
5. CSS `color-mix()` for programmatic variants
6. Multi-brand token abstraction

---

## 6. Workflow Plan

| Workflow | Purpose | Key Deliverables |
|----------|---------|-----------------|
| **scaffold** | Full theme system from scratch | `index.css` with 40+ tokens, `@theme` block, `use-theme.ts`, `use-theme-colors.ts`, UI primitives, syntax tokens, contrast report |
| **compare** | Compare theme approaches | Side-by-side of CSS vars vs CSS-in-JS vs Style Dictionary vs Tailwind v4 `@theme` |
| **refactor** | Migrate existing app to semantic tokens | Audit hardcoded colors → extract tokens → create `:root`/`.light` → replace across components |
| **test** | Contrast checks + token coverage | Automated WCAG AA validation, token coverage scan (find hardcoded colors), system pref test |
| **debug** | Fix theme inconsistencies | Flash-of-wrong-theme, missing dark/light overrides, SVG not responding, contrast failures |
| **document** | Generate token docs | Visual token catalog, contrast ratio table, usage examples per token |

---

## 7. Keyword Differentiation from `frontend-only`

| Query | Expected Route | Rationale |
|-------|---------------|-----------|
| "Build a React app" | `frontend-only` | General frontend |
| "Add dark mode to my app" | `ui-theme-architect` | Theming specialization |
| "Create a design token system" | `ui-theme-architect` | Core capability |
| "Fix WCAG contrast issues" | `ui-theme-architect` | Contrast validation |
| "Set up Tailwind CSS" | `frontend-only` | General styling |
| "Create CSS custom properties for theming" | `ui-theme-architect` | Explicit theming |
| "Build a component library" | `frontend-only` | Component scaffolding |
| "SVG won't change color in dark mode" | `ui-theme-architect` | SVG theme resolution |

**Routing conflict risk**: LOW — keywords are distinct (`theme`, `dark-mode`, `semantic-tokens`, `wcag-contrast` vs `react`, `routing`, `state`, `component`).

---

## 8. Implementation Approach

### Phase 1: Constitution
1. Read BluePearl reference implementation files
2. Extract patterns into hard-stop rules, mandatory patterns, recommended patterns
3. Incorporate industry gaps (no-FOUC, reduced motion, contrast validation)
4. Define refusal template for requests outside scope

### Phase 2: Workflows
1. **scaffold** first — most complex, establishes all deliverables
2. **test** second — validates scaffold output (contrast gate)
3. **refactor** third — most common real-world use case
4. **compare**, **debug**, **document** — follow standard patterns

### Phase 3: Validation
1. Run scaffold on a fresh React + Tailwind v4 project
2. Verify all 9 key deliverables produced
3. Run test workflow to validate contrast compliance
4. Run refactor workflow on a project with hardcoded colors

---

## 9. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Framework coupling (React-only) | High | Constitution must be framework-agnostic for token system; hooks are React-specific but pattern is portable |
| Tailwind v4 `@theme` too new | Medium | Provide fallback for Tailwind v3 `theme.extend` and vanilla CSS |
| WCAG contrast tooling varies | Low | Recommend specific tools (axe-core, Contrast Checker API) in test workflow |
| Overlap with `frontend-only` styling section | Medium | Clear scope boundary: `frontend-only` handles CSS framework setup, `ui-theme-architect` handles semantic token architecture |

---

*This document guides the creation of the `ui-theme-architect` archetype. Review and approve before proceeding with constitution and workflow authoring.*
