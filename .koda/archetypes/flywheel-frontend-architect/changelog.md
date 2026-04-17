# Changelog — Flywheel Frontend Architect

## 1.0.0 (2026-03-17)

### Added

- **Constitution** (`flywheel-frontend-architect-constitution.md`): Comprehensive guardrails covering 7 sections
  - 6 hard-stop rules: @flywheel/react-icons only (legal), @forge registry prefix, @forge/ui-tokens required, no hardcoded colors, WCAG 2.1 AA, TypeScript strict
  - 10 mandatory patterns: Vite scaffold, globals.css layered structure, component architecture, cn() utility, form pattern (RHF+Zod), theme application, icon usage, MCP config, CVA variants, entry point
  - 8 preferred patterns: pre-built blocks, MCP-first discovery, Heading for responsive text, compound composition, Surface for containers, Toast for feedback, state management, Price display
  - Complete component reference (7 custom + 46 themed + pre-built blocks)
  - Full-stack integration patterns (API layer, React Query, env vars)
  - Troubleshooting guide with 6 common issues
  - Refusal template with example
- **Scaffold workflow** (`scaffold-flywheel-frontend-architect.md`): Full project generation with requirements gathering, component selection, layout composition, theme configuration, and MCP setup
- **Compare workflow** (`compare-flywheel-frontend-architect.md`): Side-by-side evaluation of component choices, layout strategies, and form patterns with Flywheel-aligned criteria
- **Refactor workflow** (`refactor-flywheel-frontend-architect.md`): Migration audit (lucide-react, hardcoded colors, missing @forge prefix), component replacement, token adoption, and compliance validation
- **Test workflow** (`test-flywheel-frontend-architect.md`): 8-category compliance validation covering prohibited imports, registry usage, token compliance, hardcoded colors, accessibility, TypeScript, MCP config, and component architecture
- **Debug workflow** (`debug-flywheel-frontend-architect.md`): 8-category issue diagnosis with diagnostic commands, common fixes, and structured debug reports
- **Document workflow** (`document-flywheel-frontend-architect.md`): Component catalog, usage patterns, integration guides, and architecture documentation generation
- **Manifest** (`manifest.yaml`): 15 keywords, constitution path, all 6 workflow entries
- **README** (`README.md`): Workflow table, deliverables, technology stack, component catalog, related archetypes
- **Templates** (`templates/`): env-config.yaml for project scaffolding
- **Scripts** (`scripts/`): validate-compliance.py for automated compliance checking
