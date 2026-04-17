---
description: Diagnose and fix Flywheel-specific issues including missing tokens, broken theme switching, component rendering failures, icon errors, and registry problems
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read troubleshooting guidance from:
`${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/flywheel-frontend-architect-constitution.md`

Focus on Section VI (Troubleshooting Guide).

### 2. Identify Problem Category

Categorize the reported issue based on $ARGUMENTS:

| Category | Symptoms | Common Causes |
|----------|----------|---------------|
| **Theme Not Applied** | Components look unstyled / raw shadcn appearance | Missing `@forge/ui-tokens` import, missing `@theme inline` block |
| **Colors Wrong** | Wrong brand colors, tokens not resolving | Wrong theme class, missing `rgb()` wrapper in `@theme inline`, stale build cache |
| **Icon Error** | Icon not found, wrong icon rendering | Package not installed, wrong import name, lucide-react leaking |
| **Component Missing** | Component file not in `src/components/ui/` | Not installed, installed from wrong registry, `components.json` misconfigured |
| **Dark Mode Broken** | Dark mode not toggling, partial dark mode | Missing dark variant, `.dark` class not applied, tokens missing dark values |
| **Build Failure** | Vite build errors, TypeScript errors | Missing deps, wrong `@` alias config, TW4 plugin not configured |
| **Tailwind Utilities** | `bg-background` or `text-primary` not working | Missing `@theme inline`, stale Tailwind cache, wrong CSS import order |
| **Registry Access** | `npx shadcn add @forge/*` fails | JFrog not configured, proxy issues, wrong registry URL |

### 3. Collect Diagnostic Information

**For Theme/Token Issues:**

```bash
echo "=== Theme Diagnostics ==="

# Check @forge/ui-tokens is installed
grep "@forge/ui-tokens" package.json 2>/dev/null

# Check globals.css imports
head -20 src/styles/globals.css 2>/dev/null

# Check @theme inline block
grep -A3 "@theme inline" src/styles/globals.css 2>/dev/null

# Check for --color-background mapping
grep "color-background" src/styles/globals.css 2>/dev/null

# Check theme class on html
grep "theme-\|classList\|className" src/App.tsx src/main.tsx 2>/dev/null
```

**For Icon Issues:**

```bash
echo "=== Icon Diagnostics ==="

# Check @flywheel/react-icons is installed
grep "@flywheel/react-icons" package.json 2>/dev/null

# Check for any lucide-react references
grep -rn "lucide-react" src/ package.json 2>/dev/null

# List all icon imports
grep -rn "from ['\"]@flywheel/react-icons" src/ 2>/dev/null
```

**For Component Issues:**

```bash
echo "=== Component Diagnostics ==="

# List installed components
ls src/components/ui/ 2>/dev/null

# Check components.json registry
cat components.json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('registries',{}), indent=2))" 2>/dev/null || cat components.json 2>/dev/null | grep -A3 "registries"

# Check for @base-ui/react (required by Flywheel components)
grep "@base-ui/react" package.json 2>/dev/null
```

**For Build Issues:**

```bash
echo "=== Build Diagnostics ==="

# Check vite config
cat vite.config.ts 2>/dev/null

# Check for @tailwindcss/vite plugin
grep "@tailwindcss/vite" package.json 2>/dev/null

# Check TypeScript config
cat tsconfig.json 2>/dev/null | grep -A5 "compilerOptions"

# Check path alias
grep -A2 "alias" vite.config.ts 2>/dev/null
grep -A3 "paths" tsconfig.json 2>/dev/null

# Try to build and capture errors
pnpm build 2>&1 | tail -30
```

**For Registry Issues:**

```bash
echo "=== Registry Diagnostics ==="

# Check npm/pnpm registry config
cat .npmrc 2>/dev/null
npm config get registry 2>/dev/null

# Check if JFrog is configured
npm config get @flywheel:registry 2>/dev/null
npm config get @forge:registry 2>/dev/null

# Try to resolve a known package
npm view @forge/ui-tokens version 2>&1 | head -5
```

### 4. Common Issues and Solutions

#### 4.1 Components Look Unstyled (Raw shadcn Appearance)

**Symptom**: Components render with default browser styling or generic shadcn look, not AT&T branded.

**Diagnosis**: `@forge/ui-tokens` is either not installed or not imported in `globals.css`.

**Solution**:
1. Install: `pnpm add @forge/ui-tokens`
2. Verify `globals.css` has `@import "@forge/ui-tokens"` (Section 5 in the layered structure)
3. Verify the `@theme inline` color mapping block exists (Section 7)
4. Verify `globals.css` is imported in `src/main.tsx`: `import './styles/globals.css'`
5. Restart the Vite dev server: `pnpm dev`

#### 4.2 bg-background / text-primary Not Applying

**Symptom**: Tailwind utility classes like `bg-background` or `text-primary` don't produce any CSS.

**Diagnosis**: Missing `@theme inline` block that maps CSS variables to Tailwind color utilities.

**Solution**:
1. Check `globals.css` has the `@theme inline` block with `--color-background: rgb(var(--background));` entries
2. Ensure `@tailwindcss/vite` is in `vite.config.ts` plugins
3. Clear Vite cache: `rm -rf node_modules/.vite && pnpm dev`

#### 4.3 "Module not found: @flywheel/react-icons"

**Symptom**: Import fails at build time or in the IDE.

**Diagnosis**: Package not installed or JFrog npm registry not configured.

**Solution**:
1. Run `npx @forge/dx init` to verify environment setup
2. Install: `pnpm add @flywheel/react-icons`
3. If registry error: check `.npmrc` for JFrog configuration

#### 4.4 Wrong Theme / Brand Colors

**Symptom**: Application shows wrong brand colors (e.g., Consumer instead of Business).

**Diagnosis**: Wrong theme class on `<html>`, or theme class not being applied.

**Solution**:
1. Verify theme class is set: `document.documentElement.className` should be `theme-business`, `theme-firstnet`, or `theme-consumer`
2. Check `App.tsx` for theme initialization code
3. If using state management: verify theme state is being read and applied on mount

#### 4.5 Dark Mode Not Working

**Symptom**: Adding `.dark` class doesn't switch to dark mode, or dark mode is partial.

**Diagnosis**: Missing dark variant in `globals.css` or `@forge/ui-tokens` not providing dark values.

**Solution**:
1. Verify `globals.css` has: `@custom-variant dark (&:is(.dark *));`
2. Verify this line appears AFTER `@import "@forge/ui-tokens"` (order matters)
3. Verify `.dark` class is being toggled on `<html>`: `document.documentElement.classList.toggle('dark')`

#### 4.6 Component Installation Fails

**Symptom**: `npx shadcn add @forge/<name>` returns an error.

**Diagnosis**: `components.json` is misconfigured, or registry is unreachable.

**Solution**:
1. Verify `components.json` has the `@forge` registry with URL `https://forge.dev.att.com/r/{name}.json`
2. Check network/proxy: `curl -I https://forge.dev.att.com/r/button.json`
3. Ensure `style` is set to `"flywheel"` in `components.json`
4. Try direct install: `npx shadcn@latest add @forge/<name>`

#### 4.7 Base UI Component Errors

**Symptom**: Accordion, collapsible, or other interactive components throw runtime errors.

**Diagnosis**: Missing `@base-ui/react` dependency or data-attribute variants.

**Solution**:
1. Install: `pnpm add @base-ui/react`
2. Verify `globals.css` has the `@custom-variant data-open`, `data-closed`, etc. blocks
3. Verify keyframes for `accordion-down`/`accordion-up` in `@theme inline`

#### 4.8 Path Alias Not Resolving

**Symptom**: `@/components/ui/button` import fails with "module not found".

**Diagnosis**: Path alias mismatch between `vite.config.ts` and `tsconfig.json`.

**Solution**:
1. `vite.config.ts` must have: `resolve: { alias: { '@': path.resolve(__dirname, './src') } }`
2. `tsconfig.json` must have: `"paths": { "@/*": ["./src/*"] }` and `"baseUrl": "."`
3. Restart the IDE TypeScript server

### 5. Generate Debug Report

After diagnosis, provide:

```text
## Flywheel Debug Report

**Issue**: {description}
**Category**: {from Step 2 table}
**Root Cause**: {identified cause}

### Diagnostic Results
{output from Step 3 commands}

### Fix Applied
{exact changes made}

### Verification
{commands to verify the fix}

### Prevention
{how to avoid this issue in the future}
```

---

## Error Handling

- **Multiple issues**: Diagnose and fix in dependency order (infrastructure → tokens → components → icons → layout)
- **Environment not set up**: Direct user to `npx @forge/dx init` before debugging
- **Package version conflict**: Check for pnpm peer dependency issues, suggest `pnpm install --no-strict-peer-dependencies`
- **Custom component conflict**: Check if a local component is shadowing a Flywheel component

## Examples

### Example 1: Theme Not Working
```
/debug-flywheel-frontend-architect My components don't look themed — they have generic shadcn styling instead of AT&T branding
```

### Example 2: Icon Import Failure
```
/debug-flywheel-frontend-architect Getting "Module not found" when importing from @flywheel/react-icons
```

### Example 3: Dark Mode Broken
```
/debug-flywheel-frontend-architect Dark mode toggle doesn't do anything — the UI stays in light mode
```

## References

- Constitution: `${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/flywheel-frontend-architect-constitution.md`
