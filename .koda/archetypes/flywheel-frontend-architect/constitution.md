# Flywheel Frontend Architect Constitution

## Purpose

This constitution defines enforceable guardrails and operational standards for building web application frontends using the **Flywheel design system** — AT&T's enterprise component library built on shadcn/ui. All generated code, component usage, theming configuration, and project scaffolding must comply with these rules.

**Core Focus Areas**:

- Flywheel component installation and composition using the Forge registry (`npx shadcn add @forge/<name>`)
- AT&T brand theming via `@forge/ui-tokens` with multi-brand support (Business, FirstNet, Consumer)
- Exclusive use of `@flywheel/react-icons` for all iconography (1400+ AT&T brand icons)
- Tailwind CSS v4 with `@tailwindcss/vite` plugin and `@theme inline` token mapping
- React 19 + TypeScript strict mode with Vite build tooling
- Component architecture following Flywheel patterns (CVA variants, compound composition, semantic tokens)
- AI-assisted development via `@forge/mcp` (Model Context Protocol)
- WCAG 2.1 AA accessibility compliance using Flywheel's built-in accessible primitives
- Full-stack readiness: clean separation of frontend concerns to pair with backend archetypes

---

## I. Hard-Stop Rules (Non-Negotiable)

Violations require the AI agent to refuse, rewrite, or block the requested artifact.

### 1.1 Icons: @flywheel/react-icons Only

- ✘ **NEVER** import from `lucide-react`, `react-icons`, `heroicons`, `phosphor-react`, `@radix-ui/react-icons`, or any other icon library
- ✘ **NEVER** use inline SVG icon definitions when an equivalent exists in `@flywheel/react-icons`
- ✘ **NEVER** reference icon names or APIs from prohibited libraries in comments, documentation, or type definitions
- ✔ **ALWAYS** import icons from `@flywheel/react-icons` using the `{Name}Icon{Size?}` naming pattern
- ✔ **ALWAYS** use size-specific imports when available (`BellIcon16` for 16px, `BellIcon` for 24px default, `BellIcon96` for 96px)
- ✔ **ALWAYS** provide `aria-label` on icon-only buttons and `title` prop on meaningful icons

**Rationale**: AT&T has a legal prohibition on `lucide-react`. The `@flywheel/react-icons` package provides 1400+ AT&T brand-approved icons that are tree-shakeable and follow accessibility standards. All Flywheel components reference these icons internally.

**Compliant example**:
```tsx
import { BellIcon, ArrowRightIcon16, CheckCircleIcon } from "@flywheel/react-icons"

<Button variant="ghost" size="icon" aria-label="Notifications">
  <BellIcon />
</Button>
```

**Non-compliant example**:
```tsx
// ✘ PROHIBITED — lucide-react is legally restricted
import { Bell, ArrowRight, CheckCircle } from "lucide-react"
```

### 1.2 Registry: @forge Prefix Required

- ✘ **NEVER** install components from the default shadcn registry (`npx shadcn add button`)
- ✘ **NEVER** install components from `ui.shadcn.com` or any registry other than Forge
- ✘ **NEVER** manually copy-paste component source code from shadcn.com or GitHub
- ✔ **ALWAYS** use the `@forge` prefix: `npx shadcn add @forge/<name>`
- ✔ **ALWAYS** ensure `components.json` includes the Forge registry configuration:

```json
{
  "registries": {
    "@forge": {
      "url": "https://forge.dev.att.com/r/{name}.json"
    }
  }
}
```

**Rationale**: The Forge registry delivers Flywheel-themed versions of shadcn components that use `@forge/ui-tokens`, `@base-ui/react` primitives, and AT&T-specific modifications. Default shadcn components lack brand theming, use Radix instead of Base UI, and may bundle `lucide-react`.

### 1.3 Tokens: @forge/ui-tokens Required

- ✘ **NEVER** define custom CSS custom property token systems when `@forge/ui-tokens` provides the needed values
- ✘ **NEVER** use raw Tailwind palette utilities (`text-blue-500`, `bg-slate-900`, `border-zinc-700`) in application components
- ✘ **NEVER** hardcode color values (`#009FDB`, `rgb(0, 159, 219)`, `hsl(195, 100%, 43%)`) in component styles
- ✔ **ALWAYS** consume semantic CSS custom properties through Tailwind utilities: `bg-background`, `text-foreground`, `text-primary`, `border-border`
- ✔ **ALWAYS** import `@forge/ui-tokens` in `globals.css`
- ✔ **ALWAYS** wrap CSS variable references in `rgb()` for the `@theme inline` block

**Rationale**: `@forge/ui-tokens` is the single source of truth for AT&T brand colors, typography, and spacing. It maps brand primitives (`--fw-att-blue`, `--fw-cobalt-*`) to shadcn semantic variables (`--primary`, `--background`) which are then exposed as Tailwind utilities via `@theme inline`.

**Token flow**:
```
@forge/ui-tokens
  └─ Brand primitives (--fw-att-blue, --fw-cobalt-*, --fw-light-blue, ...)
  └─ Theme files (default.css / business.css / firstnet.css)
       └─ Map --fw-* → shadcn vars (--background, --primary, --border, ...)
            └─ @theme inline → Tailwind utilities (bg-background, text-primary, ...)
                 └─ Components consume via CVA (bg-primary text-primary-foreground)
```

### 1.4 No Hardcoded Colors in Components

- ✘ **NEVER** embed raw color literals in component source files
- ✘ **NEVER** reference Tailwind palette utilities (`text-blue-500`, `bg-red-600`) in application components
- ✘ **NEVER** apply inline `style` objects containing literal color values
- ✔ **ALWAYS** use semantic token utilities (`bg-background`, `text-primary`, `border-border`, `text-muted-foreground`)
- ✔ **ALWAYS** document intentional exceptions (data-visualization categorical palettes, AT&T brand logos) in a `THEME_EXCEPTIONS.md` file

**Compliant example**:
```tsx
<Card className="bg-card text-card-foreground">
  <CardHeader>
    <CardTitle className="text-foreground">Dashboard</CardTitle>
    <CardDescription className="text-muted-foreground">Overview</CardDescription>
  </CardHeader>
</Card>
```

**Non-compliant example**:
```tsx
{/* ✘ Raw palette colors break theme switching */}
<Card className="bg-white text-gray-900 dark:bg-gray-800 dark:text-white">
  <CardTitle className="text-blue-600">Dashboard</CardTitle>
</Card>
```

### 1.5 Accessibility — WCAG 2.1 AA Compliance

- ✘ **NEVER** ship UI without semantic HTML, keyboard navigation, and appropriate ARIA attributes
- ✘ **NEVER** use `div` or `span` for interactive elements — use `button`, `a`, `input`, or Flywheel's accessible primitives
- ✘ **NEVER** omit `aria-label` on icon-only buttons or controls without visible text
- ✘ **NEVER** skip focus management for dialogs, modals, sheets, and drawers
- ✔ **ALWAYS** use Flywheel components which have built-in accessibility (ARIA roles, keyboard navigation, focus trapping)
- ✔ **ALWAYS** maintain heading hierarchy (`h1` → `h2` → `h3`, no skipped levels) using the Heading component
- ✔ **ALWAYS** provide meaningful alt text for images and `title` for meaningful icons
- ✔ **ALWAYS** ensure minimum touch target of 44×44px for interactive elements

### 1.6 TypeScript Strict Mode

- ✘ **NEVER** use `any` type — use `unknown` with type guards if the type is truly unknown
- ✘ **NEVER** use `@ts-ignore` or `@ts-expect-error` without a comment explaining why
- ✔ **ALWAYS** type all component props with explicit interfaces or types
- ✔ **ALWAYS** enable `strict: true` in `tsconfig.json`

---

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns in all generated code.

### 2.1 Project Scaffolding — Vite + React 19 + Tailwind v4 + TypeScript

Every new Flywheel project must follow this technology stack:

**Required `package.json` dependencies**:
```json
{
  "dependencies": {
    "@base-ui/react": "^1.2.0",
    "@flywheel/react-icons": "^0.0.5",
    "@forge/ui-tokens": "^0.0.2",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "tailwind-merge": "^3.5.0",
    "tw-animate-css": "^1.4.0"
  },
  "devDependencies": {
    "@tailwindcss/vite": "^4.2.1",
    "@vitejs/plugin-react": "^4.4.1",
    "tailwindcss": "^4.2.1",
    "typescript": "^5.8.0",
    "vite": "^6.0.0"
  }
}
```

**Required `vite.config.ts`**:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '@': path.resolve(__dirname, './src') } },
})
```

**Required `components.json`**:
```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "flywheel",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/styles/globals.css",
    "baseColor": "",
    "cssVariables": true,
    "prefix": ""
  },
  "iconLibrary": "none",
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "registries": {
    "@forge": {
      "url": "https://forge.dev.att.com/r/{name}.json"
    }
  }
}
```

### 2.2 globals.css — Flywheel CSS Foundation

The `src/styles/globals.css` file must follow this layered structure:

```css
/* === 1. Tailwind v4 core === */
@import "tailwindcss";
@import "tw-animate-css";

/* === 2. Base UI keyframes + radius scale === */
@theme inline {
  @keyframes accordion-down {
    from { height: 0; }
    to { height: var(--accordion-panel-height, auto); }
  }
  @keyframes accordion-up {
    from { height: var(--accordion-panel-height, auto); }
    to { height: 0; }
  }
  @keyframes collapsible-down {
    from { height: 0; }
    to { height: var(--collapsible-panel-height, auto); }
  }
  @keyframes collapsible-up {
    from { height: var(--collapsible-panel-height, auto); }
    to { height: 0; }
  }
  --radius-sm: calc(var(--radius) * 0.6);
  --radius-md: calc(var(--radius) * 0.8);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) * 1.4);
  --radius-2xl: calc(var(--radius) * 1.8);
  --radius-3xl: calc(var(--radius) * 2.2);
  --radius-4xl: calc(var(--radius) * 2.6);
}

/* === 3. Custom data-attribute variants for Base UI === */
@custom-variant data-open { &:where([data-state="open"]), &:where([data-open]:not([data-open="false"])) { @slot; } }
@custom-variant data-closed { &:where([data-state="closed"]), &:where([data-closed]:not([data-closed="false"])) { @slot; } }
@custom-variant data-checked { &:where([data-state="checked"]), &:where([data-checked]:not([data-checked="false"])) { @slot; } }
@custom-variant data-unchecked { &:where([data-state="unchecked"]), &:where([data-unchecked]:not([data-unchecked="false"])) { @slot; } }
@custom-variant data-selected { &:where([data-selected="true"]) { @slot; } }
@custom-variant data-disabled { &:where([data-disabled="true"]), &:where([data-disabled]:not([data-disabled="false"])) { @slot; } }
@custom-variant data-active { &:where([data-state="active"]), &:where([data-active]:not([data-active="false"])) { @slot; } }
@custom-variant data-horizontal { &:where([data-orientation="horizontal"]) { @slot; } }
@custom-variant data-vertical { &:where([data-orientation="vertical"]) { @slot; } }

/* === 4. Scrollbar utility === */
@utility no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
  &::-webkit-scrollbar { display: none; }
}

/* === 5. Flywheel design tokens === */
@import "@forge/ui-tokens";

/* === 6. Dark mode variant === */
@custom-variant dark (&:is(.dark *));

/* === 7. shadcn CSS vars → Tailwind v4 color utilities === */
@theme inline {
  --color-background: rgb(var(--background));
  --color-foreground: rgb(var(--foreground));
  --color-card: rgb(var(--card));
  --color-card-foreground: rgb(var(--card-foreground));
  --color-popover: rgb(var(--popover));
  --color-popover-foreground: rgb(var(--popover-foreground));
  --color-primary: rgb(var(--primary));
  --color-primary-foreground: rgb(var(--primary-foreground));
  --color-secondary: rgb(var(--secondary));
  --color-secondary-foreground: rgb(var(--secondary-foreground));
  --color-muted: rgb(var(--muted));
  --color-muted-foreground: rgb(var(--muted-foreground));
  --color-accent: rgb(var(--accent));
  --color-accent-foreground: rgb(var(--accent-foreground));
  --color-destructive: rgb(var(--destructive));
  --color-destructive-foreground: rgb(var(--destructive-foreground));
  --color-border: rgb(var(--border));
  --color-input: rgb(var(--input));
  --color-ring: rgb(var(--ring));
  --color-chart-1: rgb(var(--chart-1));
  --color-chart-2: rgb(var(--chart-2));
  --color-chart-3: rgb(var(--chart-3));
  --color-chart-4: rgb(var(--chart-4));
  --color-chart-5: rgb(var(--chart-5));
  --color-sidebar: rgb(var(--sidebar-background));
  --color-sidebar-foreground: rgb(var(--sidebar-foreground));
  --color-sidebar-primary: rgb(var(--sidebar-primary));
  --color-sidebar-primary-foreground: rgb(var(--sidebar-primary-foreground));
  --color-sidebar-accent: rgb(var(--sidebar-accent));
  --color-sidebar-accent-foreground: rgb(var(--sidebar-accent-foreground));
  --color-sidebar-border: rgb(var(--sidebar-border));
  --color-sidebar-ring: rgb(var(--sidebar-ring));
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);
}

/* === 8. Base layer — fonts, borders, body === */
@layer base {
  * { @apply border-border outline-ring/50; }
  body {
    @apply bg-background text-foreground;
    font-family: 'ATTAleckSans', sans-serif;
    font-synthesis-weight: none;
    text-rendering: optimizeLegibility;
  }
}

/* === 9. Root radius token === */
:root { --radius: 0.5rem; }
```

### 2.3 Component Architecture — Directory Structure

```
src/
├── components/
│   ├── ui/              # Flywheel primitives (installed via @forge registry)
│   ├── blocks/          # Pre-built compositions (installed or custom)
│   └── features/        # Domain-specific components (custom)
├── lib/
│   ├── utils.ts         # cn() utility
│   ├── api/             # API fetch wrappers, typed clients
│   └── hooks/           # Custom React hooks
├── styles/
│   └── globals.css      # Flywheel CSS foundation (Section 2.2)
├── types/               # Shared TypeScript types
├── App.tsx              # Root component
└── main.tsx             # Entry point
```

### 2.4 Utility Function — cn()

Every project must include the `cn()` utility:

```typescript
// src/lib/utils.ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### 2.5 Form Pattern — React Hook Form + Zod + Flywheel Components

Forms must use the Flywheel form component system with schema-based validation:

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import {
  Form, FormControl, FormField, FormItem,
  FormLabel, FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const schema = z.object({
  email: z.string().email("Invalid email"),
})

type FormValues = z.infer<typeof schema>

function MyForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(schema),
    defaultValues: { email: "" },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  )
}
```

### 2.6 Theme Application — CSS Class on HTML Element

Multi-brand theme switching uses CSS classes on `<html>` or a container element:

```tsx
// Brand themes
document.documentElement.className = 'theme-business'  // AT&T Business
document.documentElement.className = 'theme-firstnet'  // FirstNet
document.documentElement.className = 'theme-consumer'  // AT&T Consumer

// Dark mode (combinable with brand themes)
document.documentElement.classList.add('dark')
document.documentElement.classList.remove('dark')
```

| Theme | Class | Description |
|-------|-------|-------------|
| Consumer | `.theme-consumer` | AT&T Consumer brand |
| Business | `.theme-business` | AT&T Business brand (darker blue) |
| FirstNet | `.theme-firstnet` | FirstNet brand (neutral/gray) |
| Dark | `.dark` | Dark mode (combinable with any brand theme) |

### 2.7 Icon Usage Patterns

```tsx
import { BellIcon, BellIcon16, BellIcon96 } from "@flywheel/react-icons"

// Size via import (preferred)
<BellIcon16 />    {/* 16px — inline text, table cells */}
<BellIcon />      {/* 24px — buttons, navigation (default) */}
<BellIcon96 />    {/* 96px — hero sections, empty states */}

// Size via className (alternative)
<BellIcon className="h-4 w-4" />

// Color — inherits currentColor by default
<CheckCircleIcon className="text-green-600" />

// Accessibility
<Button variant="ghost" size="icon" aria-label="Close">
  <CloseIcon16 />
</Button>
<WarningIcon title="Warning: action required" />  {/* meaningful icon */}
```

### 2.8 MCP Configuration

Projects should include MCP configuration for AI-assisted development:

```json
{
  "servers": {
    "forge": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@forge/mcp"]
    }
  }
}
```

Place in `.vscode/mcp.json` and/or `.cursor/mcp.json`.

### 2.9 Component Variant System — CVA + Semantic Tokens

All custom component variants must use `class-variance-authority` with semantic token utilities only:

```typescript
import { cva, type VariantProps } from 'class-variance-authority'

export const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow-sm hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4",
        xs: "h-6 px-2 text-xs",
        sm: "h-8 px-3 text-xs",
        lg: "h-10 px-6 text-base",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)
```

**Verification**: `grep -rn "text-blue\|bg-blue\|text-red\|bg-red\|text-slate\|bg-slate" src/components/` must return zero matches.

### 2.10 Entry Point Pattern

```tsx
// src/main.tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/globals.css'
import App from './App'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
```

---

## III. Preferred Patterns (Recommended)

The LLM **should adopt** unless the user explicitly overrides.

### 3.1 → Use Pre-Built Blocks Before Custom Layouts

Before building a layout from scratch, check if a Flywheel block exists via MCP:
```
forge_search("sidebar layout")
forge_search("login page")
forge_search("data table")
```

Or install directly:
```bash
npx shadcn add @forge/block-sidebar-01
npx shadcn add @forge/block-login-01
```

### 3.2 → MCP-First Component Discovery

Before building custom components, use MCP to check availability:
```
forge_search("data table")          → Discover existing components
forge_get_component("autocomplete") → Get full API and install command
forge_get_icon("search")            → Find matching icon with import
forge_get_page("theming")           → Learn theme configuration
```

### 3.3 → Responsive Typography with Heading Component

Use Flywheel's `Heading` component for responsive text sizing:

```tsx
import { Heading } from "@/components/ui/heading"

{/* Automatically scales: 5xl mobile → 6xl tablet → 7xl desktop */}
<Heading size="3xl" as="h1">Welcome</Heading>

{/* With eyebrow label */}
<Heading size="xl" as="h2" eyebrow="New Feature">
  Redesigned Dashboard
</Heading>
```

### 3.4 → Compound Component Composition

Follow Flywheel's compound component patterns for complex UI:

**TopNavigation** — slot-based:
```tsx
<TopNavigation>
  <TopNavLogo><img src="/logo.svg" alt="Logo" /></TopNavLogo>
  <TopNavMenu>{/* nav links */}</TopNavMenu>
  <TopNavAction>{/* action buttons */}</TopNavAction>
  <TopNavSub>{/* breadcrumbs */}</TopNavSub>
</TopNavigation>
```

**Sidebar** — nested composition:
```tsx
<SidebarProvider>
  <Sidebar collapsible="icon">
    <SidebarHeader>{/* branding */}</SidebarHeader>
    <SidebarContent>
      <SidebarGroup>
        <SidebarGroupLabel>Navigation</SidebarGroupLabel>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton>Dashboard</SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarGroup>
    </SidebarContent>
    <SidebarFooter>{/* user menu */}</SidebarFooter>
  </Sidebar>
  <main>
    <SidebarTrigger />
    {/* page content */}
  </main>
</SidebarProvider>
```

### 3.5 → Surface Component for Themed Containers

Use the `Surface` component instead of raw `div` elements:

```tsx
import { Surface } from "@/components/ui/surface"

<Surface theme="wash" shadow="md" rounded="2xl">
  <p>Content on a muted background with medium shadow</p>
</Surface>
```

### 3.6 → Toast for User Feedback

Use the Toaster + useToast pattern:

```tsx
import { useToast } from "@/hooks/use-toast"

const { toast } = useToast()
toast({ title: "Success", description: "Changes saved." })
toast({ title: "Error", description: "Failed.", variant: "destructive" })
```

Add `<Toaster />` to the root layout.

### 3.7 → State Management Strategy

- **Server state**: React Query (`@tanstack/react-query`) for API data
- **Client state**: React `useState`/`useReducer` for local; Zustand for shared
- **Form state**: React Hook Form (via `<Form>` component)
- **URL state**: React Router or TanStack Router

### 3.8 → Price Component for Monetary Display

```tsx
import { Price, PriceBlock } from "@/components/ui/price"

<PriceBlock>
  <Price size="sm" strike>79.99</Price>
  <Price size="xl" monthly>49.99</Price>
  <p className="text-muted-foreground text-sm">First 12 months</p>
</PriceBlock>
```

---

## IV. Available Component Reference

### Custom Flywheel Components (7)

| Component | Install Command | Key Features |
|-----------|----------------|--------------|
| Autocomplete | `npx shadcn add @forge/autocomplete` | Searchable dropdown, status indicators, custom rendering, footer slot |
| Heading | `npx shadcn add @forge/heading` | Responsive sizes (3xl–2xs), eyebrow labels, semantic HTML |
| Price | `npx shadcn add @forge/price` | Currency display, strike-through, monthly indicator, PriceBlock |
| Surface | `npx shadcn add @forge/surface` | Themed containers, elevation, border radius, interactive modes |
| Swatch | `npx shadcn add @forge/swatch` | Color selection, radio group pattern, multiple states |
| Top Navigation | `npx shadcn add @forge/top-navigation` | Slot-based app header, sticky, backdrop blur |
| Tree View | `npx shadcn add @forge/tree-view` | Hierarchical data, expand/collapse, lane lines |

### Themed shadcn Components (46)

**Input & Forms**: button, calendar, checkbox, form, input, input-otp, label, radio-group, select, slider, switch, textarea, toggle, toggle-group

**Display & Data**: avatar, badge, card, chart, progress, separator, skeleton, table

**Navigation**: breadcrumb, menubar, navigation-menu, pagination, sidebar, tabs

**Overlay & Feedback**: alert, alert-dialog, bottom-sheet, command, context-menu, date-picker, dialog, drawer, dropdown-menu, hover-card, popover, resizable, scroll-area, sheet, sonner, toast, tooltip

**Layout**: accordion, aspect-ratio, carousel, collapsible

### Pre-Built Blocks

| Block | Description |
|-------|-------------|
| bottom-sheet-01 | Mobile-friendly bottom panel patterns |
| card-patterns | Card layout compositions |
| data-table | Data table with sorting/filtering |
| empty-states | Empty state illustrations and CTAs |
| login-01 | Login form with AT&T branding |
| sidebar-01 | Sidebar navigation layout |
| top-navigation-01 | App header with navigation |

---

## V. Full-Stack Integration Points

When combined with backend archetypes, the Flywheel frontend integrates via:

### API Layer (`src/lib/api/`)
```typescript
export async function fetchUsers(): Promise<User[]> {
  const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/users`)
  if (!res.ok) throw new Error('Failed to fetch users')
  return res.json()
}
```

### React Query Integration
```tsx
import { useQuery } from '@tanstack/react-query'
import { fetchUsers } from '@/lib/api/users'

function UserList() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['users'],
    queryFn: fetchUsers,
  })

  if (isLoading) return <Skeleton className="h-20 w-full" />
  if (error) return <Alert variant="destructive">{error.message}</Alert>

  return (
    <Table>
      <TableHeader><TableRow>
        <TableHead>Name</TableHead><TableHead>Email</TableHead>
      </TableRow></TableHeader>
      <TableBody>
        {data?.map(user => (
          <TableRow key={user.id}>
            <TableCell>{user.name}</TableCell>
            <TableCell>{user.email}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

### Environment Variables
```bash
# .env.example — never commit actual values
VITE_API_BASE_URL=http://localhost:3001
VITE_AUTH_PROVIDER_URL=https://auth.example.com
```

---

## VI. Troubleshooting Guide

### 6.1 Components not themed / raw shadcn appearance

**Cause**: `@forge/ui-tokens` not imported in `globals.css`, or `@theme inline` block is missing.
**Fix**: Verify `globals.css` follows the Section 2.2 structure. Ensure `@import "@forge/ui-tokens"` appears before the `@theme inline` color mapping block.

### 6.2 `bg-background` or `text-primary` not applying styles

**Cause**: Missing `@theme inline` block that maps CSS variables to Tailwind utilities.
**Fix**: Add the color mapping `@theme inline` block from Section 2.2 step 7. Restart the Vite dev server.

### 6.3 "Module not found: @flywheel/react-icons"

**Cause**: Package not installed or JFrog registry not configured.
**Fix**: Run `npx @forge/dx init` to verify environment, then `pnpm add @flywheel/react-icons`.

### 6.4 Wrong theme or brand applied

**Cause**: Theme class not set on `<html>` element.
**Fix**: Set `document.documentElement.className = 'theme-business'` (or desired theme class).

### 6.5 Components installed but missing Flywheel customizations

**Cause**: Installed from default shadcn registry instead of Forge registry.
**Fix**: Remove the component, verify `components.json` has the `@forge` registry, reinstall with `npx shadcn add @forge/<name>`.

### 6.6 Icon not found in @flywheel/react-icons

**Fix**: Use MCP to search: `forge_get_icon("description of what you need")`. Icons follow the `{Name}Icon{Size?}` pattern.

---

## VII. Refusal Template

If a user requests an artifact that violates a hard-stop rule, respond with:

```text
⛔ This request conflicts with the Flywheel Frontend Architect constitution:

**Rule {N}: {Rule Title}**

{Explain the specific violation}

**Compliant alternative**:
{Provide the correct Flywheel-compliant approach}
```

**Example**:
```text
⛔ This request conflicts with the Flywheel Frontend Architect constitution:

**Rule 1.1: Icons — @flywheel/react-icons Only**

Importing from `lucide-react` is legally prohibited by AT&T. The requested
`import { Bell } from "lucide-react"` cannot be generated.

**Compliant alternative**:
import { BellIcon } from "@flywheel/react-icons"
```

---

**Version**: 1.0.0
**Last Updated**: 2026-03-17
**Source**: Generated from flywheel-demo reference implementation and Forge documentation
