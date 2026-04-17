---
description: Review code quality and TDD discipline — test coverage, Red-Green-Refactor compliance, and test design quality
---

User input: $ARGUMENTS

## Behavioral Rules

> **CRITICAL: This workflow performs code review and validation with a TDD lens, NOT code generation.**
>
> - **DO NOT** write, generate, or modify code unless explicitly fixing critical issues
> - **ALWAYS** present a review report with findings, recommendations, and severity ratings
> - **ANALYZE** uncommitted changes by default, or specific pull requests if instructed
> - **VALIDATE** against project conventions from `PROJECT_STRUCTURE_AND_CONVENTIONS.md`
> - **CHECK** TDD discipline (test-first, Red-Green-Refactor compliance), test design quality, coverage thresholds, performance, security, maintainability, reusability, duplicate code, SOLID principles, design patterns, and all software engineering best practices
> - **VERIFY** that every new source file has a corresponding test file before marking review as passing
> - If the user wants to implement fixes, direct them to use the `tdd-scaffold` or `tdd-refactor` workflow

## Execution Steps

### 0. Determine Review Scope

Parse $ARGUMENTS to identify what to review:

**Review Targets:**
- **Uncommitted changes** (default): Review all modified files not yet committed
- **Pull request**: Review specific PR if URL or PR number provided
- **Specific files/directories**: Review only specified paths
- **Branch comparison**: Compare current branch with target branch

**Extract:**
- Review target (uncommitted/PR/files/branch)
- PR number or URL (if applicable)
- Specific file paths (if provided)
- Comparison branch (default: main/master)

### 1. Gather Code Context

**Identify Project Structure:**
```bash
# Detect project type
- Look for package.json, requirements.txt, pom.xml → Application type
- Look for .tf, terraform/ → Infrastructure as Code
- Look for Dockerfile, helm/, k8s/ → Container/Kubernetes
- Look for frontend/, backend/ folders → Multi-component project
```

**Load Project Conventions:**
1. Check for `{frontend_folder}/docs/PROJECT_STRUCTURE_AND_CONVENTIONS.md`
2. Check for `{backend_folder}/docs/PROJECT_STRUCTURE_AND_CONVENTIONS.md`
3. Check for `./docs/PROJECT_STRUCTURE_AND_CONVENTIONS.md`
4. If not found, use default conventions from tdd-scaffold workflow

**Identify Changed Files:**
```bash
# For uncommitted changes
git status --porcelain
git diff --name-only

# For pull request
git diff origin/main...HEAD --name-only

# For specific files
Use provided file paths
```

### 2. Categorize Files by Type

Group files for targeted review:

**Frontend Files:**
- `.tsx`, `.jsx`, `.ts`, `.js` in frontend/src/components/
- React components, hooks, contexts
- Type definitions in types/
- Utilities and constants

**Backend Files:**
- `.py`, `.js`, `.ts`, `.java` in backend/src/
- API routes, controllers, services
- Models, schemas, repositories
- Middleware, utilities

**Infrastructure Files:**
- `.tf`, `.yaml`, `.yml` (Kubernetes, Terraform)
- Dockerfiles, docker-compose files
- CI/CD pipeline configurations

**Configuration Files:**
- `package.json`, `requirements.txt`, `pom.xml`
- `.env.example`, config files
- `.gitignore`, `.eslintrc`, etc.

**Documentation Files:**
- `.md` files
- API documentation
- README updates

### 3. Perform Code Quality Analysis

For each changed file, analyze across all dimensions below. Every section is mandatory.

---

#### 3.1. Duplicate Code Detection (DRY Principle)

**Actively scan for:**
- Identical or near-identical code blocks copied across files or functions
- Logic repeated in multiple components/services that can be extracted into a shared utility
- Copy-pasted error handling, validation, or transformation logic
- Repeated SQL queries or ORM patterns that should be in a repository/service layer
- Duplicated constants or configuration values defined in multiple places
- Similar React components or hooks that differ only by minor props (consolidate with generics/props)

**For each duplicate found, report:**
- All locations where the duplication occurs (file + line)
- The recommended abstraction (utility function, shared hook, base class, mixin, generic component)
- Estimated lines of code saved by refactoring
- Risk level of introducing the shared abstraction

**Common Duplicate Code Patterns to Flag:**
- Same validation logic in multiple API endpoints → extract to a validator middleware
- Same date/string/number formatting across components → extract to `utils/formatters`
- Same `try-catch` boilerplate around async calls → extract to a `withErrorHandling` wrapper
- Same API call patterns → extract to a dedicated service/repository layer
- Repeated `if-else` type checks → use polymorphism or a strategy map

---

#### 3.2. Code Reusability Analysis

**Evaluate whether code is written for reuse:**
- Are functions generic enough to handle multiple use cases, or are they over-specialized?
- Are magic strings/numbers replaced with named constants in a shared location?
- Are shared types/interfaces defined once and imported, or re-declared in multiple files?
- Are utility functions placed in a shared utilities module vs. embedded in a single component?
- Are React components decomposed to be composable and reusable across pages?
- Are backend service methods designed to be reusable by multiple controllers/routes?
- Is configuration data externalized and reusable (environment variables, config files)?
- Are common patterns (pagination, filtering, sorting) abstracted into reusable helpers?

**Reusability Score per Module:** Rate as `High / Medium / Low` with explanation.

**Recommend abstractions where reusability is low:**
- Shared hooks for repeated stateful logic (data fetching, form state, auth checks)
- Generic components for repeated UI patterns (tables, modals, form fields)
- Service/repository classes for repeated data access patterns
- Middleware for repeated cross-cutting concerns (logging, auth, validation)
- Utility libraries for repeated domain logic (calculations, transformations)

---

#### 3.3. Convention Compliance

**Frontend (React + Vite + TypeScript):**
- ✓ One component per file
- ✓ PascalCase naming with `Component` or `Page` suffix
- ✓ No type definitions in component files
- ✓ All types in `/src/types/` directory
- ✓ Proper imports: `import type { TypeName } from '../types'`
- ✓ File naming: PascalCase for components, camelCase for utilities
- ✓ Directory naming: kebab-case for multi-word
- ✓ Function naming: camelCase, verb-first (`handleSubmit`, `fetchUser`)
- ✓ Constants: SCREAMING_SNAKE_CASE in `src/utils/`
- ✓ TypeScript strict mode compliance — no `any` types
- ✓ Barrel exports (`index.ts`) for clean imports
- ✓ No inline styles — use CSS modules or Tailwind utility classes consistently

**Backend (FastAPI/Express/Spring Boot):**
- ✓ Proper file naming (snake_case for Python, camelCase for JS/TS)
- ✓ API endpoint conventions (plural nouns, proper HTTP methods)
- ✓ Request/response validation with schemas (Pydantic, Zod, JOI, etc.)
- ✓ Proper error handling with custom exceptions and error codes
- ✓ Authentication and authorization checks on every protected route
- ✓ Input validation and sanitization before processing
- ✓ Database query optimization and proper ORM usage
- ✓ Proper use of transactions for multi-step operations
- ✓ Consistent response envelope structure (`data`, `error`, `meta`)

**Infrastructure:**
- ✓ Terraform best practices (modules, variables, outputs, remote state)
- ✓ Kubernetes resource limits and requests defined
- ✓ Docker multi-stage builds for minimal image size
- ✓ Health checks and readiness probes configured
- ✓ Secret management via vault/secrets manager — no hardcoded secrets anywhere

---

#### 3.4. SOLID Principles Analysis

Evaluate all classes, modules, and functions against SOLID principles:

**S — Single Responsibility Principle (SRP):**
- Does each class/module/function have exactly one reason to change?
- Flag: Functions doing validation + business logic + data persistence together
- Flag: Components handling UI rendering + API calls + state management simultaneously
- Recommendation: Split into separate layers (controller, service, repository)

**O — Open/Closed Principle (OCP):**
- Is the code open for extension but closed for modification?
- Flag: Long if-else or switch chains that require modification for each new type
- Recommendation: Use strategy pattern, polymorphism, or plugin architecture

**L — Liskov Substitution Principle (LSP):**
- Can subclasses/implementations be substituted for their base types without breaking behavior?
- Flag: Subclasses that override methods to throw `NotImplemented` or change expected behavior
- Flag: Interface implementations that ignore required contract behaviors

**I — Interface Segregation Principle (ISP):**
- Are interfaces/types lean and focused, or do implementors depend on methods they don't use?
- Flag: Large interfaces where implementations only use a subset of methods
- Recommendation: Split into smaller, focused interfaces

**D — Dependency Inversion Principle (DIP):**
- Do high-level modules depend on abstractions, not concrete implementations?
- Flag: Direct instantiation of dependencies inside classes (use injection instead)
- Flag: Hard-coded service URLs, database connections, or third-party SDK calls without abstraction
- Recommendation: Use dependency injection, interfaces, and configuration-driven wiring

---

#### 3.5. Design Patterns Analysis

Identify where design patterns should be applied or are misapplied:

**Creational Patterns:**
- Factory/Abstract Factory: Used where object creation logic is complex or varies by type?
- Singleton: Applied correctly (e.g., DB connection pools, config managers)? Not overused?
- Builder: Used for complex object construction with many optional parameters?

**Structural Patterns:**
- Adapter: Used to integrate incompatible interfaces (third-party libraries, legacy code)?
- Decorator: Used to extend functionality without modifying existing classes?
- Facade: Used to simplify complex subsystem interactions?
- Proxy: Used for caching, access control, or lazy initialization?

**Behavioral Patterns:**
- Strategy: Used to swap algorithms or behaviors at runtime?
- Observer/Event-Driven: Used for decoupled communication between components?
- Command: Used for undoable operations or queued actions?
- Repository: Used to abstract data access from business logic?
- Chain of Responsibility: Used for middleware pipelines or validation chains?

**Anti-Patterns to Flag:**
- God Object/Class: One class doing too much — split it
- Spaghetti Code: Tangled control flow with no clear structure — refactor with patterns
- Magic Numbers/Strings: Replace with named constants
- Premature Optimization: Overly complex code without proven performance need
- Anemic Domain Model: Business logic scattered in services instead of domain objects
- Shotgun Surgery: A single change requires modifications across many unrelated files
- Feature Envy: A method that uses data from another class more than its own

---

#### 3.6. Performance Analysis

**Frontend Performance:**
- Unnecessary re-renders (missing `useMemo`, `useCallback`, `React.memo`)
- Large bundle sizes (check wildcard imports, missing tree-shaking, lazy loading)
- Inefficient state management (storing derived state, over-fetching)
- Missing code splitting (`React.lazy`, dynamic `import()`)
- Unoptimized images or assets (missing compression, wrong format)
- Excessive or redundant API calls (missing debounce, caching, deduplication)
- Memory leaks (missing cleanup in `useEffect`, unsubscribed observables/listeners)
- Blocking the main thread (heavy synchronous computation)

**Backend Performance:**
- N+1 query problems (use `JOIN`, `eager loading`, or batching)
- Missing database indexes on frequently filtered/sorted columns
- Inefficient algorithms (O(n²) or worse when O(n log n) is achievable)
- Unnecessary data fetching (select only needed columns, not `SELECT *`)
- Missing caching strategies (Redis, in-memory cache for hot data)
- Blocking I/O operations in async code (use `async/await` properly)
- Resource-intensive operations without pagination or streaming
- Missing connection pooling for databases and external services

**Infrastructure Performance:**
- Under-provisioned CPU/memory resources
- Missing Horizontal Pod Autoscaler (HPA) configuration
- Inefficient container images (large layers, unnecessary packages)
- Missing CDN for static assets and media
- Missing request compression (gzip/brotli)

---

#### 3.7. Security Analysis

**OWASP Top 10 — Check every applicable item:**
- A01 Broken Access Control: Missing authorization checks, IDOR vulnerabilities
- A02 Cryptographic Failures: Sensitive data unencrypted in transit or at rest, weak hashing
- A03 Injection: SQL, NoSQL, LDAP, OS command injection via unsanitized input
- A04 Insecure Design: Missing threat modeling, insecure design choices
- A05 Security Misconfiguration: Debug mode enabled, default credentials, verbose errors
- A06 Vulnerable Components: Outdated dependencies with known CVEs
- A07 Auth Failures: Broken session management, weak password policies, no MFA
- A08 Software/Data Integrity Failures: Missing code signing, insecure deserialization
- A09 Logging Failures: Sensitive data in logs, insufficient audit trails
- A10 SSRF: User-controlled URLs fetched without validation

**Critical Security Checks:**
- Hardcoded secrets, API keys, tokens, or passwords in code or config
- SQL/NoSQL injection via string concatenation instead of parameterized queries
- XSS via unescaped user input rendered as HTML
- CSRF protection missing on state-changing endpoints
- Insecure direct object references (IDOR) — user can access another user's data
- Authentication bypass or missing auth checks on sensitive routes
- Sensitive data exposed in API responses, URLs, or logs
- Insecure dependencies — run `npm audit` / `pip audit` / `snyk test`
- Missing or misconfigured rate limiting on authentication and API endpoints
- Improper error handling that exposes stack traces or internal details
- Insecure file uploads (missing type validation, size limits, path traversal)
- Timing attacks in authentication comparisons (use constant-time comparison)

**Frontend Security:**
- XSS prevention (`dangerouslySetInnerHTML` usage, proper sanitization with DOMPurify)
- Secure storage (no sensitive data in `localStorage`/`sessionStorage` — use `httpOnly` cookies)
- HTTPS enforcement and HSTS headers
- Content Security Policy (CSP) headers configured
- Dependency vulnerabilities (`npm audit`)
- Exposed API keys or tokens in client-side code

**Backend Security:**
- SQL injection prevention (ORM or parameterized queries everywhere)
- JWT/session token security (short expiry, rotation, revocation support)
- Password hashing with bcrypt/argon2 (not MD5/SHA1)
- CORS configuration (no wildcard `*` in production)
- API rate limiting per user and per IP
- Input validation and sanitization on every endpoint
- Secrets loaded from environment/vault — never from code

---

#### 3.8. Code Maintainability Analysis

**Code Complexity Metrics:**
- Cyclomatic complexity: Flag functions with > 10 decision branches
- Function length: Flag functions exceeding 50 lines — split into smaller units
- File length: Flag files exceeding 300-500 lines — split by responsibility
- Deep nesting: Flag code nested > 3-4 levels — use early returns/guard clauses
- Parameter count: Flag functions with > 4 parameters — use an options object

**Code Clarity:**
- Meaningful, intention-revealing variable and function names (no `temp`, `data2`, `x`)
- No misleading names (name must match what the function actually does)
- Complex logic has explanatory comments (the "why", not the "what")
- Self-documenting code structure reduces the need for comments
- Consistent formatting and code style enforced by linter/formatter
- Error messages are descriptive and actionable for users and developers

**Readability Best Practices:**
- Prefer positive conditionals (`isValid` over `!isInvalid`)
- Use early returns / guard clauses to reduce nesting
- Avoid magic numbers and magic strings — use named constants
- Avoid deep method chaining that obscures intent
- Boolean parameters should be avoided (use named options objects)

**Architecture & Modularity:**
- Separation of concerns: UI, business logic, and data access are in separate layers
- Single Responsibility: Each module/class/function has one clear purpose
- Low coupling: Modules communicate through well-defined interfaces, not internal details
- High cohesion: Related logic is grouped together in the same module
- Dependency direction flows inward (domain layer has no external dependencies)
- Circular dependencies flagged and eliminated

**Technical Debt:**
- Flag TODO/FIXME/HACK comments and assess if they should be resolved now
- Identify workarounds that mask underlying problems
- Flag deprecated API usage that needs migration
- Identify dead code (unused imports, functions, variables) that should be removed

---

#### 3.9. Extensibility & Scalability Analysis

**Design for Extensibility:**
- Open/Closed Principle applied (extend behavior without modifying existing code)
- Plugin/hook points available for future features
- Feature flags or configuration-driven behavior for easy toggling
- Event-driven design for decoupled future extensions

**Scalability Considerations:**
- Stateless service design (no in-memory session state that blocks horizontal scaling)
- Proper use of message queues for async/background processing
- Database connection pooling configured
- Async/await used for all I/O operations
- Long-running tasks offloaded to background workers
- Paginated APIs — no unbounded result sets returned

**Testability:**
- Dependency injection used so dependencies can be mocked
- Pure functions preferred for business logic (no hidden side effects)
- Side effects isolated and wrapped for easy testing
- Test boundaries clearly defined between unit, integration, and E2E tests

---

#### 3.10. TDD Discipline Review (MANDATORY)

> **Every code review MUST include this TDD-specific section. Non-TDD compliant code must be flagged.**

**Test-First Discipline:**
- Flag any new source file that does NOT have a corresponding test file — this is a TDD violation
- Check that test files were likely created BEFORE or alongside implementation (compare file timestamps or git history)
- Verify that no production logic was introduced without at least one failing test to drive it
- Flag empty test files, skipped tests (`xtest`, `xit`, `@pytest.mark.skip`), or placeholder tests with no assertions

**Red-Green-Refactor Cycle Compliance:**
- Review commit history for evidence of Red → Green → Refactor cycles (small, incremental commits)
- Flag large implementation commits without corresponding test commits (suggests code-first, not TDD)
- Check for over-engineering: if implementation is complex but tests are minimal, the Refactor phase may have exceeded scope

**Test Design Quality:**
- **Test naming:** Every test name must describe behavior, not implementation (e.g., `should return 401 when token is expired`, NOT `test_auth_function`)
- **AAA structure:** Tests must follow Arrange → Act → Assert (or Given/When/Then for BDD) without mixing concerns
- **Single assertion principle:** Each test should verify ONE behavior. Flag tests with unrelated multiple assertions
- **No test logic:** Flag tests containing `if`, `for`, `while`, or complex conditional logic — tests must be declarative
- **Test isolation:** Tests must not depend on execution order. Flag shared mutable state between test cases
- **Meaningful failures:** A failing test must clearly communicate WHAT failed and WHY — no cryptic assertion messages
- **Test doubles appropriately used:** Flag over-mocking (mocking things that don't need mocking) and under-mocking (testing real I/O where it should be isolated)

**Coverage Quality:**
- Check that both **happy paths** AND **error/edge-case paths** are tested for every function
- Flag functions with only happy-path tests — error handling paths must be tested too
- Verify boundary values are tested (empty strings, null, 0, max values, etc.)
- Check that coverage is meaningful (not just line coverage — behavioral coverage matters)
- Flag tests that only test implementation details (checking internal state, private method calls) rather than observable behavior

**TDD Review Score:**

| TDD Dimension | Status | Severity |
|---------------|--------|----------|
| Every source file has a test file | ✓ Pass / ✗ Fail | Critical if fail |
| Test names describe behavior | ✓ Pass / ✗ Fail | Major if fail |
| AAA structure followed | ✓ Pass / ✗ Fail | Minor if fail |
| No logic inside tests | ✓ Pass / ✗ Fail | Major if fail |
| Tests are isolated (no order dependency) | ✓ Pass / ✗ Fail | Major if fail |
| Both happy path and error paths tested | ✓ Pass / ✗ Fail | Critical if fail |
| No skipped/placeholder tests | ✓ Pass / ✗ Fail | Major if fail |
| Test doubles used appropriately | ✓ Pass / ✗ Fail | Minor if fail |

---

#### 3.11. Best Practices Validation

**General Software Engineering Best Practices:**
- Error handling: all failure paths handled explicitly (no silent catches)
- Logging: structured logging at appropriate levels (debug/info/warn/error), no sensitive data
- Configuration: all environment-specific values in environment variables or config files
- Documentation: public APIs, complex logic, and non-obvious decisions documented
- Immutability: prefer immutable data structures to avoid unexpected mutations
- Fail-fast: validate inputs at entry points, fail loudly with clear messages
- Code reusability: shared logic extracted to utilities, not duplicated

**Frontend Best Practices:**
- React hooks rules compliance (no hooks in conditions or loops)
- Proper component composition (small, focused, composable components)
- Accessibility: ARIA labels, semantic HTML, keyboard navigation, color contrast
- Responsive design for all screen sizes
- Loading states and error states handled for all async operations
- Form validation with clear user feedback (client-side + server-side)
- Optimistic UI updates with proper rollback on failure

**Backend Best Practices:**
- RESTful API design (proper resource naming, HTTP methods, status codes)
- API versioning strategy in place (`/api/v1/`)
- Request/response validation on every endpoint
- Database migrations versioned and reversible
- Background jobs are idempotent (safe to retry on failure)
- Graceful shutdown: in-flight requests completed before process exit
- Health check endpoints (`/health`, `/ready`) implemented

**Testing Best Practices:**
- Test coverage target: > 80% for business logic
- Unit tests: test one thing in isolation with all dependencies mocked
- Integration tests: test component interactions with real or realistic dependencies
- E2E tests: cover critical user flows
- Test naming: `should [expected behavior] when [condition]`
- Tests are independent — no shared mutable state between tests
- No logic in tests (no `if`, loops — keep tests simple and declarative)
- Edge cases and failure paths tested, not just the happy path

**Dependency Management:**
- No unused dependencies in `package.json` / `requirements.txt`
- Dependencies pinned to specific versions (or ranges with upper bounds)
- No deprecated packages in use
- Security vulnerabilities checked (`npm audit`, `pip audit`, `snyk`)
- Peer dependencies compatible with current runtime versions

---

### 4. Generate Review Report

Present findings in a structured format:

```markdown
# Code Review Report

**Review Scope:** [Uncommitted Changes / PR #123 / Specific Files]
**Review Date:** [Date]
**Files Reviewed:** [Count]
**Total Issues Found:** [Count]

## Executive Summary

- **Critical Issues:** [Count] 🔴
- **High Priority:** [Count] 🟠
- **Medium Priority:** [Count] 🟡
- **Low Priority:** [Count] 🟢
- **Suggestions:** [Count] 💡

**Overall Assessment:** [Pass / Pass with Recommendations / Needs Changes / Blocked]

---

## Critical Issues 🔴

### [File Path] - [Issue Title]
**Severity:** Critical
**Category:** [Security / Performance / Correctness / Data Integrity]
**Line(s):** [Line Number(s)]
**Principle Violated:** [SOLID / DRY / OWASP / Best Practice]

**Issue:**
[Detailed description of the problem]

**Code:**
```[language]
[Problematic code snippet]
```

**Impact:**
[Explanation of why this is critical — business, security, or system impact]

**Recommendation:**
[Specific fix or approach with rationale]

**Suggested Fix:**
```[language]
[Fixed code example]
```

---

## High Priority Issues 🟠

[Same format as Critical Issues]

---

## Medium Priority Issues 🟡

[Same format as Critical Issues]

---

## Low Priority Issues 🟢

[Same format as Critical Issues]

---

## Suggestions 💡

[Same format as Critical Issues]

---

## Duplicate Code Analysis

**Duplicate Code Found:** [Yes / No]
**Total Duplications:** [Count]
**Estimated Lines Affected:** [Count]

| Location A | Location B | Lines | Recommended Abstraction |
|---|---|---|---|
| [file:line] | [file:line] | [N] | [utility/hook/service/base class] |

**Summary:** [Description of duplication pattern and recommended consolidation strategy]

---

## Reusability Analysis

| Module / Component | Reusability | Reason | Recommendation |
|---|---|---|---|
| [Name] | High / Medium / Low | [Reason] | [Action] |

---

## SOLID Principles Compliance

| Principle | Status | Violations Found |
|---|---|---|
| Single Responsibility (SRP) | ✅ Pass / ❌ Fail | [Details] |
| Open/Closed (OCP) | ✅ Pass / ❌ Fail | [Details] |
| Liskov Substitution (LSP) | ✅ Pass / ❌ Fail | [Details] |
| Interface Segregation (ISP) | ✅ Pass / ❌ Fail | [Details] |
| Dependency Inversion (DIP) | ✅ Pass / ❌ Fail | [Details] |

---

## Design Patterns Assessment

**Patterns Applied Correctly:** [List]
**Patterns Misapplied:** [List with explanation]
**Anti-Patterns Found:** [List with explanation and recommendation]
**Recommended Patterns Not Used:** [List with rationale]

---

## Convention Compliance

### Frontend Conventions
- ✅ Component naming: [Pass/Fail]
- ✅ Type definitions: [Pass/Fail]
- ✅ File structure: [Pass/Fail]
- ✅ Naming conventions: [Pass/Fail]
- ✅ TypeScript strict compliance: [Pass/Fail]
- ⚠️ Issues found: [Count]

### Backend Conventions
- ✅ API design: [Pass/Fail]
- ✅ Error handling: [Pass/Fail]
- ✅ Input validation: [Pass/Fail]
- ✅ Security: [Pass/Fail]
- ⚠️ Issues found: [Count]

---

## Performance Analysis

**Frontend:**
- Bundle size impact: [+X KB]
- Render performance: [Good / Needs Optimization]
- Memory usage: [Good / Potential Leaks]
- Identified bottlenecks: [List]

**Backend:**
- Query efficiency: [Good / N+1 Detected / Missing Indexes]
- Algorithm complexity: [O(?) — acceptable / needs improvement]
- Response time impact: [Negligible / Moderate / Significant]
- Resource usage: [Optimized / Needs Improvement]

---

## Security Analysis (OWASP Top 10)

| OWASP Category | Status | Findings |
|---|---|---|
| A01 Broken Access Control | ✅ / ❌ | [Details] |
| A02 Cryptographic Failures | ✅ / ❌ | [Details] |
| A03 Injection | ✅ / ❌ | [Details] |
| A04 Insecure Design | ✅ / ❌ | [Details] |
| A05 Security Misconfiguration | ✅ / ❌ | [Details] |
| A06 Vulnerable Components | ✅ / ❌ | [Details] |
| A07 Auth Failures | ✅ / ❌ | [Details] |
| A08 Integrity Failures | ✅ / ❌ | [Details] |
| A09 Logging Failures | ✅ / ❌ | [Details] |
| A10 SSRF | ✅ / ❌ | [Details] |

**Security Score:** [X/10]
**Hardcoded Secrets:** [None / Found — locations]
**Vulnerable Dependencies:** [None / Found — package@version CVE-ID]

---

## Maintainability Analysis

**Code Complexity:**
- Average Cyclomatic Complexity: [N] ([Acceptable <10 / Needs Refactoring])
- Files Exceeding Length Limit: [Count] ([List])
- Deep Nesting Violations: [Count] ([List])
- Magic Numbers/Strings Found: [Count] ([List])

**Dead Code:**
- Unused imports: [Count] ([List])
- Unused functions/variables: [Count] ([List])
- TODO/FIXME/HACK comments: [Count] ([List with assessment])

**Maintainability Index:** [0-100]

---

## Test Coverage

**Current Coverage:** [X%]
**Changed Lines Coverage:** [X%]
**Missing Tests:**
- [File/Function that needs tests and why]

**Test Quality Issues:**
- [Tests with poor isolation, testing implementation instead of behavior, etc.]

---

## Code Quality Metrics Summary

```
Maintainability Index:     [0-100]
Cyclomatic Complexity:     [Average per function]
Code Duplication:          [X%]
Test Coverage:             [X%]
Security Score:            [0-10]
Performance Score:         [0-10]
Reusability Score:         [High / Medium / Low]
SOLID Compliance:          [X/5 principles met]
Convention Compliance:     [X%]
Technical Debt Estimate:   [X hours]
```

---

## Recommendations

### Immediate Actions (Before Merge)
1. [Action item — severity, file, specific fix]
2. [Action item — severity, file, specific fix]

### Follow-up Actions (Post-Merge)
1. [Action item for future improvement]
2. [Action item for future improvement]

### Technical Debt Backlog
- [Identified technical debt item — effort estimate]
- [Identified technical debt item — effort estimate]

---

## Positive Highlights ✨

- [Good practices observed]
- [Well-implemented patterns]
- [Improvements over previous code]
- [Reusability or design decisions done well]

---

## Next Steps

1. **If Critical Issues Found:**
   - Block merge — address all critical issues first
   - Re-run `/tdd-review` after fixes

2. **If High Priority Issues Found:**
   - Address all high priority issues before merge
   - Schedule medium priority items as follow-up

3. **If Only Low Priority/Suggestions:**
   - Code is ready to merge
   - Log suggestions as backlog items

**Estimated Fix Time:** [X hours/days]
```

---

### 5. Validate Against Project Patterns

Cross-reference with solution patterns from tdd-compare and tdd-scaffold:

**Check Pattern Consistency:**
- ML Pipeline: Proper MLflow tracking, model versioning
- Data Platform: Data quality checks, idempotent transformations
- Web Application: Frontend-backend integration, API contracts
- DevOps Pipeline: Proper CI/CD stages, deployment strategies

**Validate Integration Points:**
- API contracts match between frontend and backend
- Message schemas consistent across services
- Database migrations properly versioned
- Configuration management consistent

**Cross-Component DRY:**
- Shared types/schemas defined once (e.g., in a `shared/` package) and consumed everywhere
- No duplicated validation rules between frontend and backend — use shared schema libraries if possible

---

### 6. Generate Actionable Metrics

**Code Quality Metrics:**
```
Maintainability Index: [0-100]
Cyclomatic Complexity: [Average]
Code Duplication:      [X%]
Test Coverage:         [X%]
Security Score:        [0-10]
Performance Score:     [0-10]
Reusability Score:     [High / Medium / Low]
SOLID Compliance:      [X/5]
Convention Compliance: [X%]
Technical Debt:        [X hours estimate]
```

**Trend Analysis:**
- Compared to previous commits
- Improvement or regression per metric
- Technical debt growing or shrinking

---

### 7. Provide Fix Guidance

For each issue, provide:

1. **Why it's a problem** — principle violated, risk introduced
2. **How to fix it** — step-by-step instructions
3. **Code example** — before/after comparison
4. **Related documentation** — links to relevant standards, docs, or patterns
5. **Testing approach** — how to verify the fix is correct and doesn't regress

---

## Review Checklist

Before completing the review, verify every item below:

- [ ] All changed files analyzed
- [ ] Duplicate code scanned across all changed and related files
- [ ] Reusability assessed — shared abstractions recommended where applicable
- [ ] SOLID principles evaluated for all classes, modules, and functions
- [ ] Design patterns assessed — correct usage and anti-patterns flagged
- [ ] Security vulnerabilities checked (OWASP Top 10)
- [ ] Hardcoded secrets and sensitive data scanned
- [ ] Dependency vulnerabilities flagged (npm audit / pip audit)
- [ ] Performance implications assessed (N+1, complexity, bundle size)
- [ ] Maintainability checked (complexity, nesting, naming, dead code)
- [ ] Convention compliance validated against project standards
- [ ] Test coverage evaluated — missing and poor-quality tests flagged
- [ ] Documentation updates reviewed
- [ ] Breaking changes identified and documented
- [ ] Configuration changes validated
- [ ] Migration scripts reviewed (if applicable)
- [ ] Technical debt items identified and estimated

---

## Examples

**Example 1: Uncommitted Changes Review**
```
User: /tdd-review

AI: Analyzing uncommitted changes...

Files Changed: 5
- frontend/src/components/UserProfile.tsx (modified)
- frontend/src/types/UserType.ts (new)
- backend/src/api/v1/users.py (modified)
- backend/tests/test_users.py (modified)
- docs/API.md (modified)

# Code Review Report

**Critical Issues:** 1 🔴
**High Priority:** 2 🟠
**Medium Priority:** 3 🟡

## Critical Issues 🔴

### backend/src/api/v1/users.py - SQL Injection Vulnerability
**Line:** 45
**Principle Violated:** OWASP A03 — Injection

**Issue:**
Direct string interpolation in SQL query allows SQL injection.

**Code:**
```python
query = f"SELECT * FROM users WHERE email = '{email}'"
```

**Recommendation:**
Use parameterized queries with SQLAlchemy ORM or prepared statements.

**Suggested Fix:**
```python
query = session.query(User).filter(User.email == email)
```

## Duplicate Code Analysis

**Duplicate Code Found:** Yes
**Total Duplications:** 2
**Estimated Lines Affected:** 24

| Location A | Location B | Lines | Recommended Abstraction |
|---|---|---|---|
| users.py:30-42 | orders.py:18-30 | 12 | extract to `validate_pagination_params()` utility |
| UserProfile.tsx:55-67 | UserCard.tsx:33-45 | 12 | extract to `<UserAvatar />` shared component |

[Continue with all issues...]
```

**Example 2: Pull Request Review**
```
User: /tdd-review PR #456

AI: Reviewing Pull Request #456: "Add user authentication feature"

Files Changed: 12
Branch: feature/user-auth → main

# Code Review Report

**Overall Assessment:** Pass with Recommendations

**Critical Issues:** 0 🔴
**High Priority:** 1 🟠
**Medium Priority:** 5 🟡

## Positive Highlights ✨
- Excellent test coverage (92%)
- Proper JWT implementation with short expiry and refresh tokens
- Good error handling with custom exception hierarchy
- Well-documented API endpoints with OpenAPI schema

## SOLID Principles Compliance

| Principle | Status | Violations Found |
|---|---|---|
| SRP | ✅ Pass | Auth service properly separated from user management |
| OCP | ❌ Fail | AuthStrategy uses if-else chain — add new auth type requires modification |
| DIP | ❌ Fail | UserController directly instantiates DatabaseService — inject it |

## High Priority Issues 🟠

### frontend/src/utils/auth.ts - Token Storage
**Line:** 23
**Principle Violated:** OWASP A07 — Authentication Failures

**Issue:**
JWT token stored in localStorage is vulnerable to XSS attacks.

**Recommendation:**
Use httpOnly cookies for token storage to prevent JavaScript access.

[Continue with review...]
```

---

## Required Output Structure

Every response from this workflow MUST contain all sections below:

1. **Review Summary** — files reviewed, issue counts by severity, overall assessment
2. **Detailed Findings** — all issues with severity, category, principle violated, code snippets, and recommended fixes
3. **Duplicate Code Analysis** — duplications found, locations, recommended abstractions
4. **Reusability Analysis** — per-module reusability score with recommendations
5. **SOLID Principles Compliance** — pass/fail per principle with specific violations
6. **Design Patterns Assessment** — correct usage, misuse, anti-patterns, and missing patterns
7. **Convention Compliance Report** — frontend, backend, and infrastructure conventions
8. **Performance Analysis** — frontend and backend performance findings
9. **Security Analysis** — full OWASP Top 10 checklist with findings
10. **Maintainability Analysis** — complexity, dead code, technical debt
11. **Test Coverage Report** — coverage gaps and test quality issues
12. **Code Quality Metrics Summary** — all metrics in tabular form
13. **Actionable Recommendations** — immediate and follow-up with effort estimates
14. **Next Steps** — merge decision, re-review requirements, and fix time estimate

---

## Notes

- **This is a review-only workflow. Do not generate or modify code unless explicitly requested.**
- Review is based on conventions from `PROJECT_STRUCTURE_AND_CONVENTIONS.md` if available
- All findings must be specific, actionable, and include code examples with line numbers
- Severity ratings must be consistent and justified with principle or standard violated
- Duplicate code detection must scan across ALL changed files, not just individual files in isolation
- Reusability recommendations must include concrete abstraction names and locations
- SOLID and design pattern analysis applies to all languages (Python, TypeScript, Java, etc.)
- Security analysis must cover all OWASP Top 10 categories — not just the obvious ones
- Provide constructive feedback with positive highlights alongside issues
- For implementing fixes, direct users to `tdd-scaffold` or `tdd-refactor` workflows
- Review must be thorough AND pragmatic — prioritize issues by real-world impact
- Consider the project stage (prototype vs. production) when assessing severity of design issues
