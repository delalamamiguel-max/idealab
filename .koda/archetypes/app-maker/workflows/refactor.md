---
description: Refactor web application to apply security, performance, and AT&T brand best practices (App Maker)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype app-maker --json ` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: target files/directories, refactoring goals (performance, security, brand compliance, code quality, accessibility), specific issues to address. Request clarification if incomplete.

### 4. Analyze Existing Code

Scan target application for issues:

**Brand Compliance**:
- Non-ATT colors used (not #009FDB, #00388F, etc.)
- Missing or incorrect ATT Aleck font
- AT&T Blue not dominant
- Incorrect color proportions
- Poor contrast ratios (<4.5:1)

**Security Issues**:
- Hardcoded secrets or API keys
- Missing input validation
- XSS vulnerabilities (dangerouslySetInnerHTML)
- SQL injection risks
- Missing CSRF protection
- Insecure HTTP usage
- Missing security headers

**Performance Issues**:
- Large bundle sizes (>200KB)
- Missing code splitting
- Unoptimized images
- No lazy loading
- Missing memoization
- Inefficient API calls
- Missing caching strategies

**Code Quality**:
- TypeScript `any` types
- Large functions (>50 lines)
- Duplicate code
- Poor component organization
- Missing error handling
- No loading states

**Accessibility**:
- Missing ARIA labels
- No keyboard navigation
- Non-semantic HTML
- Poor focus management
- Missing alt text

Report findings with severity (critical/high/medium/low) and file locations.

### 5. Generate Refactoring Plan

Create prioritized plan:

**Phase 1: Critical Issues** (Hard-stop violations):
1. Remove hardcoded secrets → environment variables
2. Add input validation → Zod schemas + Pydantic models
3. Fix XSS vulnerabilities → sanitize user content
4. Enforce HTTPS → configuration updates
5. Fix accessibility violations → ARIA labels, semantic HTML

**Phase 2: Brand Compliance**:
1. Update color palette → AT&T colors
2. Replace fonts → ATT Aleck Sans
3. Redesign CTAs → Cobalt buttons
4. Adjust color proportions → AT&T Blue dominant
5. Fix contrast issues → ensure 4.5:1 ratio

**Phase 3: Performance Optimization**:
1. Implement code splitting → dynamic imports
2. Optimize images → WebP format, lazy loading
3. Add memoization → useMemo, useCallback
4. Optimize API calls → React Query with caching
5. Reduce bundle size → tree shaking, compression

**Phase 4: Code Quality**:
1. Remove `any` types → proper TypeScript types
2. Split large functions → smaller, focused functions
3. Extract duplicate code → shared utilities
4. Reorganize components → proper structure
5. Add error boundaries → comprehensive error handling

### 6. Apply Refactorings

Execute refactorings in priority order:

**A. Security Refactorings**:
```typescript
// BEFORE: Hardcoded API key
const API_KEY = 'sk_live_123456';

// AFTER: Environment variable
const API_KEY = import.meta.env.VITE_API_KEY;
```

```typescript
// BEFORE: No input validation
const handleSubmit = (data) => { api.post('/users', data); };

// AFTER: Zod validation
const userSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

const handleSubmit = (data) => {
  const validated = userSchema.parse(data);
  api.post('/users', validated);
};
```

**B. Brand Compliance Refactorings**:
```typescript
// BEFORE: Generic blue color
<button className="bg-blue-500">Click me</button>

// AFTER: AT&T Cobalt for CTA
<button className="bg-att-cobalt text-white">Click me</button>
```

```css
/* BEFORE: Generic font */
body { font-family: Arial, sans-serif; }

/* AFTER: ATT Aleck Sans */
body { font-family: 'ATT Aleck Sans', system-ui, sans-serif; }
```

**C. Performance Refactorings**:
```typescript
// BEFORE: No code splitting
import HeavyChart from './HeavyChart';

// AFTER: Dynamic import
const HeavyChart = lazy(() => import('./HeavyChart'));
```

```typescript
// BEFORE: Inefficient re-renders
const ExpensiveComponent = ({ data }) => {
  const result = expensiveCalculation(data);
  return <div>{result}</div>;
};

// AFTER: Memoization
const ExpensiveComponent = ({ data }) => {
  const result = useMemo(() => expensiveCalculation(data), [data]);
  return <div>{result}</div>;
};
```

**D. Accessibility Refactorings**:
```typescript
// BEFORE: Non-semantic div
<div onClick={handleClick}>Click me</div>

// AFTER: Semantic button with ARIA
<button 
  onClick={handleClick}
  aria-label="Submit form"
>
  Click me
</button>
```

**E. Backend Refactorings**:
```python
# BEFORE: SQL injection risk
query = f"SELECT * FROM users WHERE id = {user_id}"

# AFTER: Parameterized query
query = "SELECT * FROM users WHERE id = :user_id"
result = db.execute(query, {"user_id": user_id})
```

### 7. Add Missing Features

Implement missing mandatory patterns:

**Error Boundaries**:
```typescript
// src/components/ErrorBoundary.tsx
export class ErrorBoundary extends Component {
  state = { hasError: false };
  
  static getDerivedStateFromError() {
    return { hasError: true };
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

**Loading States**:
```typescript
// Add loading skeletons
{isLoading ? <Skeleton /> : <DataTable data={data} />}
```

**Rate Limiting** (Backend):
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/public")
@limiter.limit("100/hour")
def public_endpoint():
    return {"message": "success"}
```

### 8. Update Tests

Ensure tests cover refactored code:
- Update unit tests for new functions
- Add integration tests for security features
- Update E2E tests for UI changes
- Add accessibility tests

### 9. Validate and Report


**Report Results**:
```
✅ Application Refactored

📊 Refactoring Summary:
   Phase 1 (Critical): 12 issues fixed
   Phase 2 (Brand): 8 improvements applied
   Phase 3 (Performance): 10 optimizations added
   Phase 4 (Code Quality): 15 improvements made

🎨 Brand Compliance:
   ✓ AT&T color palette applied
   ✓ ATT Aleck font integrated
   ✓ Cobalt CTA buttons
   ✓ Color contrast fixed (4.5:1)

🔒 Security Improvements:
   ✓ Secrets moved to environment variables
   ✓ Input validation added (Zod + Pydantic)
   ✓ XSS protection implemented
   ✓ CSRF protection enabled
   ✓ Security headers configured

⚡ Performance Gains:
   ✓ Bundle size reduced by 40% (320KB → 190KB)
   ✓ Code splitting implemented
   ✓ Images optimized (lazy loading)
   ✓ First Load: 1.2s → 0.8s
   ✓ Lighthouse score: 72 → 94

♿ Accessibility:
   ✓ ARIA labels added to interactive elements
   ✓ Keyboard navigation enabled
   ✓ Semantic HTML structure
   ✓ Focus management improved

📋 Files Modified: <count> files
📋 Lines Changed: +<additions> -<deletions>

⚠️ Remaining Issues:
   - <Any issues that couldn't be automatically fixed>

📋 Next Steps:
   1. Review refactored code for correctness
   2. Run test suite: npm test && pytest
   3. Manual testing of affected features
   4. Deploy to staging for validation
   5. Monitor performance metrics

💡 Commands:
   - Run tests: npm test
   - Check bundle: npm run build --analyze
   - Lighthouse audit: npm run lighthouse
```

## Error Handling

**Cannot Fix Automatically**: Report issues requiring manual intervention with clear guidance.

**Breaking Changes**: Warn about changes that may affect functionality, suggest testing strategy.

**Conflicting Requirements**: Explain conflicts (e.g., performance vs. features) and suggest trade-offs.

## Examples

**Example 1**: `/refactor-app Apply AT&T brand guidelines to existing dashboard`
Output: Updated colors, fonts, CTAs; brand compliance report

**Example 2**: `/refactor-app Fix security vulnerabilities in authentication flow`
Output: Environment variables, input validation, HTTPS enforcement

**Example 3**: `/refactor-app Improve performance of product listing page`
Output: Code splitting, lazy loading, memoization, bundle size reduction

## References

Constitution: (pre-loaded above)
