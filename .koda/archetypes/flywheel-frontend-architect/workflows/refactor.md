---
description: Migrate an existing frontend project to Flywheel compliance by replacing prohibited imports, adopting Forge registry components, and applying AT&T brand tokens
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read refactoring guardrails from:
`${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/flywheel-frontend-architect-constitution.md`

Focus on Section I (Hard-Stop Rules) and Section II (Mandatory Patterns).

### 2. Audit Current Project State

Perform a comprehensive audit of the existing codebase:

#### 2.1 Icon Library Audit

```bash
echo "=== Icon Library Audit ==="

# Find all icon imports
grep -rn "from ['\"]lucide-react" src/ 2>/dev/null
grep -rn "from ['\"]react-icons" src/ 2>/dev/null
grep -rn "from ['\"]@heroicons" src/ 2>/dev/null
grep -rn "from ['\"]@radix-ui/react-icons" src/ 2>/dev/null
grep -rn "from ['\"]@flywheel/react-icons" src/ 2>/dev/null

# Count lucide imports for migration scope
grep -rn "from ['\"]lucide-react" src/ 2>/dev/null | wc -l
```

#### 2.2 Component Registry Audit

```bash
echo "=== Component Registry Audit ==="

# Check if components.json exists
test -f components.json && echo "components.json exists" || echo "components.json MISSING"

# Check registry configuration
cat components.json 2>/dev/null | grep -q "forge.dev.att.com" && echo "Forge registry: configured" || echo "Forge registry: NOT configured"

# List installed UI components
ls src/components/ui/ 2>/dev/null
```

#### 2.3 Token/Color Audit

```bash
echo "=== Token/Color Audit ==="

# Check for @forge/ui-tokens
grep -q "@forge/ui-tokens" package.json 2>/dev/null && echo "ui-tokens: installed" || echo "ui-tokens: NOT installed"

# Count hardcoded Tailwind palette references
echo "Palette class count:"
grep -rn "text-\(blue\|red\|green\|slate\|gray\|zinc\)-[0-9]" src/ 2>/dev/null | wc -l

# Count literal hex values in components
echo "Hex literal count:"
grep -rn "#[0-9a-fA-F]\{3,8\}" src/components/ src/features/ 2>/dev/null | wc -l

# Count inline style colors
echo "Inline style color count:"
grep -rn "color:\s*['\"]#" src/ 2>/dev/null | wc -l
```

#### 2.4 Configuration Audit

```bash
echo "=== Configuration Audit ==="

# Check Tailwind version
grep "tailwindcss" package.json 2>/dev/null

# Check if Tailwind v4 vite plugin is installed
grep "@tailwindcss/vite" package.json 2>/dev/null && echo "TW4 vite plugin: YES" || echo "TW4 vite plugin: NO"

# Check globals.css structure
grep "@forge/ui-tokens" src/styles/globals.css src/index.css 2>/dev/null
grep "@theme inline" src/styles/globals.css src/index.css 2>/dev/null

# Check TypeScript strict mode
grep '"strict"' tsconfig.json 2>/dev/null
```

### 3. Generate Migration Plan

Present a structured migration plan to the user based on the audit:

```text
## Migration Plan

### Phase 1: Infrastructure (do first)
- [ ] Install @forge/ui-tokens
- [ ] Install @flywheel/react-icons
- [ ] Configure components.json with Forge registry
- [ ] Create/update globals.css with Flywheel CSS foundation
- [ ] Add @theme inline color mappings
- [ ] Add @tailwindcss/vite plugin (if upgrading to TW4)

### Phase 2: Icon Migration
- [ ] Replace {n} lucide-react imports with @flywheel/react-icons
- [ ] Update icon naming ({Lucide} → {Name}Icon)
- [ ] Remove lucide-react from package.json
- [ ] Add aria-label to all icon-only buttons

### Phase 3: Component Migration
- [ ] Reinstall {n} components from @forge registry
- [ ] Update component imports if paths changed
- [ ] Verify component behavior after replacement

### Phase 4: Color Migration
- [ ] Replace {n} Tailwind palette references with semantic tokens
- [ ] Replace {n} hex literals with semantic tokens
- [ ] Document exceptions in THEME_EXCEPTIONS.md

### Phase 5: Validation
- [ ] Run test-flywheel-frontend-architect for compliance report
- [ ] Fix any remaining issues
```

**⛔ STOP: Present plan to user for approval before proceeding.**

---

### 4. Phase 1: Infrastructure Setup

#### 4.1 Install Token Package

```bash
pnpm add @forge/ui-tokens @flywheel/react-icons
pnpm add class-variance-authority clsx tailwind-merge tw-animate-css  # if not present
pnpm add @base-ui/react  # if not present
```

#### 4.2 Configure components.json

Create or update `components.json`:
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

#### 4.3 Create/Update globals.css

Create or update `src/styles/globals.css` following constitution Section 2.2:
- Tailwind v4 imports
- Base UI keyframes
- Custom data-attribute variants
- `@import "@forge/ui-tokens"`
- Dark mode variant
- `@theme inline` color mappings
- Base layer (ATTAleckSans font)

#### 4.4 Create cn() Utility (If Missing)

Ensure `src/lib/utils.ts` exists with the `cn()` function per constitution Section 2.4.

### 5. Phase 2: Icon Migration

For each file with prohibited icon imports:

1. **Map icon names**: Lucide icons use `{Name}` format, Flywheel uses `{Name}Icon` format

**Common mappings**:
| Lucide Import | Flywheel Import |
|---------------|-----------------|
| `Bell` | `BellIcon` |
| `Search` | `SearchIcon` |
| `X` | `CloseIcon16` |
| `ChevronDown` | `ChevronDownIcon16` |
| `ChevronRight` | `ChevronRightIcon16` |
| `Check` | `CheckIcon` |
| `Plus` | `PlusIcon` |
| `Minus` | `MinusIcon` |
| `ArrowLeft` | `ArrowLeftIcon` |
| `ArrowRight` | `ArrowRightIcon` |
| `User` | `UserIcon` |
| `Settings` | `SettingsIcon` |
| `Menu` | `MenuIcon` |
| `MoreHorizontal` | `MoreHorizontalIcon` |

2. **Use MCP for unfamiliar icons**: `forge_get_icon("description")` to find the correct Flywheel icon

3. **Update import statements**:
```tsx
// Before
import { Bell, Search, X } from "lucide-react"

// After
import { BellIcon, SearchIcon, CloseIcon16 } from "@flywheel/react-icons"
```

4. **Update JSX usage** — Flywheel icons may have slightly different size props

5. **Remove lucide-react from package.json**:
```bash
pnpm remove lucide-react
```

### 6. Phase 3: Component Migration

For each UI component currently installed from default shadcn:

1. **Back up existing component** (in case of local customizations)
2. **Reinstall from Forge registry**: `npx shadcn add @forge/<name>` (will overwrite)
3. **Restore any custom modifications** on top of the Forge version
4. **Verify component works** with the new Flywheel tokens

**Important**: If components have significant local customizations, compare the Forge version with the local version and merge changes carefully.

### 7. Phase 4: Color Migration

Apply semantic token replacements across all component and feature files:

**Migration rules**:

| Current Usage | Replacement |
|--------------|------------|
| `bg-white`, `bg-slate-50` | `bg-background` |
| `text-black`, `text-slate-900`, `text-gray-900` | `text-foreground` |
| `text-blue-500`, `text-blue-600` | `text-primary` |
| `bg-blue-600`, `bg-blue-700` | `bg-primary` |
| `text-white` (on primary buttons) | `text-primary-foreground` |
| `text-slate-400`, `text-gray-400`, `text-gray-500` | `text-muted-foreground` |
| `bg-slate-100`, `bg-gray-100` | `bg-muted` |
| `bg-slate-800`, `bg-gray-800` | `bg-card` or `bg-secondary` |
| `border-slate-200`, `border-gray-200` | `border-border` |
| `text-red-500`, `text-red-600` | `text-destructive` |
| `bg-red-600` | `bg-destructive` |
| `hover:bg-slate-100`, `hover:bg-gray-100` | `hover:bg-accent` |
| `ring-blue-500` | `ring-ring` |
| `dark:bg-slate-900` → `dark:text-white` | Remove — tokens handle dark mode automatically |

**Important**: Do NOT blindly replace — verify each mapping makes semantic sense for the component's purpose.

### 8. Phase 5: Validation

Run the automated compliance script for a quick check:

```bash
python "${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/scripts/validate-compliance.py" .
```

Then run the full test workflow for comprehensive validation:

```
/test-flywheel-frontend-architect Run full compliance check
```

Fix any remaining issues identified in the compliance report.

### 9. Document Exceptions

Create `THEME_EXCEPTIONS.md` at the project root listing any intentional non-compliant color usage:

```markdown
# Theme Exceptions

Files and patterns excluded from Flywheel color compliance checks.

| File | Color | Justification |
|------|-------|---------------|
| src/components/charts/bar-chart.tsx | Categorical palette | Fixed colors for chart legibility |
| src/components/brand/logo.tsx | #009FDB | AT&T corporate brand logo |
```

---

## Error Handling

- **Component has heavy local customizations**: Compare Forge version with local version, merge manually, present diff to user for approval
- **Icon not found in @flywheel/react-icons**: Use MCP `forge_get_icon()` or fall back to a generic icon with TODO comment
- **Tailwind v3 → v4 upgrade required**: Guide through migration, replace `tailwind.config.js` with `@theme inline` CSS approach
- **Existing CSS-in-JS theme system**: Migrate CSS variables to `@forge/ui-tokens`, remove CSS-in-JS theme dependency

## Examples

### Example 1: Full Migration
```
/refactor-flywheel-frontend-architect Migrate my React app from shadcn defaults + lucide-react to full Flywheel compliance with Business theme
```

### Example 2: Icon-Only Migration
```
/refactor-flywheel-frontend-architect Replace all lucide-react imports with @flywheel/react-icons equivalents
```

### Example 3: Token Adoption
```
/refactor-flywheel-frontend-architect Replace all hardcoded Tailwind palette colors with semantic tokens from @forge/ui-tokens
```

## References

- Constitution: `${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/flywheel-frontend-architect-constitution.md`
- Validation script: `${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/scripts/validate-compliance.py`
