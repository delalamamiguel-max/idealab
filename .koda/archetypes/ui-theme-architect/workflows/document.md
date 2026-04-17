---
description: Generate comprehensive token documentation including visual catalog, contrast ratio tables, usage examples, and architecture guides
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read documentation standards from:
`${ARCHETYPES_BASEDIR}/ui-theme-architect/ui-theme-architect-constitution.md`

### 2. Identify Documentation Scope

Based on $ARGUMENTS, determine which documents to generate:

| Document | Purpose | Audience |
|----------|---------|----------|
| **Token Catalog** | Visual reference of all tokens with swatches | Developers, Designers |
| **Contrast Report** | WCAG AA compliance evidence for all token pairs | Accessibility team, QA |
| **Architecture Guide** | How the token system is structured and why | New developers |
| **Migration Guide** | Steps for adding new tokens or modifying existing ones | Maintenance developers |
| **Component Token Map** | Which tokens each component consumes | UI developers |
| **Brand Customization Guide** | How to create brand variants | Platform team |

### 3. Generate Token Catalog

Create a visual token reference document.

**Deliverable**: `docs/theme/token-catalog.md` or equivalent

**Structure per token**:

```text
### --background

| Property | Dark Mode | Light Mode |
|----------|-----------|------------|
| Value | oklch(0.145 0.014 265.1) | oklch(0.985 0.002 247) |
| Usage | Page and application background | Page and application background |
| Paired with | --foreground | --foreground |
| Contrast ratio | 12.3:1 (with foreground) | 14.1:1 (with foreground) |

**Usage examples**:
- `bg-background` — page body
- `bg-background/50` — semi-transparent overlay
```

**Include all 20 core tokens + any extended tokens defined in the project.**

### 4. Generate Contrast Report

Create an accessibility compliance document.

**Deliverable**: `docs/theme/contrast-report.md`

**Content**:

1. **Summary table**: All foreground/background pairs with computed contrast ratios for both dark and light modes
2. **Pass/Fail status**: WCAG 2.1 AA compliance per pair
3. **Methodology**: How contrast was calculated (oklch to sRGB to relative luminance)
4. **Recommendations**: Any pairs that are close to the minimum threshold and should be monitored

### 5. Generate Architecture Guide

Create a technical overview of the theme system.

**Deliverable**: `docs/theme/architecture.md`

**Sections**:

1. **Overview**: Dark-first `:root` / `html.light` pattern explanation
2. **Token Naming Convention**: `--{role}` and `--{role}-{modifier}` patterns with examples
3. **File Structure**: Where tokens are defined, where hooks live, where registration happens
4. **Mode Switching Flow**: Diagram showing localStorage → hook → DOM class → CSS cascade
5. **Framework Integration**: How Tailwind `@theme` (or config) connects to CSS custom properties
6. **SVG/Canvas Theming**: How non-CSS rendering contexts resolve colors at runtime
7. **Adding New Tokens**: Step-by-step checklist for introducing a new semantic token
8. **Accessibility Requirements**: Contrast ratio rules and validation process

### 6. Generate Migration Guide

Create a maintenance reference for token changes.

**Deliverable**: `docs/theme/migration-guide.md`

**Content**:

1. **Adding a New Token**: Steps to add to `:root`, `html.light`, `@theme`, and component usage
2. **Modifying a Token Value**: How to change a color while maintaining contrast compliance
3. **Removing a Token**: How to deprecate and remove safely with grep-based usage scanning
4. **Upgrading Tailwind Version**: Migration from v3 config to v4 `@theme` block
5. **Adding a New Theme Mode**: How to extend beyond dark/light (e.g., high-contrast, sepia)

### 7. Generate Component Token Map (If Requested)

Create a cross-reference of which tokens each component consumes.

**Deliverable**: `docs/theme/component-token-map.md`

**Method**: Scan component files for semantic token utility classes and map them back to CSS custom properties.

**Format**:

```text
| Component | Tokens Used |
|-----------|-------------|
| Button (primary) | --primary, --primary-foreground, --ring |
| Button (destructive) | --destructive, --destructive-foreground, --ring |
| Card | --card, --card-foreground, --border |
| Input | --background, --foreground, --input, --ring |
| Badge (default) | --primary, --primary-foreground |
| Alert (info) | --info, --info-foreground, --border |
| Sidebar | --sidebar, --sidebar-foreground, --sidebar-border |
```

### 8. Compile Documentation Package

Assemble all generated documents into a cohesive package:

```text
docs/theme/
├── README.md                # Index with links to all theme docs
├── token-catalog.md         # Visual token reference
├── contrast-report.md       # WCAG compliance evidence
├── architecture.md          # Technical overview
├── migration-guide.md       # Maintenance reference
└── component-token-map.md   # Token usage cross-reference (optional)
```

Create the `docs/theme/README.md` index file linking to all documents with brief descriptions.

---

## Post-Documentation Checklist

```text
✅ Token catalog with all defined tokens
✅ Contrast report with WCAG AA pass/fail per pair
✅ Architecture guide with mode switching flow
✅ Migration guide for common maintenance tasks
✅ Index README linking all documents

🔧 Next Steps:
1. Review contrast report for any near-threshold pairs
2. Share architecture guide with new team members
3. Include contrast report in accessibility audit package
```

---

## Error Handling

**No Token File Found**: Report that no theme system exists. Recommend running `/scaffold-ui-theme-architect` before generating documentation.

**Partial Theme System**: Generate documentation for what exists, and add a "Missing" section listing tokens or patterns that should be added to reach full compliance.

**Large Component Set**: For projects with 100+ components, generate the component token map for shared UI primitives only (buttons, inputs, cards, alerts, badges) unless full coverage is explicitly requested.

## Examples

### Example 1: Full Documentation Package
```text
/document-ui-theme-architect "
Generate complete theme documentation for our React dashboard.
Token file: src/index.css
Components: src/components/ui/
Include contrast report for accessibility audit.
"
```

### Example 2: Token Catalog Only
```text
/document-ui-theme-architect "
Generate a visual token catalog for our design team.
They need color swatches, oklch values, and usage examples
for all semantic tokens in both dark and light modes.
"
```

### Example 3: Architecture Guide for Onboarding
```text
/document-ui-theme-architect "
New developers joining the team need to understand our theme system.
Generate an architecture guide explaining the dark-first pattern,
how to add new tokens, and how the Tailwind integration works.
"
```

---

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/ui-theme-architect/ui-theme-architect-constitution.md`
- **Related**: scaffold-ui-theme-architect, test-ui-theme-architect
