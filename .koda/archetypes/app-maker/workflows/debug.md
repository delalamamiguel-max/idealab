---
description: Debug web application errors including frontend crashes, API failures, and deployment issues (App Maker)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype app-maker --json ` and parse for debugging tools availability.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: error description, error messages/stack traces, affected components/endpoints, steps to reproduce, environment (dev/staging/prod). Request clarification if incomplete.

### 4. Categorize Error Type

Analyze error to determine category:

**Frontend Errors**:
- Component crashes / render errors
- State management issues
- API call failures
- Build/bundle errors
- Hydration mismatches (SSR)
- Memory leaks
- Performance degradation

**Backend Errors**:
- API endpoint failures (4xx, 5xx)
- Database connection issues
- Authentication/authorization failures
- Validation errors
- Timeout errors
- Memory/resource exhaustion

**Integration Errors**:
- CORS issues
- Authentication token problems
- API contract mismatches
- Third-party service failures

**Deployment Errors**:
- Build failures
- Environment variable issues
- Docker container crashes
- SSL/certificate problems

### 5. Debug Frontend Errors

**A. Component Crashes**:
```typescript
// Common issue: Missing null checks
// ERROR: Cannot read property 'name' of undefined

// DEBUG APPROACH:
1. Check if data exists before accessing
2. Add optional chaining: user?.name
3. Add default values: user?.name ?? 'Unknown'
4. Add loading state checks
```

**B. State Management Issues**:
```typescript
// Common issue: Stale closure in useEffect

// DEBUG APPROACH:
1. Check useEffect dependencies
2. Verify state updates trigger re-renders
3. Use React DevTools to inspect state
4. Add console.logs to track state changes
```

**C. API Call Failures**:
```typescript
// Common issue: CORS or network errors

// DEBUG APPROACH:
1. Check browser console for CORS errors
2. Verify API URL is correct
3. Check network tab for request/response
4. Verify authentication token is sent
5. Check backend CORS configuration
```

**D. Build Errors**:
```bash
# Common issue: Module resolution failures

# DEBUG APPROACH:
1. Clear node_modules and reinstall
2. Check import paths (relative vs absolute)
3. Verify TypeScript configuration
4. Check for circular dependencies
```

### 6. Debug Backend Errors

**A. API Endpoint Failures**:
```python
# Common issue: Unhandled exceptions

# DEBUG APPROACH:
1. Check FastAPI logs for stack trace
2. Add try-except blocks with logging
3. Verify input validation with Pydantic
4. Test endpoint with curl/Postman
5. Check database connection
```

**B. Database Issues**:
```python
# Common issue: Connection pool exhausted

# DEBUG APPROACH:
1. Check connection pool settings
2. Verify connections are being closed
3. Check for long-running queries
4. Monitor database connections
5. Add connection timeout configuration
```

**C. Authentication Failures**:
```python
# Common issue: Invalid JWT tokens

# DEBUG APPROACH:
1. Verify token format (Bearer <token>)
2. Check token expiration
3. Verify JWT secret matches
4. Check Entra ID configuration
5. Test token validation manually
```

### 7. Debug Integration Errors

**A. CORS Issues**:
```python
# SYMPTOM: "Access-Control-Allow-Origin" header missing

# FIX:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**B. API Contract Mismatches**:
```typescript
// SYMPTOM: Frontend expects different data structure

// DEBUG APPROACH:
1. Compare frontend TypeScript types with backend Pydantic models
2. Check API response in browser DevTools
3. Verify API versioning matches
4. Use OpenAPI spec for source of truth
```

### 8. Debug Performance Issues

**A. Slow Page Loads**:
```typescript
// DEBUG APPROACH:
1. Use React DevTools Profiler
2. Check for unnecessary re-renders
3. Identify expensive computations (add useMemo)
4. Check for missing code splitting
5. Run Lighthouse audit for insights
```

**B. Memory Leaks**:
```typescript
// Common issue: Missing cleanup in useEffect

// FIX:
useEffect(() => {
  const subscription = api.subscribe();
  
  return () => {
    subscription.unsubscribe();  // Cleanup
  };
}, []);
```

**C. Large Bundle Sizes**:
```bash
# DEBUG APPROACH:
1. Run: npm run build --analyze
2. Identify large dependencies
3. Use dynamic imports for heavy components
4. Remove unused dependencies
5. Enable tree shaking
```

### 9. Debug Deployment Issues

**A. Build Failures**:
```bash
# Common issue: Missing environment variables

# DEBUG APPROACH:
1. Check CI/CD logs for error details
2. Verify all env vars are set
3. Test build locally: npm run build
4. Check for missing dependencies in package.json
```

**B. Runtime Errors in Production**:
```typescript
// Common issue: Environment-specific config

// DEBUG APPROACH:
1. Check production error logs
2. Verify environment variables are set correctly
3. Test production build locally
4. Check for differences in dev vs prod behavior
5. Enable error tracking (Sentry)
```

### 10. Provide Debugging Guidance

For each identified issue:

**Issue Description**: Clear explanation of the problem

**Root Cause**: Why the error occurred

**Fix**: Specific code changes needed
```typescript
// Example fix with before/after
```

**Prevention**: How to avoid in future (tests, linting, patterns)

**Testing**: How to verify the fix works

### 11. Generate Debug Report

```
🐛 Debugging Report

📍 Error Type: <category>
📍 Severity: <critical/high/medium/low>
📍 Affected Components: <list>

🔍 Root Cause Analysis:
<Detailed explanation of why error occurred>

🛠️ Fixes Applied:
1. <Fix description> - <file>:<line>
2. <Fix description> - <file>:<line>
3. ...

✅ Verification Steps:
1. <Test to verify fix>
2. <Expected behavior>

🚫 Prevention Measures:
- Add unit test: <test description>
- Update linting rule: <rule>
- Add validation: <where>

📋 Additional Recommendations:
- <Recommendation 1>
- <Recommendation 2>

💡 Useful Debug Commands:
- Check logs: <command>
- Test locally: <command>
- Monitor: <command>
```

### 12. Validate Fix

Run tests to verify fix: `npm test && cd backend && pytest`

Report test results and confirm issue is resolved.

## Error Handling

**Cannot Reproduce**: Request additional information (exact steps, environment, error logs).

**Multiple Root Causes**: Prioritize issues and address in order of severity.

**Requires External Fix**: Identify external dependencies (third-party APIs, infrastructure) and provide workarounds.

## Common Debug Patterns

**Pattern 1: CORS Error**
- Symptom: Network error, no response from API
- Root Cause: Backend not configured for frontend origin
- Fix: Update CORS middleware with frontend URL

**Pattern 2: Hydration Mismatch**
- Symptom: Content flashes/changes after initial load
- Root Cause: Server and client render different content
- Fix: Ensure consistent data/logic between SSR and CSR

**Pattern 3: Memory Leak**
- Symptom: App becomes slow over time
- Root Cause: Event listeners or subscriptions not cleaned up
- Fix: Add cleanup functions to useEffect

**Pattern 4: Authentication Loop**
- Symptom: Redirects infinitely between login and protected route
- Root Cause: Token validation logic incorrect
- Fix: Check token validation and route guard logic

**Pattern 5: Database Connection Pool Exhausted**
- Symptom: API becomes unresponsive after many requests
- Root Cause: Connections not being released
- Fix: Use context managers or ensure connection closure

## Examples

**Example 1**: `/debug-app "Cannot read property 'map' of undefined" in UserList component`
Output: Identifies missing null check, provides fix with optional chaining

**Example 2**: `/debug-app API returns 500 error when creating new user`
Output: Finds database constraint violation, fixes validation logic

**Example 3**: `/debug-app Build fails with "Module not found" error`
Output: Identifies incorrect import path, provides correct relative path

**Example 4**: `/debug-app Page loads slowly with large dataset`
Output: Adds pagination, implements virtual scrolling, optimizes queries

## References

Constitution: (pre-loaded above)
