---
description: Generate comprehensive documentation for a Flywheel frontend project including component catalog, usage patterns, integration guides, and architecture overview
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read documentation standards from:
`${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/flywheel-frontend-architect-constitution.md`

### 2. Identify Documentation Scope

Based on $ARGUMENTS, determine which documents to generate:

| Document | Purpose | Audience |
|----------|---------|----------|
| **Component Catalog** | Installed components with usage examples | Developers |
| **Architecture Guide** | Project structure, patterns, conventions | New developers |
| **Theme Guide** | Brand themes, dark mode, token usage | Developers, Designers |
| **Icon Reference** | Available icons, usage patterns, accessibility | Developers |
| **API Integration Guide** | Fetch patterns, React Query setup, typed clients | Full-stack developers |
| **AGENTS.md** | AI workspace instructions for coding assistants | AI tools |
| **Contributing Guide** | How to add components and maintain standards | Team contributors |

### 3. Generate Component Catalog

Scan `src/components/ui/` to build a catalog of installed components.

**Deliverable**: `docs/components.md`

**Structure**:

```markdown
# Component Catalog

## Installed Components

| Component | Category | Custom Flywheel | Install Command |
|-----------|----------|----------------|-----------------|
| Button | Input | No | `npx shadcn add @forge/button` |
| Card | Display | No | `npx shadcn add @forge/card` |
| Autocomplete | Input | Yes | `npx shadcn add @forge/autocomplete` |
| Top Navigation | Navigation | Yes | `npx shadcn add @forge/top-navigation` |
| ... | ... | ... | ... |

## Usage Examples

### Button
{code example with all variants}

### Card
{code example with header, content, footer}

...
```

**Method**:
```bash
# List all installed components
ls src/components/ui/ | sed 's/.tsx$//'
```

For each component, generate a usage example based on the Flywheel documentation patterns.

### 4. Generate Architecture Guide

**Deliverable**: `docs/architecture.md`

**Sections**:

1. **Overview**: Technology stack and rationale
2. **Directory Structure**: Explanation of `components/ui/`, `components/blocks/`, `components/features/`, `lib/`, `styles/`
3. **CSS Architecture**: globals.css layered structure explanation
4. **Token Flow**: How `@forge/ui-tokens` → `@theme inline` → Tailwind utilities → components
5. **Component Patterns**: CVA variants, compound composition, slot-based architecture
6. **State Management**: Server state, client state, form state, URL state
7. **API Integration**: Fetch wrappers, React Query patterns, error handling
8. **Testing Strategy**: Component tests, accessibility checks, compliance scans

```markdown
# Architecture Guide

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Framework | React 19 | UI rendering |
| Build | Vite 6 | Dev server and bundling |
| Language | TypeScript 5.8 | Type safety |
| Styling | Tailwind CSS 4 | Utility-first CSS |
| Tokens | @forge/ui-tokens | AT&T brand theming |
| Icons | @flywheel/react-icons | 1400+ AT&T icons |
| Primitives | @base-ui/react | Headless UI primitives |
| Variants | class-variance-authority | Component variant management |

## CSS Architecture

The styling system follows a layered architecture in `globals.css`:

\`\`\`
Layer 1: Tailwind v4 core (@import "tailwindcss")
Layer 2: Animation utilities (@import "tw-animate-css")
Layer 3: Base UI keyframes + radius scale
Layer 4: Data-attribute variants (data-open, data-closed, etc.)
Layer 5: Flywheel tokens (@import "@forge/ui-tokens")
Layer 6: Dark mode variant
Layer 7: Token → Tailwind utility mapping (@theme inline)
Layer 8: Base defaults (font, border, body)
Layer 9: Root radius token
\`\`\`

## Token Flow

\`\`\`
@forge/ui-tokens
  └─ Brand primitives (--fw-att-blue, --fw-cobalt-*)
  └─ Theme files (business / firstnet / consumer)
       └─ shadcn vars (--background, --primary, --border)
            └─ @theme inline → Tailwind utilities
                 └─ Components (bg-primary, text-foreground)
\`\`\`
```

### 5. Generate Theme Guide

**Deliverable**: `docs/theming.md`

**Content**:

1. **Available Themes**: Business, FirstNet, Consumer with visual descriptions
2. **Theme Switching**: How to apply theme classes at runtime
3. **Dark Mode**: `.dark` class usage and combination with brand themes
4. **Token Reference**: Table of all available semantic tokens (`--primary`, `--background`, etc.)
5. **Customization**: How to override specific token values if needed
6. **Best Practices**: Use semantic utilities, avoid hardcoded colors, document exceptions

### 6. Generate Icon Reference

**Deliverable**: `docs/icons.md`

**Content**:

1. **Import Pattern**: `import { NameIcon } from "@flywheel/react-icons"`
2. **Size Variants**: 16px, 24px (default), 32px, 64px, 96px
3. **Accessibility**: `aria-label` for icon buttons, `title` for meaningful icons
4. **Color**: `currentColor` inheritance, className overrides
5. **Finding Icons**: MCP `forge_get_icon()`, online gallery at forge.dev.att.com
6. **Common Icons**: Table of frequently used icons with import names

```markdown
## Common Icons

| Purpose | Import | Size |
|---------|--------|------|
| Close | `CloseIcon16` | 16px |
| Search | `SearchIcon` | 24px |
| Menu | `MenuIcon` | 24px |
| Bell / Notifications | `BellIcon` | 24px |
| User / Profile | `UserIcon` | 24px |
| Settings | `SettingsIcon` | 24px |
| Chevron Down | `ChevronDownIcon16` | 16px |
| Arrow Right | `ArrowRightIcon` | 24px |
| Check | `CheckIcon` | 24px |
| Warning | `WarningIcon` | 24px |
```

### 7. Generate API Integration Guide (If Applicable)

**Deliverable**: `docs/api-integration.md`

**Content**:

1. **Typed API Client Pattern**: `src/lib/api/` with typed fetch wrappers
2. **React Query Setup**: Provider, query keys, mutation patterns
3. **Error Handling**: API errors → Alert components, toast notifications
4. **Loading States**: Skeleton components, progress indicators
5. **Environment Variables**: `VITE_API_BASE_URL` configuration
6. **Authentication**: Token management pattern (if auth is configured)

### 8. Generate AGENTS.md (If Requested)

**Deliverable**: `AGENTS.md` at project root

Generate workspace instructions for AI coding assistants following the pattern from the reference implementation:

```markdown
# {Project Name} — Flywheel Workspace

This project uses the Flywheel design system by AT&T.

## Rules

- **Icons**: Use `@flywheel/react-icons` only. **Never use `lucide-react`** (legally prohibited).
- **Theming**: Use `@forge/ui-tokens`. Theme classes: `.theme-consumer`, `.theme-business`, `.theme-firstnet` on `<html>`.
- **Tailwind**: v4, bare utility classes (no `tw-` prefix).
- **Components**: Install from Forge registry via `npx shadcn add @forge/<name>`.

## Adding Components

\`\`\`bash
npx shadcn add @forge/button
npx shadcn add @forge/dialog
# ... list installed components
\`\`\`

## MCP Workflow

\`\`\`
1. forge_search("query")           → discover components
2. forge_get_component("name")     → get source + install
3. forge_get_icon("description")   → find icons
4. forge_get_page("topic")         → read docs
\`\`\`

## Available Components
{list all installed components}
```

### 9. Generate Contributing Guide (If Requested)

**Deliverable**: `docs/contributing.md`

**Content**:

1. **Adding a Component**: `npx shadcn add @forge/<name>`, verify in `src/components/ui/`
2. **Creating Custom Components**: CVA pattern, semantic tokens only, TypeScript typed props
3. **Icon Rules**: @flywheel/react-icons only, accessibility requirements
4. **Color Rules**: Semantic tokens only, THEME_EXCEPTIONS.md for intentional literals
5. **Code Review Checklist**: Pre-commit checks derived from test workflow

### 10. Compile Documentation Package

Assemble all generated documents:

```text
docs/
├── components.md         # Installed component catalog
├── architecture.md       # Technical overview
├── theming.md            # Brand themes and tokens
├── icons.md              # Icon reference
├── api-integration.md    # API patterns (if applicable)
└── contributing.md       # Team standards (if requested)

AGENTS.md                 # AI workspace instructions (at project root)
```

---

## Error Handling

- **No components installed**: Generate catalog of available (not yet installed) components instead
- **No API integration**: Skip API guide, note it as future work
- **Custom components present**: Include them in the catalog with "[Custom]" tag
- **Monorepo**: Ask which package to document

## Examples

### Example 1: Full Documentation
```
/document-flywheel-frontend-architect Generate complete documentation including component catalog, architecture guide, theme guide, and AGENTS.md
```

### Example 2: Component Catalog Only
```
/document-flywheel-frontend-architect Generate a component catalog showing all installed Flywheel components with usage examples
```

### Example 3: Onboarding Docs
```
/document-flywheel-frontend-architect Generate architecture and contributing guides for new team members joining the project
```

## References

- Constitution: `${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/flywheel-frontend-architect-constitution.md`
- Forge docs: https://forge.dev.att.com
