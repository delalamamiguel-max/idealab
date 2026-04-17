---
description: Validate Flywheel compliance by scanning for prohibited imports, hardcoded colors, missing registry prefixes, accessibility issues, and configuration errors
---

User input: $ARGUMENTS

## Execution Steps

### 0. Set ARCHETYPES_BASEDIR

// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Load Constitution

Read validation requirements from:
`${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/flywheel-frontend-architect-constitution.md`

Focus on Section I (Hard-Stop Rules) and Section II (Mandatory Patterns).

### 2. Identify Test Scope

Determine what to test based on $ARGUMENTS:

| Scope | Tests |
|-------|-------|
| **Icons** | No lucide-react or other prohibited icon library imports |
| **Registry** | All components installed from @forge registry |
| **Tokens** | @forge/ui-tokens imported and configured correctly |
| **Colors** | Zero hardcoded palette classes or color literals in components |
| **Accessibility** | ARIA attributes, keyboard nav, heading hierarchy, focus management |
| **TypeScript** | strict mode enabled, no explicit `any` types |
| **MCP** | @forge/mcp configured in editor MCP configs |
| **Architecture** | Correct directory structure (ui/, blocks/, features/) |

Default: Run all scopes if $ARGUMENTS does not specify a subset.

### 3. Automated Compliance Scan (Optional)

If a quick automated pass is desired, run the cross-platform validation script:

```bash
python "${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/scripts/validate-compliance.py" .
```

This covers Rules 1.1–1.4, 1.6 and architecture checks. Continue with the manual steps below for full coverage (accessibility, MCP, deeper analysis).

### 4. Icon Compliance Scan (Rule 1.1)

Scan for prohibited icon library imports:

```bash
# Check for lucide-react (legally prohibited)
echo "=== Icon Compliance ==="
grep -rn "lucide-react" src/ package.json 2>/dev/null
grep -rn "from ['\"]react-icons" src/ 2>/dev/null
grep -rn "from ['\"]@heroicons" src/ 2>/dev/null
grep -rn "from ['\"]phosphor-react" src/ 2>/dev/null
grep -rn "from ['\"]@radix-ui/react-icons" src/ 2>/dev/null
```

| Test | Pass Criteria |
|------|--------------|
| lucide-react imports | Zero matches in src/ and package.json |
| react-icons imports | Zero matches |
| heroicons imports | Zero matches |
| phosphor-react imports | Zero matches |
| @radix-ui/react-icons imports | Zero matches |
| @flywheel/react-icons in package.json | Present in dependencies |

**Also verify icon accessibility**:
```bash
# Icon-only buttons without aria-label
grep -rn 'size="icon"' src/ | grep -v "aria-label" 2>/dev/null
```

### 5. Registry Compliance Scan (Rule 1.2)

Verify Forge registry configuration:

```bash
echo "=== Registry Compliance ==="

# Check components.json exists and has @forge registry
cat components.json 2>/dev/null | grep -q "forge.dev.att.com" && echo "PASS: Forge registry configured" || echo "FAIL: Forge registry missing from components.json"

# Check for flywheel style
cat components.json 2>/dev/null | grep -q '"flywheel"' && echo "PASS: Flywheel style set" || echo "FAIL: Flywheel style not set"

# Check iconLibrary is not lucide
cat components.json 2>/dev/null | grep -q '"lucide"' && echo "FAIL: iconLibrary set to lucide" || echo "PASS: iconLibrary not lucide"
```

### 6. Token Compliance Scan (Rule 1.3)

Verify @forge/ui-tokens setup:

```bash
echo "=== Token Compliance ==="

# Check package.json for @forge/ui-tokens
grep -q "@forge/ui-tokens" package.json && echo "PASS: ui-tokens in dependencies" || echo "FAIL: ui-tokens missing from package.json"

# Check globals.css imports ui-tokens
grep -q "@forge/ui-tokens" src/styles/globals.css 2>/dev/null && echo "PASS: globals.css imports ui-tokens" || echo "FAIL: globals.css missing ui-tokens import"

# Check @theme inline block exists with color mappings
grep -q "color-background" src/styles/globals.css 2>/dev/null && echo "PASS: @theme inline color mappings present" || echo "FAIL: @theme inline color mappings missing"

# Check dark mode variant
grep -q "dark" src/styles/globals.css 2>/dev/null && echo "PASS: Dark mode variant present" || echo "FAIL: Dark mode variant missing"

# Check base layer
grep -q "bg-background" src/styles/globals.css 2>/dev/null && echo "PASS: Base layer sets bg-background" || echo "FAIL: Base layer missing"
```

### 7. Hardcoded Color Scan (Rule 1.4)

Scan all component files for literal color references:

```bash
echo "=== Hardcoded Color Scan ==="

# Tailwind palette class violations
echo "--- Tailwind palette classes ---"
grep -rn "text-\(blue\|red\|green\|yellow\|purple\|pink\|orange\|slate\|gray\|zinc\|neutral\|stone\)-[0-9]" src/components/ src/features/ 2>/dev/null

# Background palette classes
grep -rn "bg-\(blue\|red\|green\|yellow\|purple\|pink\|orange\|slate\|gray\|zinc\|neutral\|stone\)-[0-9]" src/components/ src/features/ 2>/dev/null

# Border palette classes
grep -rn "border-\(blue\|red\|green\|yellow\|purple\|pink\|orange\|slate\|gray\|zinc\|neutral\|stone\)-[0-9]" src/components/ src/features/ 2>/dev/null

# Literal hex values in TSX/TS files
echo "--- Literal hex colors ---"
grep -rn "#[0-9a-fA-F]\{3,8\}" src/components/ src/features/ 2>/dev/null

# Inline style color literals
echo "--- Inline style colors ---"
grep -rn "color:\s*['\"]#\|backgroundColor:\s*['\"]#" src/components/ src/features/ 2>/dev/null
```

| Test | Pass Criteria |
|------|--------------|
| Palette class scan | Zero matches in component/feature directories |
| Hex literal scan | Zero matches in component/feature directories |
| Inline style scan | Zero matches in component/feature directories |

**Exception**: Files listed in `THEME_EXCEPTIONS.md` are excluded from failure counts.

### 8. Accessibility Scan (Rule 1.5)

```bash
echo "=== Accessibility Scan ==="

# Icon buttons without aria-label
echo "--- Icon buttons without aria-label ---"
grep -rn 'size="icon"' src/ | grep -v "aria-label" 2>/dev/null

# Images without alt text
echo "--- Images without alt ---"
grep -rn "<img" src/ | grep -v "alt=" 2>/dev/null

# Interactive divs/spans (should be button/a/input)
echo "--- Interactive divs ---"
grep -rn 'onClick=' src/components/ | grep -E "<(div|span)" 2>/dev/null

# Check heading hierarchy in feature components
echo "--- Heading usage ---"
grep -rn "<h[1-6]\|<Heading" src/components/features/ src/pages/ 2>/dev/null
```

| Test | Pass Criteria |
|------|--------------|
| Icon buttons | All icon-sized buttons have aria-label |
| Image alt text | All img elements have alt attribute |
| Interactive elements | No onClick on div/span (use button/a) |
| Heading hierarchy | No skipped heading levels |

### 9. TypeScript Compliance Scan (Rule 1.6)

```bash
echo "=== TypeScript Compliance ==="

# Check for explicit 'any' types
grep -rn ": any\b\|as any\b" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | grep -v "node_modules" | grep -v ".d.ts"

# Check tsconfig strict mode
grep -q '"strict": true' tsconfig.json 2>/dev/null && echo "PASS: strict mode enabled" || echo "FAIL: strict mode not enabled"

# Check for @ts-ignore without comments
grep -rn "@ts-ignore" src/ --include="*.ts" --include="*.tsx" 2>/dev/null
```

### 10. MCP Configuration Scan

```bash
echo "=== MCP Configuration ==="

# Check for VS Code MCP config
test -f .vscode/mcp.json && echo "PASS: .vscode/mcp.json exists" || echo "WARN: .vscode/mcp.json missing"

# Check for Cursor MCP config
test -f .cursor/mcp.json && echo "PASS: .cursor/mcp.json exists" || echo "WARN: .cursor/mcp.json missing"

# Check for @forge/mcp reference
grep -rq "@forge/mcp" .vscode/ .cursor/ 2>/dev/null && echo "PASS: @forge/mcp configured" || echo "WARN: @forge/mcp not configured"
```

### 11. Architecture Scan

```bash
echo "=== Architecture Scan ==="

# Check directory structure
test -d src/components/ui && echo "PASS: src/components/ui/ exists" || echo "FAIL: src/components/ui/ missing"
test -f src/lib/utils.ts && echo "PASS: src/lib/utils.ts exists" || echo "FAIL: src/lib/utils.ts missing"
test -f src/styles/globals.css && echo "PASS: src/styles/globals.css exists" || echo "FAIL: src/styles/globals.css missing"
test -f src/main.tsx && echo "PASS: src/main.tsx exists" || echo "FAIL: src/main.tsx missing"

# Check cn() utility
grep -q "twMerge" src/lib/utils.ts 2>/dev/null && echo "PASS: cn() uses tailwind-merge" || echo "FAIL: cn() missing or incorrect"

# Check vite.config has @ alias
grep -q "@" vite.config.ts 2>/dev/null && echo "PASS: @ alias configured" || echo "FAIL: @ alias missing"
```

### 12. Generate Compliance Report

Compile all results into a structured report:

```text
## Flywheel Compliance Report

**Project**: {name}
**Date**: {date}
**Constitution Version**: 1.0.0

### Summary

| Category | Status | Issues |
|----------|--------|--------|
| Icons (Rule 1.1) | PASS/FAIL | {count} |
| Registry (Rule 1.2) | PASS/FAIL | {count} |
| Tokens (Rule 1.3) | PASS/FAIL | {count} |
| Colors (Rule 1.4) | PASS/FAIL | {count} |
| Accessibility (Rule 1.5) | PASS/FAIL | {count} |
| TypeScript (Rule 1.6) | PASS/FAIL | {count} |
| MCP Config | PASS/WARN | {count} |
| Architecture | PASS/FAIL | {count} |

### Overall: {PASS/FAIL}

### Issues Found
{detailed list of each issue with file:line and recommended fix}

### Recommendations
{prioritized list of fixes}
```

---

## Error Handling

- **Source directory not found**: Check project root — look for `src/`, `app/`, or user-specified source directory
- **No components installed yet**: Report architecture as WARN (not FAIL) — components may be added later
- **THEME_EXCEPTIONS.md exists**: Read it and exclude listed files/patterns from hardcoded color failures
- **Monorepo structure**: Ask user which package to scan if multiple `src/` directories exist

## Examples

### Example 1: Full Compliance Check
```
/test-flywheel-frontend-architect Run a full compliance check on my project
```

### Example 2: Icon-Only Scan
```
/test-flywheel-frontend-architect Check for any lucide-react imports or icon issues
```

### Example 3: Pre-Deploy Validation
```
/test-flywheel-frontend-architect Run all tests and generate a compliance report for the PR review
```

## References

- Constitution: `${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/flywheel-frontend-architect-constitution.md`
- Validation script: `${ARCHETYPES_BASEDIR}/flywheel-frontend-architect/scripts/validate-compliance.py`
