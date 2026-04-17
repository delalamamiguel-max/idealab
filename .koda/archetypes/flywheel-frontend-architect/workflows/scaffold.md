---
description: Scaffold a new Flywheel-compliant web application frontend with Vite, React 19, Tailwind v4, TypeScript, AT&T brand theming, and 60+ Flywheel components
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
`${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/flywheel-frontend-architect-constitution.md`

Verify no hard-stop rule violations exist in the user's requirements.

### 2. Gather Project Requirements

**PROMPT THE USER FOR ALL OF THE FOLLOWING before starting scaffold:**

#### 2.1 Project Context
- **Project Name**: Application or package identifier
- **Project Type**: New greenfield project or adding Flywheel to existing project
- **Description**: Brief description of what the application does

#### 2.2 Brand Theme
- **Primary Theme**: Consumer (default) | Business | FirstNet
- **Dark Mode**: Include dark mode support? (Yes recommended)
- **Theme Switching**: Runtime theme switching UI? (Yes if user-facing)

#### 2.3 Component Selection
Present the available components and ask which are needed for the initial scaffold:

**Layout & Navigation:**
- Top Navigation (app header)
- Sidebar (collapsible navigation)
- Breadcrumb
- Tabs
- Navigation Menu

**Content & Display:**
- Card
- Table (data table)
- Heading (responsive typography)
- Surface (themed container)
- Badge
- Avatar
- Skeleton (loading states)
- Price (monetary display)

**Input & Forms:**
- Button
- Input
- Select
- Autocomplete (search dropdown)
- Checkbox
- Radio Group
- Form (React Hook Form integration)
- Calendar / Date Picker
- Textarea
- Switch / Toggle

**Overlay & Feedback:**
- Dialog
- Sheet (slide-over panel)
- Drawer / Bottom Sheet
- Toast (notifications)
- Alert / Alert Dialog
- Dropdown Menu
- Tooltip
- Command (command palette)

**Special:**
- Swatch (color selection)
- Tree View (hierarchical data)
- Carousel

#### 2.4 Page Layout Pattern
- **Layout Type**: Sidebar + content | Top nav + content | Sidebar + top nav + content | Minimal (no nav)
- **Responsive Strategy**: Mobile-first | Desktop-first

#### 2.5 Data & Integration
- **API Integration**: REST | GraphQL | None (static/mock data for now)
- **State Management**: React Query (recommended) | Zustand | Context only
- **Authentication**: OAuth/OIDC integration needed? (delegate to backend archetype)

#### 2.6 Additional Features
- **MCP Configuration**: Include @forge/mcp setup? (Yes recommended)
- **AGENTS.md**: Generate AI workspace instructions? (Yes recommended)

**⛔ STOP: Do not proceed until all requirements gathered.**

---

### 3. Scaffold Project Structure

#### 3.1 If New Project — Use Forge CLI (Preferred)

```bash
npx @forge/dx init            # verify environment
npx @forge/dx create {name}   # scaffold project
cd {name}
```

If Forge CLI is unavailable, scaffold manually:

```bash
npm create vite@latest {name} -- --template react-ts
cd {name}
pnpm install
```

Then configure manually per Section 3.2.

#### 3.2 Configure Project Files

**Create/update `components.json`** per constitution Section 2.1.

**Create/update `vite.config.ts`** per constitution Section 2.1:
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

**Update `tsconfig.json`** — ensure `strict: true` and path aliases:
```json
{
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  }
}
```

**Create `tsconfig.app.json`** — extends base config with proper module settings.

#### 3.3 Install Core Dependencies

```bash
pnpm add @base-ui/react @flywheel/react-icons @forge/ui-tokens class-variance-authority clsx tailwind-merge tw-animate-css react react-dom
pnpm add -D @tailwindcss/vite @vitejs/plugin-react tailwindcss typescript vite
```

**If forms are needed**:
```bash
pnpm add react-hook-form @hookform/resolvers zod
```

**If data table / carousel / calendar / drawer / command are needed**:
```bash
pnpm add embla-carousel-react    # carousel
pnpm add react-day-picker        # calendar/date-picker
pnpm add vaul                    # drawer/bottom-sheet
pnpm add cmdk                    # command palette
```

**If state management is needed**:
```bash
pnpm add @tanstack/react-query   # server state
pnpm add zustand                 # client state (if requested)
```

### 4. Create CSS Foundation

Create `src/styles/globals.css` following constitution Section 2.2 — the complete layered structure with:
1. Tailwind v4 + animation imports
2. Base UI keyframes + radius scale
3. Custom data-attribute variants
4. Scrollbar utility
5. `@import "@forge/ui-tokens"`
6. Dark mode variant
7. `@theme inline` color mapping
8. Base layer (font, border, body defaults)
9. Root radius token

### 5. Create Utility Files

**Create `src/lib/utils.ts`** per constitution Section 2.4:
```typescript
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### 6. Install Selected Components

Install all components selected in Step 2.3 using the Forge registry:

```bash
# Install each component — example batch
npx shadcn add @forge/button @forge/card @forge/badge
npx shadcn add @forge/dialog @forge/sheet @forge/toast
npx shadcn add @forge/input @forge/form @forge/select
npx shadcn add @forge/sidebar @forge/top-navigation @forge/tabs
```

**Important**: Always use the `@forge/` prefix. Never omit it.

After installation, verify components are in `src/components/ui/`.

### 7. Create Entry Point

**Create `src/main.tsx`** per constitution Section 2.10.

**Create `src/App.tsx`** with:
- Theme switching UI (if requested in Step 2.2)
- Layout shell using selected navigation components
- Sample content demonstrating installed components
- Toast provider (`<Toaster />`) if toast was selected

**Example App.tsx with theme switcher**:
```tsx
import { useState } from 'react'
import { Button } from '@/components/ui/button'

type Theme = 'theme-consumer' | 'theme-business' | 'theme-firstnet'

const themes: { label: string; value: Theme }[] = [
  { label: 'Consumer', value: 'theme-consumer' },
  { label: 'Business', value: 'theme-business' },
  { label: 'FirstNet', value: 'theme-firstnet' },
]

export default function App() {
  const [activeTheme, setActiveTheme] = useState<Theme>('theme-business')

  function switchTheme(theme: Theme) {
    setActiveTheme(theme)
    document.documentElement.className = theme
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Layout and content here */}
    </div>
  )
}
```

### 8. Configure MCP (If Requested)

**Create `.vscode/mcp.json`**:
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

**Create `.cursor/mcp.json`** with matching Cursor format.

### 9. Generate AGENTS.md (If Requested)

Create `AGENTS.md` at the project root with workspace rules:
- Icon rules (@flywheel/react-icons only)
- Theming rules (@forge/ui-tokens, theme classes)
- Tailwind rules (v4, bare utilities)
- Component installation rules (@forge prefix)
- MCP workflow reference
- Available component list
- Theme switching reference

### 10. Create .env.example (If API Integration Requested)

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:3001

# Authentication (if needed)
VITE_AUTH_PROVIDER_URL=https://auth.example.com
VITE_AUTH_CLIENT_ID=your-client-id
```

### 11. Post-Scaffold Validation

// turbo
Run the following validation checks:

```bash
# 1. Verify no lucide-react imports
grep -rn "lucide-react" src/ package.json 2>/dev/null && echo "FAIL: lucide-react found" || echo "PASS: No lucide-react"

# 2. Verify @forge/ui-tokens installed
grep "@forge/ui-tokens" package.json && echo "PASS: ui-tokens present" || echo "FAIL: ui-tokens missing"

# 3. Verify @flywheel/react-icons installed
grep "@flywheel/react-icons" package.json && echo "PASS: react-icons present" || echo "FAIL: react-icons missing"

# 4. Verify components.json has @forge registry
grep "forge.dev.att.com" components.json && echo "PASS: Forge registry configured" || echo "FAIL: Forge registry missing"

# 5. Verify globals.css imports ui-tokens
grep "@forge/ui-tokens" src/styles/globals.css && echo "PASS: globals.css imports tokens" || echo "FAIL: globals.css missing token import"

# 6. Verify no hardcoded Tailwind palette colors in components
grep -rn "text-blue-\|bg-blue-\|text-red-\|bg-red-\|text-slate-\|bg-slate-\|text-gray-\|bg-gray-" src/components/ 2>/dev/null && echo "FAIL: Hardcoded colors found" || echo "PASS: No hardcoded colors"
```

Report results and fix any failures before completing.

---

## Error Handling

- **Forge CLI unavailable**: Fall back to manual Vite + React scaffold, then configure manually
- **JFrog registry inaccessible**: Run `npx @forge/dx init` to configure access, then retry
- **Component installation fails**: Verify `components.json` registry URL, check network/proxy settings
- **@forge/ui-tokens not found**: Ensure JFrog npm registry is configured in `.npmrc`
- **TypeScript errors after scaffold**: Verify `tsconfig.json` path aliases match `vite.config.ts` aliases

## Examples

### Example 1: Dashboard Application
```
/scaffold-flywheel-frontend-architect Create a dashboard app called "network-ops" with Business theme, sidebar layout, data tables, charts, and form inputs. Include MCP and AGENTS.md.
```

### Example 2: Customer Portal
```
/scaffold-flywheel-frontend-architect Create a customer-facing portal called "my-account" with Consumer theme, top nav layout, cards, pricing components, and form validation. Include dark mode toggle.
```

### Example 3: Add Flywheel to Existing Project
```
/scaffold-flywheel-frontend-architect Add Flywheel to my existing React app. I need the token setup, button, dialog, and toast components with FirstNet theming.
```

## References

- Constitution: `${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/flywheel-frontend-architect-constitution.md`
- Forge docs: https://forge.dev.att.com
