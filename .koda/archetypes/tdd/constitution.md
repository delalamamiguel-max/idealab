# TDD (Test-Driven Development) Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the TDD archetype, which enforces strict Red-Green-Refactor discipline across all software development activities. Every piece of code must be driven by a failing test first, implemented with the minimal code to pass, then refactored for quality — ensuring high test coverage, clean design, and confidence in every change.

**Source**: Created for Test-Driven Development workflows spanning unit testing, integration testing, BDD, ATDD, contract testing, property-based testing, data pipeline TDD, and ML TDD.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code or design that violates these rules:

### TDD Cycle Integrity
- ✘ **No implementation without a failing test**: Do not write production code unless a failing test (Red phase) exists that demands it.
- ✘ **No skipping the Green phase**: Do not move to refactoring without first making all tests pass with minimal implementation.
- ✘ **No refactoring with failing tests**: Do not restructure or optimize code while any test is failing — all tests must be Green before refactoring begins.
- ✘ **No merging stages**: Do not combine the plan and implementation in a single response — always present the plan first, wait for confirmation, then implement.
- ✘ **No assumed confirmation**: Silence or a follow-up question is NOT confirmation — do not proceed to implementation until the user explicitly approves (e.g., "yes", "proceed", "go ahead").
- ✘ **No multi-component dumps**: Do not generate multiple components in one response unless the user explicitly says "do all" or "generate everything" — scaffold one component at a time by default.

### Test Quality
- ✘ **No implementation-coupled tests**: Do not write tests that test implementation details (private methods, internal state) — test observable behavior and public interfaces only.
- ✘ **No tests without assertions**: Do not create test functions that lack meaningful assertions — every test must assert expected outcomes.
- ✘ **No untested source files**: Do not scaffold or deliver any source file containing logic without a corresponding test file — if there are 5 source files, there must be 5 test files.
- ✘ **No hardcoded test data without context**: Do not use magic numbers or unexplained literals in tests — use named constants, fixtures, or factories with descriptive names.
- ✘ **No test interdependence**: Do not write tests that depend on execution order or shared mutable state — each test must be independently runnable.
- ✘ **No ignored/skipped tests without justification**: Do not leave `@skip`, `.skip()`, or `@pytest.mark.skip` annotations without a documented reason and a ticket/issue reference.
- ✘ **No empty catch blocks in tests**: Do not swallow exceptions in test code — let failures propagate for clear diagnostics.

### Security & Code Quality
- ✘ **No hardcoded secrets**: Do not include API keys, credentials, passwords, or tokens directly in code or test fixtures.
- ✘ **No eval or dynamic code execution**: Do not use `eval()`, `exec()`, `new Function()`, or similar on user-influenced data.
- ✘ **No missing input validation**: Do not accept user input without validation at system boundaries.
- ✘ **No SQL injection**: Do not construct queries with string concatenation — use parameterized queries or ORM methods.
- ✘ **No XSS vulnerabilities**: Do not render unsanitized user content in HTML.
- ✘ **No PII in logs or errors**: Do not log tokens, passwords, SSNs, credit card numbers, or expose stack traces in production error responses.
- ✘ **No deprecated cryptography**: Do not use MD5, SHA1, unsalted hashes, or custom cryptographic implementations.

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

### TDD Workflow Discipline
- ✔ **Red-Green-Refactor cycle**: Every feature follows Red (write failing test) → Green (minimal code to pass) → Refactor (improve design while keeping tests green).
- ✔ **Test files before implementation files**: In scaffolding plans and file generation order, test files are always listed and created before their corresponding implementation files.
- ✔ **Plan-then-implement**: Always present a structured plan (test strategy, component breakdown, TDD approach per component) and wait for user confirmation before generating any code.
- ✔ **Per-component checkpoints**: After generating each component's tests + implementation, stop and wait for user instruction before proceeding to the next component.
- ✔ **Behavioral test naming**: Test names must read as specifications describing behavior (e.g., `should return 401 when token is expired`, `calculates total with discount applied`).

### TDD Pattern Selection
- ✔ **Pattern-per-component mapping**: Each component in the plan must specify which TDD pattern applies — Classic Inside-Out, Outside-In (London), BDD, ATDD, Contract-First, Property-Based, Data Pipeline TDD, or ML TDD.
- ✔ **Classic Inside-Out TDD**: Use for pure logic, utilities, algorithms, data transformations — test smallest units first, build outward.
- ✔ **Outside-In TDD (London/Mockist)**: Use for API endpoints, controllers, service layers — start from the outermost interface and mock dependencies inward.
- ✔ **BDD (Behavior-Driven Development)**: Use when requirements are expressed as user stories with Given-When-Then scenarios — Gherkin syntax with Cucumber/behave.
- ✔ **ATDD (Acceptance Test-Driven Development)**: Use when business stakeholders define acceptance criteria upfront — FitNesse, Robot Framework, or structured acceptance tests.
- ✔ **Contract-First TDD**: Use for API boundaries and microservice interfaces — Pact or similar consumer-driven contract testing.
- ✔ **Property-Based Testing**: Use for mathematical functions, parsers, serializers, and invariants — Hypothesis (Python), fast-check (JS/TS), QuickCheck.
- ✔ **Data Pipeline TDD**: Use for ETL, data quality, schema validation — test data contracts, transformations, and output schemas before building pipelines.
- ✔ **ML TDD**: Use for model training, evaluation, feature engineering — test data preprocessing, model input/output shapes, metric thresholds, and reproducibility.

### Test Architecture
- ✔ **Test pyramid adherence**: Maintain a healthy ratio — many unit tests, fewer integration tests, minimal E2E tests.
- ✔ **Test co-location**: Place test files in a `tests/` directory mirroring `src/` structure, or in `__tests__/` adjacent to source files.
- ✔ **Minimum test cases per file**: At least one happy-path test and one error/edge-case test per source file.
- ✔ **Coverage targets**: Aim for 80%+ line coverage, 70%+ branch coverage — document coverage thresholds in the test plan.
- ✔ **Test isolation**: Each test creates its own state, mocks, and fixtures — no shared mutable state between tests.
- ✔ **Deterministic tests**: Tests must produce the same result on every run — no reliance on wall-clock time, random data without seeds, or external services without mocks.

### Test Documentation
- ✔ **Run instructions per component**: Every component must include a "How to Run Unit Tests" section with exact commands for: install dependencies, run all tests, run single test file, run with coverage.
- ✔ **Test strategy documentation**: The plan must document the chosen TDD approach, test scope matrix, coverage targets, and testing frameworks for each component.
- ✔ **Conventions file**: When generating project structure documentation, output to `PROJECT_STRUCTURE_AND_CONVENTIONS.md` — never use any other filename for this purpose.

### Existing Project vs. Greenfield
- ✔ **Detect before acting**: Always determine whether the workspace is an existing project (has source code, package.json, etc.) or greenfield before scaffolding.
- ✔ **Respect existing structure**: For existing projects, scaffold into the current directory layout — do not create new top-level `frontend/` or `backend/` folders.
- ✔ **Follow existing conventions**: If `PROJECT_STRUCTURE_AND_CONVENTIONS.md` exists, follow it strictly — do not impose different patterns.
- ✔ **Greenfield defaults**: For new projects, use the default technology stack (React 18+ / Vite / TypeScript for frontend, Fastify 5+ / TypeScript / MongoDB for backend, Vitest for testing) unless the user specifies otherwise.

### HTTP Service (Frontend Projects)
- ✔ **Single httpService gateway**: All frontend HTTP calls must go through a custom `httpService` utility wrapping native `fetch` — no Axios, ky, got, or other HTTP libraries.
- ✔ **Environment-driven base URL**: Use `VITE_API_BASE_URL` environment variable — no hardcoded URLs, no Vite dev-server proxy.

### Cross-Workflow References
- ✔ **Workflow routing**: Direct users to the appropriate TDD workflow when their request doesn't match the current one — scaffold for new code, debug for test failures, refactor for improvement, compare for approach evaluation, review for code quality assessment.
- ✔ **Review integration**: The `review.md` supporting file provides comprehensive code review checklists (DRY, SOLID, reusability, security, performance, TDD compliance) — reference it during refactoring and documentation workflows.

## III. Scope

This constitution applies to:
- All TDD workflow executions (scaffold, debug, test, refactor, document, compare)
- Code review assessments (via review supporting file)
- Any code generation where test-first discipline is requested
- Projects in any language/framework (Python, TypeScript/JavaScript, Java, Go, etc.)

## IV. Out of Scope

This constitution does not cover:
- AT&T brand compliance (see `app-maker` archetype)
- Infrastructure provisioning (see `aks-devops-deployment`, `terraform-cicd-architect`)
- ML model architecture decisions (see `model-architect`, `model-specialist`)
- Security-specific auditing (see `security-guardian`, `python-security-vulnerability`)
