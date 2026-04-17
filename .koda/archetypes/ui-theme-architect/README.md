# UI Theme Architect

Design and implement comprehensive semantic token theming systems with dark/light/system mode switching, CSS custom properties, WCAG 2.1 AA contrast compliance, syntax highlighting theming, SVG/canvas theme awareness, and reduced motion support.

## Status

**Complete** — Constitution, all 6 workflows, and manifest finalized.

## Workflows

| Workflow | Command | Purpose |
|----------|---------|---------|
| **Scaffold** | `/scaffold-ui-theme-architect` | Generate a complete semantic token theming system from scratch |
| **Compare** | `/compare-ui-theme-architect` | Compare theming approaches (CSS vars vs CSS-in-JS, oklch vs hsl, etc.) |
| **Refactor** | `/refactor-ui-theme-architect` | Migrate existing hardcoded colors to semantic tokens |
| **Test** | `/test-ui-theme-architect` | Validate WCAG contrast, token parity, and hardcoded color scans |
| **Debug** | `/debug-ui-theme-architect` | Diagnose FOUC, SVG color bugs, contrast failures, parity mismatches |
| **Document** | `/document-ui-theme-architect` | Generate token catalog, contrast report, and architecture guide |

## Key Deliverables

- CSS token file with 20+ semantic tokens in dark-first `:root` / `html.light` architecture
- Theme application hook with live `prefers-color-scheme` system preference detection
- SVG/canvas theme resolution hook via `getComputedStyle` + `MutationObserver`
- Syntax highlighting token set (10-25 tokens for code rendering)
- Tailwind v4 `@theme` registration (or v3 config equivalent)
- WCAG 2.1 AA contrast validation for all foreground/background pairs
- No-FOUC initialization script for SSR/SSG frameworks

## Constitution Highlights

- **6 Hard-Stop Rules**: No hardcoded colors, semantic naming only, WCAG AA contrast, system preference detection, theme parity, CSS as single source of truth
- **7 Mandatory Patterns**: Token architecture, theme hook, SVG resolution hook, syntax tokens, chrome theming, component variants, Tailwind registration
- **6 Preferred Patterns**: No-FOUC script, reduced motion, high contrast, token docs, color-mix() variants, multi-brand abstraction

## Reference Implementation

BluePearl's own frontend theming system serves as the battle-tested reference:

- `frontend/src/index.css` — 40+ semantic tokens, `@theme` registration, scrollbar/selection/focus theming
- `frontend/src/lib/hooks/use-theme.ts` — Theme application with Zustand + matchMedia
- `frontend/src/lib/hooks/use-theme-colors.ts` — SVG/canvas runtime color resolution

## Related Archetypes

- `frontend-only` — Generic frontend scaffolding (routing, state, components — no theming specialization)
- `app-maker` — Full-stack web application generation
