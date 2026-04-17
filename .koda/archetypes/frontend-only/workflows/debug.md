---
description: Debug frontend-only issues such as React runtime errors, build failures, styling issues, and hydration problems (Frontend Only)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype frontend_only` and parse for debugging tools availability.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Collect Symptoms
From $ARGUMENTS, extract:
- error message / stack trace
- reproduction steps
- framework (Vite/Next.js/etc)
- browser + version
- whether it happens in dev/prod

If missing, ask for logs and a minimal repro.

### 4. Categorize Error Type

Analyze error to determine category:

**Build Errors**:
- TypeScript compile errors
- Module resolution failures
- Circular dependency issues
- Bundler config (Vite/Next) issues
- Dependency mismatch / lockfile drift

**Styling Errors**:
- Tailwind classes not applying
- PostCSS configuration issues
- CSS module import failures
- AT&T color variables not recognized

**Runtime Errors**:
- React rendering crashes
- Null/undefined property access
- State management bugs
- Event handler failures

**Hydration Errors** (Next.js):
- Server/client mismatch
- useEffect timing issues
- Dynamic content inconsistencies

**API/Network Errors**:
- CORS issues (handle via proxy config)
- Fetch timeout errors
- Response parsing failures

**Accessibility Errors**:
- Missing ARIA labels
- Keyboard navigation broken
- Focus management issues

### 5. Debug Build Errors

**A. TypeScript Compile Errors**:
```typescript
// Common issue: Missing null checks
// BEFORE (error: Object is possibly 'undefined')
const name = user.profile.name;

// AFTER: Optional chaining
const name = user?.profile?.name ?? 'Unknown';
```

**B. Module Resolution Failures**:
```bash
# Check tsconfig.json paths
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}

# Verify vite.config.ts alias matches
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
}
```

**C. Dependency Mismatch**:
```bash
# Clear and reinstall
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### 6. Debug Styling Errors

**A. Tailwind Classes Not Applying**:
```javascript
// Check tailwind.config.ts content paths
content: [
  './src/**/*.{js,ts,jsx,tsx}',
  './index.html',
],

// Verify globals.css imports
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**B. AT&T Colors Not Working**:
```typescript
// Verify colors are defined in tailwind.config.ts
theme: {
  extend: {
    colors: {
      'att-blue': '#009FDB',
      'att-cobalt': '#00388F',
    },
  },
}

// Usage: className="bg-att-blue text-white"
```

**C. PostCSS Configuration Missing**:
```javascript
// postcss.config.js must exist
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

### 7. Debug Runtime Errors

**A. Component Crash (null/undefined)**:
```typescript
// BEFORE: Crashes if data is undefined
function UserCard({ user }) {
  return <div>{user.name}</div>;
}

// AFTER: Defensive rendering
function UserCard({ user }: { user?: User }) {
  if (!user) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

**B. State Management Issues**:
```typescript
// Common issue: Stale closure in useEffect
// BEFORE
useEffect(() => {
  const interval = setInterval(() => {
    setCount(count + 1); // Stale count!
  }, 1000);
  return () => clearInterval(interval);
}, []); // Missing dependency

// AFTER: Use functional update
useEffect(() => {
  const interval = setInterval(() => {
    setCount(prev => prev + 1);
  }, 1000);
  return () => clearInterval(interval);
}, []);
```

**C. Event Handler Errors**:
```typescript
// BEFORE: Missing event type
const handleClick = (e) => { ... }

// AFTER: Proper typing
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => { ... }
```

### 8. Debug Hydration Errors (Next.js)

**A. Server/Client Mismatch**:
```typescript
// BEFORE: Different content on server vs client
function Component() {
  return <div>{new Date().toLocaleString()}</div>;
}

// AFTER: Use useEffect for client-only content
function Component() {
  const [time, setTime] = useState<string>();
  
  useEffect(() => {
    setTime(new Date().toLocaleString());
  }, []);
  
  return <div>{time ?? 'Loading...'}</div>;
}
```

**B. Dynamic Imports for Client-Only**:
```typescript
import dynamic from 'next/dynamic';

const ClientOnlyComponent = dynamic(
  () => import('@/components/ClientOnly'),
  { ssr: false }
);
```

### 9. Debug API/Network Errors

**A. CORS Issues (Frontend-Only Fix)**:
```typescript
// Use Vite proxy for development
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'https://api.example.com',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, ''),
    },
  },
}
```

**B. Fetch Timeout Handling**:
```typescript
// Add timeout to fetch requests
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 10000);

try {
  const response = await fetch(url, { signal: controller.signal });
} catch (error) {
  if (error.name === 'AbortError') {
    console.error('Request timed out');
  }
} finally {
  clearTimeout(timeoutId);
}
```

### 10. Apply Fixes
- Make the smallest safe change.
- Add regression tests when feasible.
- If the issue is backend-dependent, implement defensive UI handling and document backend requirement separately.

### 11. Generate Debug Report

```
🐛 Frontend Debug Report

📍 Error Type: <category>
📍 Severity: <critical/high/medium/low>
📍 Framework: <Vite/Next.js/etc>
📍 Browser: <browser + version>

🔍 Root Cause Analysis:
<Detailed explanation of why error occurred>

🛠️ Fixes Applied:
1. <Fix description> - <file>:<line>
2. <Configuration change> - <config file>

✅ Verification Steps:
1. Run dev server: pnpm dev
2. Test in browser: <specific action>
3. Run tests: pnpm test

🚫 Prevention Measures:
- Add lint rule: <rule>
- Add test: <test description>
- Update documentation: <location>

💡 Useful Debug Commands:
- Check TypeScript: pnpm tsc --noEmit
- Check lint: pnpm lint
- Check build: pnpm build
- React DevTools: Install browser extension
```

## Error Handling

**Cannot Reproduce**: Request browser console logs, network tab screenshot, exact reproduction steps.

**Multiple Root Causes**: Prioritize by severity and impact, address systematically.

**Backend-Dependent Issue**: Document backend requirement and implement defensive UI handling.

## Common Debug Patterns

**Pattern 1: Tailwind Not Working**
- Symptom: Classes have no effect
- Root Cause: Missing PostCSS config or content paths
- Fix: Verify tailwind.config.ts and postcss.config.js

**Pattern 2: Component Crash on Load**
- Symptom: White screen, console error
- Root Cause: Accessing undefined property
- Fix: Add null checks, optional chaining, loading states

**Pattern 3: Hydration Mismatch**
- Symptom: Next.js warning about server/client mismatch
- Root Cause: Dynamic content rendered differently
- Fix: Use useEffect for client-only content

**Pattern 4: State Not Updating**
- Symptom: UI doesn't reflect state changes
- Root Cause: Stale closure or missing dependency
- Fix: Use functional updates, add dependencies

## Examples

**Example 1**: `/debug-frontend Tailwind classes not applying after adding AT&T colors`

**Example 2**: `/debug-frontend Component crashes when user data is undefined`

**Example 3**: `/debug-frontend Next.js hydration error on date display`

**Example 4**: `/debug-frontend CORS error when fetching from external API`

## References

Constitution: (pre-loaded above)
Environment Config: `${ARCHETYPES_BASEDIR}/frontend-only/templates/env-config.yaml`
