# App Maker Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the App Maker archetype, which generates production-ready web applications adhering to AT&T brand guidelines.

**Source**: Created for web application development with React/FastAPI stack and AT&T brand compliance

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code or design that violates these rules:

- ✘ **No hardcoded secrets**: Do not include API keys, credentials, or secrets directly in code
- ✘ **AT&T Blue dominance**: Do not create designs where AT&T Blue (#009FDB) is not the dominant color
- ✘ **No non-ATT fonts**: Do not use fonts other than ATT Aleck family (exception: system fallbacks only)
- ✘ **No public licenses**: Do not use public licenses, always use AT&T Proprietary
- ✘ **No missing input validation**: Do not accept user input without validation (frontend and backend)
- ✘ **No accessibility violations**: Do not omit ARIA labels, keyboard navigation, or semantic HTML
- ✘ **Color contrast required**: Do not use color combinations with contrast ratio <4.5:1 for text
- ✘ **HTTPS enforcement**: Do not deploy without HTTPS in production
- ✘ **No XSS vulnerabilities**: Do not use dangerouslySetInnerHTML with unsanitized user content
- ✘ **Authentication required**: Do not expose protected routes/APIs without authentication when Entra ID enabled
- ✘ **No SQL injection**: Do not construct SQL queries with string concatenation
- ✘ **No incompatible dependency versions**: Do not specify Python package versions without verifying compatibility (especially Pydantic + SQLAlchemy combinations)
- ✘ **No plaintext or weak password storage**: Never store user passwords or secrets without strong hashing (Argon2id or bcrypt with cost factor) and per-user salts.
- ✘ **No logging of secrets or PII**: Do not log tokens, passwords, SSNs, credit card numbers, emails, phone numbers, or access keys.
- ✘ **No use of eval/new Function/dynamic code execution**: Prohibit `eval`, `Function`, or Python `exec` on user-influenced data.
- ✘ **No deprecated/weak cryptography**: Disallow MD5, SHA1, unsalted hashes, or custom crypto; use approved algorithms (AES-256-GCM, SHA-256/SHA-3 for hashing, TLS 1.2+).
- ✘ **No unsanitized file uploads**: Disallow accepting files without size/type validation.
- ✘ **No absence of request size limits**: Enforce max body size & rate limits to mitigate resource exhaustion.
- ✘ **No PII exposure in errors**: Errors must not leak user data, stack traces, or internal paths in production.
- ✘ **No unbounded pagination/queries**: Always enforce server-side limits and pagination; refuse requests without bounds.
- ✘ **No silent error swallowing**: Disallow catching exceptions without logging structured diagnostics.
- ✘ **No ambiguous ORM joins**: Do not use `.join()` or `.outerjoin()` without explicit ON conditions in SQLAlchemy queries
- ✘ **No undefined relationship overlaps**: Do not define multiple relationships on same foreign key without declaring `overlaps` parameter
- ✘ **No missing PostCSS config**: Do not create TailwindCSS projects without `postcss.config.js` (styles will not load)

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

### Brand Compliance
- ✔ **ATT Aleck font**: Load and use ATT Aleck Sans as primary font with proper fallbacks
- ✔ **AT&T color palette**: Use AT&T Blue, White, Cobalt, Lime, Mint as defined in ATT_COLORS.md
- ✔ **Cobalt CTAs**: Use Cobalt for call-to-action buttons
- ✔ **Color proportion**: Ensure AT&T Blue occupies 80%+ when combining with non-brand colors
- ✔ **Typography hierarchy**: AT&T Blue or black for headlines, appropriate contrast for body text

### Frontend Architecture
- ✔ **TypeScript strict mode**: Enable strict mode in tsconfig.json
- ✔ **Component structure**: Organize as components/ui, components/features, components/layouts
- ✔ **Form validation**: Use React Hook Form + Zod for all forms
- ✔ **State management**: Use React Query for server state, Context/Zustand for client state
- ✔ **Error boundaries**: Wrap app in error boundary components
- ✔ **Loading states**: Show loading indicators for async operations
- ✔ **PostCSS configuration**: Always create `postcss.config.js` when using TailwindCSS (required for style processing)

### Backend Architecture (FastAPI)
- ✔ **Input validation**: Use Pydantic models for request/response validation
- ✔ **CORS configuration**: Configure CORS with specific allowed origins
- ✔ **Error handling**: Use FastAPI exception handlers with proper status codes
- ✔ **API versioning**: Version APIs (/api/v1/)
- ✔ **Rate limiting**: Implement rate limiting for public endpoints
- ✔ **Health & readiness endpoints**: Provide `/healthz` (quick) and `/readyz` (dependencies check) endpoints.
- ✔ **Structured JSON logging**: Use correlation/trace IDs for each request; no plain print logs.
- ✔ **OpenTelemetry tracing**: Instrument inbound requests, DB calls, and external HTTP clients.
- ✔ **Centralized config management**: Load typed settings from environment with Pydantic BaseSettings layer; forbid scattered `os.getenv` calls.
- ✔ **Dependency Injection pattern**: Use FastAPI dependency injection for services (db sessions, cache clients) instead of global singletons.
- ✔ **Standard error envelope**: Return structured errors `{error:{code,message,details,trace_id}}`.
- ✔ **Connection pooling**: Use async DB drivers with configured pool sizes and timeouts.
- ✔ **Explicit join conditions**: Always specify ON clause in SQLAlchemy joins: `.outerjoin(Model, Model.fk == OtherModel.pk)`
- ✔ **Relationship declarations**: Add `overlaps="relationship_name"` when multiple relationships reference same foreign key
- ✔ **Foreign key specification**: Use `foreign_keys=[column]` parameter for self-referential or ambiguous relationships
- ✔ **Date serialization**: Convert date/datetime objects to ISO strings with `.isoformat()` for JSON responses
- ✔ **Module-level imports**: Place all imports at top of file; avoid imports inside functions
- ✔ **Analytics fallback logic**: Time-range queries should fall back to most recent available data if no results in range

### Python Dependency Management
- ✔ **Version pinning**: Pin all production dependencies to specific versions in requirements.txt
- ✔ **Compatibility verification**: Use tested version combinations for interconnected libraries
- ✔ **Dependency comments**: Document version choices and compatibility notes in requirements.txt
- ✔ **Reserved keyword avoidance**: Prefix database columns to avoid ORM conflicts (e.g., `workflow_metadata` not `metadata`)
- ✔ **Compatible combinations**: Follow tested dependency matrices:
  - **FastAPI 0.104.x + Pydantic 2.9.2 + SQLAlchemy 2.0.35** (Recommended - Production Ready)
  - **FastAPI 0.104.x + Pydantic 2.5.x + SQLAlchemy 2.0.23+** (Stable Legacy)
  - **Avoid: Pydantic 2.11+ with SQLAlchemy < 2.0.35** (Incompatible)
- ✔ **Lock file usage**: Generate a deterministic lock (e.g., `requirements.lock` via pip-tools) for reproducible builds.
- ✔ **Segregated dev/test dependencies**: Maintain `requirements-dev.txt` for non-production tooling.
- ✔ **Minimal base image footprint**: Optimize container builds by excluding dev extras.

### SQLAlchemy Reserved Attributes (Never use as column names)
- ✔ **Avoid these identifiers**: `metadata`, `query`, `mapper`, `session`, `bind`, `__tablename__`, `__table__`, `__mapper__`, `_sa_instance_state`
- ✔ **Use prefixed alternatives**: `entity_metadata`, `workflow_metadata`, `search_query`, `user_session`, `db_mapper`
- ✔ **Cross-platform SQL keywords**: Avoid `user`, `table`, `column`, `index`, `key`, `value`, `order`, `group`, `timestamp` without qualification

### Security
- ✔ **Environment variables**: Store secrets in .env files (gitignored)
- ✔ **Input sanitization**: Sanitize all user inputs on backend
- ✔ **CSRF protection**: Implement CSRF tokens for mutations
- ✔ **Content Security Policy**: Set appropriate CSP headers
- ✔ **Secure headers**: Set X-Content-Type-Options, X-Frame-Options headers
- ✔ **PII data classification**: Tag and restrict handling/logging of personally identifiable information; mask at boundaries.
- ✔ **Secret rotation & vault integration**: Fetch secrets from a vault (e.g., Azure Key Vault) rather than long-lived .env values.
- ✔ **JWT/OAuth token validation**: Validate issuer, audience, expiration; use short token TTLs & refresh flow.
- ✔ **Input size & rate limits**: Enforce max payload sizes and per-IP thresholds beyond generic rate limiting.
- ✔ **Audit logging**: Record create/update/delete & auth events with actor, timestamp, and trace ID.
- ✔ **File upload sanitization**: Enforce MIME/type whitelist, max size.

### Testing
- ✔ **Unit tests**: Write unit tests for business logic functions
- ✔ **Component tests**: Test React components with React Testing Library
- ✔ **API tests**: Test FastAPI endpoints with pytest
- ✔ **E2E tests**: Create critical path E2E tests with Playwright
- ✔ **Performance smoke tests**: Basic latency & throughput checks for key endpoints (e.g., p95 < target).

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

### Code Quality
- ➜ **ESLint + Prettier**: Configure linting and formatting
- ➜ **Pre-commit hooks**: Use Husky + lint-staged
- ➜ **TypeScript strict**: No `any` types, prefer `unknown` with type guards
- ➜ **Function size**: Keep functions under 50 lines

### UI/UX
- ➜ **Mobile-first**: Design for mobile, enhance for desktop
- ➜ **Touch targets**: Minimum 44x44px for interactive elements
- ➜ **Loading skeletons**: Use skeleton screens instead of spinners
- ➜ **Toast notifications**: Use toast library for user feedback

### Performance
- ➜ **Code splitting**: Use dynamic imports for heavy components
- ➜ **Image optimization**: Use optimized image formats
- ➜ **Lazy loading**: Lazy load below-the-fold content
- ➜ **Bundle size**: Keep initial bundle <200KB gzipped
- ➜ **Lighthouse score**: Target >90 for all metrics
- ➜ **Database query optimization**: Monitor slow queries (>200ms) and add indices or refactors.
- ➜ **Connection pooling & circuit breakers**: Apply timeouts and fallback logic for external services.

### API Design

- ➜ **RESTful conventions**: Use standard HTTP methods and status codes
- ➜ **Pagination**: Paginate list endpoints
- ➜ **API documentation**: Generate OpenAPI/Swagger docs
- ➜ **Consistent error schema**: Standardized fields: `code`, `message`, `trace_id`, `details`.
- ➜ **Rate limiting headers**: Expose remaining quota via `X-RateLimit-*` headers.

### Developer Experience
- ➜ **Onboarding docs**: Quick-start guide with common commands & architecture overview.

**Version**: 1.0.1
**Last Updated**: 2025-10-24
**Source**: `/Users/md464h/projects/aifc_projects/eaifc_windsurf/app-maker/instructions.md`
