# Flywheel Frontend Architect

Build Flywheel-compliant web application frontends using AT&T's enterprise design system. Leverages 60+ themed components from the Forge registry, `@flywheel/react-icons`, `@forge/ui-tokens` for multi-brand theming, and `@forge/mcp` for AI-assisted development.

## Status

**Complete** — Constitution, all 6 workflows, manifest, scripts, and templates finalized.

## Workflows

| Workflow | Command | Purpose |
|----------|---------|---------|
| **Scaffold** | `/scaffold-flywheel-frontend-architect` | Create a new Flywheel project or add Flywheel to an existing project |
| **Compare** | `/compare-flywheel-frontend-architect` | Compare component choices, layout patterns, and integration strategies |
| **Refactor** | `/refactor-flywheel-frontend-architect` | Migrate existing frontend to Flywheel compliance |
| **Test** | `/test-flywheel-frontend-architect` | Validate Flywheel compliance (icons, registry, tokens, a11y) |
| **Debug** | `/debug-flywheel-frontend-architect` | Diagnose Flywheel-specific issues (themes, components, tokens, icons) |
| **Document** | `/document-flywheel-frontend-architect` | Generate component catalog, usage docs, and integration guides |

## Key Deliverables

- Vite + React 19 + Tailwind v4 + TypeScript project scaffold
- `components.json` configured with Forge registry (`https://forge.dev.att.com/r/{name}.json`)
- `globals.css` with layered CSS foundation (Tailwind → tokens → theme inline → base)
- 60+ Flywheel components installable via `npx shadcn add @forge/<name>`
- `@flywheel/react-icons` with 1400+ AT&T brand icons
- Multi-brand theming (Business, FirstNet, Consumer) via `@forge/ui-tokens`
- Dark mode via `.dark` CSS class
- MCP configuration for AI-assisted development
- Full-stack integration patterns (API layer, React Query, typed clients)

## Constitution Highlights

- **6 Hard-Stop Rules**: No lucide-react (legally prohibited), @forge prefix required, @forge/ui-tokens required, no hardcoded colors, WCAG 2.1 AA, TypeScript strict
- **10 Mandatory Patterns**: Vite scaffold, globals.css structure, component architecture, cn() utility, form pattern, theme application, icon usage, MCP config, CVA variants, entry point
- **8 Preferred Patterns**: Pre-built blocks, MCP-first discovery, Heading for responsive text, compound composition, Surface for containers, Toast for feedback, state management, Price for monetary display

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Framework | React | 19+ |
| Build | Vite | 6+ |
| Language | TypeScript | 5.8+ |
| Styling | Tailwind CSS | 4+ |
| Tokens | `@forge/ui-tokens` | 0.0.2+ |
| Icons | `@flywheel/react-icons` | 0.0.5+ |
| Primitives | `@base-ui/react` | 1.2+ |
| Variants | `class-variance-authority` | 0.7+ |

## Component Catalog

### Custom Flywheel (7)
Autocomplete, Heading, Price, Surface, Swatch, Top Navigation, Tree View

### Themed shadcn (46+)
Accordion, Alert, Alert Dialog, Aspect Ratio, Avatar, Badge, Bottom Sheet, Breadcrumb, Button, Calendar, Card, Carousel, Chart, Checkbox, Collapsible, Command, Context Menu, Date Picker, Dialog, Drawer, Dropdown Menu, Form, Hover Card, Input, Input OTP, Label, Menubar, Navigation Menu, Pagination, Popover, Progress, Radio Group, Resizable, Scroll Area, Select, Separator, Sheet, Sidebar, Skeleton, Slider, Sonner, Switch, Table, Tabs, Textarea, Toast, Toggle, Toggle Group, Tooltip

## Related Archetypes

| Archetype | Relationship |
|-----------|-------------|
| `frontend-only` | Generic frontend scaffolding — no Flywheel knowledge |
| `ui-theme-architect` | Custom token/theme creation — delegates here for Flywheel-specific tokens |
| `backend-only` | API and backend services — pairs with this archetype for full-stack |
| `app-maker` | Full-stack orchestration — can delegate frontend to this archetype |
| `dev-ops-engineer` | CI/CD and deployment — builds/deploys the Flywheel frontend |
