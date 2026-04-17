---
description: Compare frontend-only approaches (framework, routing, state, styling, testing) and recommend a fit (Frontend Only)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype frontend_only` and parse for ENV_VALID.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Read `${ARCHETYPES_BASEDIR}/frontend-only/templates/env-config.yaml` for standards and requirements.

### 3. Parse Input
Extract from $ARGUMENTS: approaches to compare (Approach A vs Approach B), comparison dimensions (performance, DX, accessibility, bundle size, learning curve), context (team expertise, project requirements, timeline). Request clarification if incomplete.

### 4. Identify Comparison Type

Determine what is being compared:

**Framework Comparisons**:
- Vite SPA vs Next.js vs Remix
- React vs Vue vs Svelte
- Create React App vs Vite

**State Management Comparisons**:
- React Query vs SWR
- Redux vs Zustand vs Jotai
- Context API vs External State Library

**Styling Comparisons**:
- TailwindCSS vs CSS Modules vs Styled Components
- Radix UI vs Headless UI vs shadcn/ui
- CSS-in-JS vs Utility-first CSS

**Testing Comparisons**:
- Vitest vs Jest
- Playwright vs Cypress
- React Testing Library vs Enzyme

**Build Tool Comparisons**:
- Vite vs Webpack vs Turbopack
- pnpm vs npm vs yarn

### 5. Define Evaluation Criteria

Establish dimensions for comparison:

**Technical Criteria**:
- Performance (bundle size, load time, runtime)
- Developer Experience (setup, debugging, hot reload)
- Type Safety (TypeScript support)
- Accessibility (built-in a11y features)
- Testing (ease of testing, tooling)

**Project Fit Criteria**:
- Learning curve for team
- Community and ecosystem
- Documentation quality
- Long-term maintenance
- Migration complexity

**AT&T-Specific Criteria**:
- TailwindCSS compatibility
- AT&T color palette support
- WCAG 2.1 AA compliance support
- Existing team expertise
- Internal tooling compatibility

### 6. Analyze Approach A

**Example: Vite + React SPA**

**Pros**:
- Fast development server (ESM-based)
- Simple setup and configuration
- Excellent TypeScript support
- Small bundle size
- Great for internal tools and dashboards

**Cons**:
- No SSR (SEO limitations)
- Client-side routing only
- No built-in data fetching patterns
- Manual code splitting setup

**Performance**:
- Dev server start: <500ms
- HMR: <50ms
- Production bundle: ~150KB (React + Router)
- Initial load: Fast (no server rendering)

**DX Score**: 9/10
**Accessibility**: Manual implementation required
**Learning Curve**: Low

**Best For**:
- Internal tools
- Dashboards
- Single-page applications
- Prototypes and POCs

### 7. Analyze Approach B

**Example: Next.js**

**Pros**:
- SSR/SSG for SEO
- File-based routing
- Built-in API routes
- Image optimization
- Excellent documentation

**Cons**:
- More complex setup
- Larger bundle size
- Hydration complexity
- Overkill for simple apps

**Performance**:
- Dev server start: 1-3s
- HMR: 100-500ms
- Production bundle: ~200KB+ (framework overhead)
- Initial load: Depends on SSR strategy

**DX Score**: 8/10
**Accessibility**: Good built-in support
**Learning Curve**: Medium

**Best For**:
- Public-facing websites
- SEO-critical applications
- Marketing sites
- Content-heavy applications

### 8. Create Comparison Matrix

```
📊 Comparison: Vite SPA vs Next.js

┌─────────────────────────┬──────────────────────┬──────────────────────┐
│ Criteria                │ Vite SPA             │ Next.js              │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ Setup Complexity        │ Simple ✓             │ Medium               │
│ Dev Server Speed        │ Excellent ✓          │ Good                 │
│ Bundle Size             │ Smaller ✓            │ Larger               │
│ SSR/SEO                 │ No                   │ Yes ✓                │
│ File-based Routing      │ Manual               │ Built-in ✓           │
│ TypeScript              │ Excellent ✓          │ Excellent ✓          │
│ TailwindCSS             │ Easy ✓               │ Easy ✓               │
│ Learning Curve          │ Low ✓                │ Medium               │
│ Community               │ Growing              │ Large ✓              │
│ AT&T Colors Support     │ Yes ✓                │ Yes ✓                │
│ WCAG Compliance         │ Manual               │ Better tooling ✓     │
│ Internal Tools          │ Excellent ✓          │ Good                 │
│ Public Websites         │ Limited              │ Excellent ✓          │
└─────────────────────────┴──────────────────────┴──────────────────────┘

✓ = Better option for this criteria
```

### 9. State Management Comparison

```
📊 Comparison: React Query vs Redux vs Zustand

┌─────────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┐
│ Criteria                │ React Query          │ Redux Toolkit        │ Zustand              │
├─────────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┤
│ Server State            │ Excellent ✓          │ Manual               │ Manual               │
│ Client State            │ Limited              │ Excellent ✓          │ Excellent ✓          │
│ Bundle Size             │ ~13KB                │ ~30KB                │ ~3KB ✓               │
│ Boilerplate             │ Minimal ✓            │ Medium               │ Minimal ✓            │
│ DevTools                │ Excellent ✓          │ Excellent ✓          │ Good                 │
│ Learning Curve          │ Low ✓                │ Medium               │ Low ✓                │
│ Caching                 │ Built-in ✓           │ Manual               │ Manual               │
│ TypeScript              │ Excellent ✓          │ Excellent ✓          │ Excellent ✓          │
└─────────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┘

Recommendation:
- Server state (API data): React Query
- Simple client state: Zustand or Context
- Complex client state: Redux Toolkit
```

### 10. Testing Framework Comparison

```
📊 Comparison: Vitest vs Jest

┌─────────────────────────┬──────────────────────┬──────────────────────┐
│ Criteria                │ Vitest               │ Jest                 │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ Speed                   │ Faster ✓             │ Slower               │
│ Vite Integration        │ Native ✓             │ Requires config      │
│ ESM Support             │ Native ✓             │ Experimental         │
│ Watch Mode              │ Excellent ✓          │ Good                 │
│ Snapshot Testing        │ Yes ✓                │ Yes ✓                │
│ Coverage                │ v8/istanbul ✓        │ istanbul ✓           │
│ Community               │ Growing              │ Mature ✓             │
│ Documentation           │ Good                 │ Excellent ✓          │
│ React Testing Library   │ Compatible ✓         │ Compatible ✓         │
└─────────────────────────┴──────────────────────┴──────────────────────┘

Recommendation: Vitest for Vite projects, Jest for existing projects
```

### 11. Provide Recommendations

**Recommendation Based on Context**:

**Choose Vite SPA if**:
- Building internal tools or dashboards
- SEO is not required
- Team prefers simplicity
- Fast development iteration needed
- Prototype or POC

**Choose Next.js if**:
- SEO is important
- Public-facing website
- Need SSR/SSG
- Complex routing requirements
- Image optimization needed

**Recommended Stack for Frontend-Only**:
```
Framework: Vite + React
Styling: TailwindCSS (with AT&T colors)
State: React Query (server) + Zustand (client)
Forms: React Hook Form + Zod
Testing: Vitest + React Testing Library
E2E: Playwright
UI Library: Radix UI or Headless UI
```

### 12. Generate Comparison Report

```
📋 Comparison Report: <Approach A> vs <Approach B>

🎯 Context:
   Project Type: <type>
   SEO Required: <yes/no>
   Team Expertise: <React/Vue/etc>
   Timeline: <timeline>
   Accessibility: WCAG 2.1 AA required

📊 Summary:
   Winner: <Approach> (by <X> criteria)
   
   Approach A Wins: <count> criteria
   Approach B Wins: <count> criteria
   Tie: <count> criteria

🏆 Recommended Approach: <Approach>

Rationale:
<Detailed explanation considering project requirements,
team expertise, timeline, and AT&T compliance>

⚠️ Considerations:
- <Migration consideration>
- <Learning curve consideration>
- <Long-term maintenance consideration>

📦 Recommended Stack:
   Framework: <choice>
   Styling: TailwindCSS (AT&T colors configured)
   State: <choice>
   Testing: <choice>
   UI Library: <choice>

⏱️ Setup Time Estimate:
   Approach A: <X> hours
   Approach B: <Y> hours

🔧 Migration Complexity:
   From current: <low/medium/high>
   Risk level: <low/medium/high>

✅ Next Steps:
   1. <First concrete action>
   2. <Second concrete action>
   3. <Third concrete action>
```

## Error Handling

**Insufficient Context**: Request details about project type, team expertise, timeline.

**Incomparable Approaches**: Explain why comparison is invalid (e.g., comparing framework to library).

**No Clear Winner**: Provide hybrid approach or context-dependent recommendation.

## Common Comparisons

**Comparison 1: Vite vs Next.js**
- Vite: Simple, fast, great for SPAs and internal tools
- Next.js: SSR/SSG, SEO, better for public websites

**Comparison 2: TailwindCSS vs CSS Modules**
- TailwindCSS: Utility-first, rapid development, AT&T colors easy
- CSS Modules: Scoped styles, traditional CSS, more verbose

**Comparison 3: React Query vs Redux**
- React Query: Server state, caching, minimal boilerplate
- Redux: Complex client state, time-travel debugging

**Comparison 4: Vitest vs Jest**
- Vitest: Vite-native, faster, ESM support
- Jest: Mature, extensive ecosystem, better docs

## Examples

**Example 1**: `/compare-frontend Compare Vite SPA vs Next.js for internal dashboard`

**Example 2**: `/compare-frontend Compare React Query vs Zustand for state management`

**Example 3**: `/compare-frontend Compare TailwindCSS vs CSS Modules for styling`

**Example 4**: `/compare-frontend Compare Vitest vs Jest for testing React components`

## References

Constitution: (pre-loaded above)
Environment Config: `${ARCHETYPES_BASEDIR}/frontend-only/templates/env-config.yaml`
