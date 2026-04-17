---
description: Refactor a frontend-only codebase for maintainability, accessibility, and performance (Frontend Only)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype frontend_only` and parse for ENV_VALID.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Read `${ARCHETYPES_BASEDIR}/frontend-only/templates/env-config.yaml` for project structure and brand guidelines.

### 3. Parse Input
Extract from $ARGUMENTS: target files/modules, refactoring goals (performance, accessibility, type safety, code quality, brand compliance), specific issues to address. Request clarification if incomplete.

### 4. Confirm Frontend-only Scope
- ✘ Do not change backend code, infra, or database.
- If backend changes are needed to complete request, explain and propose a frontend-only alternative.

### 5. Analyze Existing Code

Scan target frontend code for issues:

**Brand Compliance**:
- Non-AT&T colors used (should use `att-blue`, `att-cobalt`, etc.)
- Missing or incorrect color palette
- Inconsistent styling patterns

**Accessibility Issues**:
- Missing ARIA labels
- Poor keyboard navigation
- Insufficient color contrast
- Missing focus indicators
- Touch targets < 44x44px

**Type Safety Issues**:
- `any` types used
- Missing type definitions
- Untyped event handlers
- Missing null checks

**Code Quality Issues**:
- Large components (>200 lines)
- Duplicate code
- Inconsistent naming
- Missing error boundaries
- Poor folder structure

**Performance Issues**:
- Missing memoization
- Large bundle imports
- No code splitting
- Unnecessary re-renders

Report findings with severity (critical/high/medium/low) and file locations.

### 6. Generate Refactoring Plan

Create prioritized plan:

**Phase 1: Critical Accessibility & Type Safety**:
1. Add missing ARIA labels
2. Fix keyboard navigation
3. Replace `any` with proper types
4. Add null checks and type guards

**Phase 2: Brand Compliance**:
1. Replace hardcoded colors with AT&T palette
2. Update TailwindCSS config
3. Standardize button and link styles

**Phase 3: Code Quality**:
1. Split large components
2. Extract reusable UI primitives
3. Normalize folder structure
4. Add error boundaries

**Phase 4: Performance**:
1. Add memoization
2. Implement code splitting
3. Optimize imports

### 7. Apply Refactorings

**A. Brand Compliance Refactorings**:
```typescript
// BEFORE: Hardcoded colors
<button className="bg-blue-500 hover:bg-blue-700">

// AFTER: AT&T brand colors
<button className="bg-att-blue hover:bg-att-cobalt">
```

```typescript
// BEFORE: Inline color values
<div style={{ backgroundColor: '#0066cc' }}>

// AFTER: Tailwind AT&T colors
<div className="bg-att-blue">
```

**B. Accessibility Refactorings**:
```typescript
// BEFORE: Missing ARIA label
<button onClick={handleOpen}>
  <IconMenu />
</button>

// AFTER: Accessible button
<button onClick={handleOpen} aria-label="Open menu">
  <IconMenu aria-hidden="true" />
</button>
```

```typescript
// BEFORE: Non-interactive element with click
<div onClick={handleClick}>Click me</div>

// AFTER: Proper button element
<button onClick={handleClick} type="button">Click me</button>
```

```typescript
// BEFORE: Small touch target
<button className="p-1">X</button>

// AFTER: Minimum 44x44px touch target
<button className="min-w-[44px] min-h-[44px] p-2">X</button>
```

**C. Type Safety Refactorings**:
```typescript
// BEFORE: any type
const handleChange = (e: any) => {
  setValue(e.target.value);
};

// AFTER: Proper typing
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};
```

```typescript
// BEFORE: Missing null check
function UserProfile({ user }) {
  return <div>{user.name}</div>;
}

// AFTER: Type guard and null check
interface User {
  name: string;
  email: string;
}

function UserProfile({ user }: { user: User | null }) {
  if (!user) return <div>Loading...</div>;
  return <div>{user.name}</div>;
}
```

**D. Code Quality Refactorings**:
```typescript
// BEFORE: Large component with mixed concerns
function Dashboard() {
  // 300+ lines of mixed logic, UI, and data fetching
}

// AFTER: Split into focused components
function Dashboard() {
  return (
    <DashboardLayout>
      <DashboardHeader />
      <DashboardStats />
      <DashboardCharts />
    </DashboardLayout>
  );
}
```

```typescript
// BEFORE: Duplicate button styles
<button className="px-4 py-2 bg-att-cobalt text-white rounded-lg">Save</button>
<button className="px-4 py-2 bg-att-cobalt text-white rounded-lg">Submit</button>

// AFTER: Reusable UI primitive
// src/components/ui/Button.tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
}

export function Button({ variant = 'primary', children, ...props }: ButtonProps) {
  const baseClasses = 'px-4 py-2 rounded-lg font-medium transition-colors';
  const variantClasses = {
    primary: 'bg-att-cobalt text-white hover:bg-att-blue',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
  };
  
  return (
    <button className={`${baseClasses} ${variantClasses[variant]}`} {...props}>
      {children}
    </button>
  );
}
```

**E. Performance Refactorings**:
```typescript
// BEFORE: No memoization
function ExpensiveList({ items, filter }) {
  const filtered = items.filter(item => item.name.includes(filter));
  return <ul>{filtered.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}

// AFTER: Memoized computation
function ExpensiveList({ items, filter }) {
  const filtered = useMemo(
    () => items.filter(item => item.name.includes(filter)),
    [items, filter]
  );
  return <ul>{filtered.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}
```

```typescript
// BEFORE: No code splitting
import HeavyChart from './HeavyChart';

// AFTER: Lazy loading
const HeavyChart = lazy(() => import('./HeavyChart'));

function Dashboard() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyChart />
    </Suspense>
  );
}
```

### 8. Update Tests
- Update tests to match refactored code.
- Add tests for new UI primitives.
- Verify accessibility tests pass.

### 9. Validate Refactorings

Run validation checks:
- `pnpm tsc --noEmit` - Type checking
- `pnpm lint` - Lint code
- `pnpm test` - Run tests
- `pnpm build` - Verify build

### 10. Generate Refactoring Report

```
🔧 Frontend Refactoring Report

📊 Issues Identified: <count>
   Critical: <count>
   High: <count>
   Medium: <count>
   Low: <count>

✅ Refactorings Applied:
   Accessibility: <count> fixes
   Brand Compliance: <count> fixes
   Type Safety: <count> fixes
   Code Quality: <count> improvements
   Performance: <count> optimizations

♿ Accessibility Improvements:
   ✓ Added ARIA labels
   ✓ Fixed keyboard navigation
   ✓ Improved focus indicators
   ✓ Increased touch targets

🎨 Brand Compliance:
   ✓ Updated to AT&T color palette
   ✓ Standardized button styles
   ✓ Consistent hover states

📦 Code Quality:
   ✓ Split large components
   ✓ Created reusable UI primitives
   ✓ Normalized folder structure
   ✓ Added error boundaries

⚡ Performance Gains:
   ✓ Added memoization
   ✓ Implemented code splitting
   ✓ Optimized imports

📁 Files Changed:
   - <file list>

⚠️ Breaking Changes:
   - <list if any>

✅ Next Steps:
   1. Review refactored code
   2. Run full test suite
   3. Test in browser
   4. Update documentation
```

## Error Handling

**Breaking Changes**: Identify backward compatibility issues and provide migration guide.

**Test Failures**: Fix tests to match refactored code or identify regression issues.

**Complex Refactoring**: Break into smaller incremental changes.

## Common Refactoring Patterns

**Pattern 1: Hardcoded Colors → AT&T Palette**
- Identify all color values
- Map to AT&T brand colors
- Update TailwindCSS config
- Replace in components

**Pattern 2: any Types → Proper Types**
- Identify all `any` usage
- Create interface definitions
- Add type guards
- Update function signatures

**Pattern 3: Large Component → Smaller Components**
- Identify logical sections
- Extract to separate files
- Create shared props interface
- Maintain state at appropriate level

**Pattern 4: Inline Styles → Reusable Primitives**
- Identify repeated patterns
- Create UI primitive component
- Add variant props
- Replace inline usage

## Examples

**Example 1**: `/refactor-frontend Update colors to AT&T brand palette`

**Example 2**: `/refactor-frontend Improve accessibility for form components`

**Example 3**: `/refactor-frontend Split large Dashboard component into smaller pieces`

**Example 4**: `/refactor-frontend Remove all any types and add proper TypeScript`

## References

Constitution: (pre-loaded above)
Environment Config: `${ARCHETYPES_BASEDIR}/frontend-only/templates/env-config.yaml`
