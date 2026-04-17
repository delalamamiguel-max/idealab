# Changelog — UI Theme Architect

## 1.0.0 (2026-03-02)

### Added

- **Constitution** (`ui-theme-architect-constitution.md`): 849 lines covering 8 sections
  - 6 hard-stop rules: no hardcoded colors, semantic naming, WCAG AA contrast, system preference, theme parity, CSS as source of truth
  - 7 mandatory patterns: token architecture, theme hook, SVG resolution hook, syntax tokens, chrome theming, component variants, Tailwind registration
  - 6 preferred patterns: no-FOUC script, reduced motion, high contrast, token docs, color-mix() variants, multi-brand abstraction
  - Token inventory with 20 core + 10 extended tokens
  - Troubleshooting guide with 6 common issues
  - Security and performance checklist
  - Refusal template with example
- **Scaffold workflow** (`scaffold-ui-theme-architect.md`): Full theme system generation with requirements gathering, token CSS, hooks, component variants, and validation
- **Compare workflow** (`compare-ui-theme-architect.md`): Side-by-side evaluation of theming approaches with constitution-aligned criteria and 4 pre-built comparison tables
- **Refactor workflow** (`refactor-ui-theme-architect.md`): Hardcoded color audit, semantic token extraction, component migration, and post-refactor validation
- **Test workflow** (`test-ui-theme-architect.md`): 10-category validation covering contrast ratios, token parity, hardcoded color scans, system preference detection, and framework registration
- **Debug workflow** (`debug-ui-theme-architect.md`): 8-category issue diagnosis with diagnostic commands, common solutions, and structured debug reports
- **Document workflow** (`document-ui-theme-architect.md`): Token catalog, contrast report, architecture guide, migration guide, and component token map generation
- **Manifest** (`manifest.yaml`): 13 keywords, constitution path, all 6 workflow entries
- **README** (`README.md`): Workflow table, key deliverables, constitution highlights, reference implementation links
