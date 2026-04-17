---
description: Compare web application approaches, architectures, and implementation patterns (App Maker)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype app-maker --json ` and parse for ENV_VALID.

### 2. Load Configuration
- The constitution rules are already loaded in context above.

### 3. Parse Input
Extract from $ARGUMENTS: approaches to compare (Approach A vs Approach B), comparison dimensions (performance, maintainability, security, scalability, cost), context (team size, timeline, requirements). Request clarification if incomplete.

### 4. Identify Comparison Type

Determine what is being compared:

**Architecture Comparisons**:
- SPA vs SSR vs SSG
- Monolith vs Microservices
- REST vs GraphQL
- Client-side vs Server-side rendering

**Technology Stack Comparisons**:
- React vs Vue vs Angular
- FastAPI vs Express vs Django
- PostgreSQL vs MongoDB
- Vite vs Next.js vs CRA

**Implementation Pattern Comparisons**:
- State management (Context vs Redux vs Zustand)
- Form handling approaches
- Authentication strategies
- Data fetching patterns

**Deployment Comparisons**:
- Vercel vs Netlify vs AWS
- Containerized vs Serverless
- Monorepo vs Polyrepo

### 5. Define Evaluation Criteria

Establish dimensions for comparison:

**Technical Criteria**:
- Performance (bundle size, load time, runtime)
- Scalability (concurrent users, data volume)
- Security (attack surface, auth mechanisms)
- Maintainability (code complexity, testability)
- Developer Experience (DX, learning curve)

**Business Criteria**:
- Development time/cost
- Hosting costs
- Team expertise requirements
- Long-term support/community

**AT&T-Specific Criteria**:
- Brand guideline compliance
- Enterprise integration (Entra ID)
- Telemetry integration (App Insights)
- Security standards alignment

### 6. Analyze Approach A

Evaluate first approach across all criteria:

**Example: SPA with React + Vite**

**Pros**:
- Fast development with Vite HMR
- Simple deployment (static hosting)
- Rich ecosystem and component libraries
- Easy AT&T brand integration with TailwindCSS
- Client-side routing flexibility

**Cons**:
- SEO challenges (requires prerendering)
- Initial bundle size can be large
- Client-side data fetching delays
- Security concerns (API keys exposure risk)

**Performance**:
- Initial load: 1.5-2s (depends on bundle size)
- Subsequent navigation: <100ms (client-side routing)
- Bundle size: 150-250KB gzipped (with code splitting)

**Use Cases**:
- Internal dashboards and tools
- Applications behind authentication
- Interactive data visualization apps
- Admin panels

### 7. Analyze Approach B

Evaluate second approach across same criteria:

**Example: SSR with Next.js**

**Pros**:
- Better SEO (server-rendered HTML)
- Faster initial page load (streamed HTML)
- API routes included (no separate backend needed)
- Optimized images and fonts automatically
- Incremental Static Regeneration (ISR)

**Cons**:
- More complex deployment (needs Node.js server)
- Higher hosting costs (compute vs static)
- Steeper learning curve (SSR concepts)
- More complex state management

**Performance**:
- Initial load: 0.8-1.2s (server-rendered)
- Time to Interactive: 1.5-2s
- Subsequent navigation: <100ms
- Bundle size: Similar to SPA (code splitting)

**Use Cases**:
- Public-facing marketing sites
- E-commerce applications
- Content-heavy applications
- SEO-critical pages

### 8. Create Comparison Matrix

Generate side-by-side comparison:

```
📊 Comparison: SPA (React + Vite) vs SSR (Next.js)

┌─────────────────────────┬──────────────────────┬──────────────────────┐
│ Criteria                │ Approach A (SPA)     │ Approach B (SSR)     │
├─────────────────────────┼──────────────────────┼──────────────────────┤
│ Initial Load Time       │ 1.5-2s              │ 0.8-1.2s ✓          │
│ SEO                     │ Poor (needs work)    │ Excellent ✓         │
│ Development Speed       │ Fast ✓              │ Moderate            │
│ Deployment Complexity   │ Simple ✓            │ Moderate            │
│ Hosting Cost            │ Low ✓               │ Higher              │
│ AT&T Brand Integration  │ Easy ✓              │ Easy ✓              │
│ Scalability             │ High ✓              │ High ✓              │
│ Security                │ Moderate             │ Better ✓            │
│ Developer Experience    │ Excellent ✓         │ Good                │
│ Learning Curve          │ Gentle ✓            │ Steep               │
└─────────────────────────┴──────────────────────┴──────────────────────┘

✓ = Better option for this criteria
```

### 9. Provide Code Examples

Show implementation differences:

**Approach A: SPA Data Fetching**
```typescript
// Client-side data fetching with React Query
function UserList() {
  const { data, isLoading } = useQuery({
    queryKey: ['users'],
    queryFn: () => apiClient.get('/users'),
  });

  if (isLoading) return <Skeleton />;
  return <UserTable users={data} />;
}
```

**Approach B: SSR Data Fetching**
```typescript
// Server-side data fetching with Next.js
export async function getServerSideProps() {
  const users = await prisma.user.findMany();
  return { props: { users } };
}

function UserList({ users }) {
  return <UserTable users={users} />;
}
```

### 10. Analyze Trade-offs

Identify key trade-offs:

**Performance vs Complexity**:
- SPA: Simpler but slower initial load
- SSR: Faster initial load but more complex setup

**Cost vs Features**:
- Static hosting (SPA): Cheap but limited SEO
- Server hosting (SSR): More expensive but better SEO

**Developer Experience vs Production Optimization**:
- Vite (SPA): Fast dev but manual optimization
- Next.js (SSR): Slower dev but auto-optimized

### 11. Provide Recommendations

**Recommendation Based on Context**:

**Choose Approach A (SPA) if**:
- Building internal tools or dashboards
- SEO is not important (behind auth)
- Want simplest deployment
- Team is familiar with React
- Budget is constrained
- Need fastest development time

**Choose Approach B (SSR) if**:
- Public-facing application
- SEO is critical
- Performance is top priority
- Can handle deployment complexity
- Want built-in API routes
- Need optimal Core Web Vitals

**Hybrid Approach**:
Consider Next.js with static generation (SSG) for best of both:
- Pre-render public pages at build time (SEO + speed)
- Use client-side routing for dynamic features
- Add server components for data-heavy pages

### 12. Generate Comparison Report

```
📋 Comparison Report: <Approach A> vs <Approach B>

🎯 Context:
   Project Type: <type>
   Team Size: <size>
   Timeline: <timeline>
   Requirements: <requirements>

📊 Summary:
   Winner: <Approach> (by <X> criteria)
   
   Approach A Wins: <count> criteria
   Approach B Wins: <count> criteria
   Tie: <count> criteria

🏆 Recommended Approach: <Approach>

Rationale:
<Detailed explanation of why this approach is recommended
for the given context, requirements, and constraints>

⚠️ Considerations:
- <Important consideration 1>
- <Important consideration 2>
- <Important consideration 3>

💰 Cost Analysis:
   Approach A: $<X>/month (hosting + compute)
   Approach B: $<Y>/month (hosting + compute)

⏱️ Development Time Estimate:
   Approach A: <X> weeks
   Approach B: <Y> weeks

📚 Learning Resources:
   Approach A: <links>
   Approach B: <links>

✅ Next Steps:
   1. <Action based on recommendation>
   2. <Follow-up action>
   3. <Validation step>
```

## Error Handling

**Insufficient Context**: Request more details about requirements, constraints, team expertise.

**Incomparable Approaches**: Explain why comparison is not valid (e.g., comparing frontend to backend).

**No Clear Winner**: Provide hybrid approach or suggest additional evaluation needed.

## Common Comparisons

**Comparison 1: React vs Vue**
- Use React: Larger ecosystem, better AT&T enterprise support, TypeScript-first
- Use Vue: Simpler learning curve, better documentation, smaller bundle

**Comparison 2: REST vs GraphQL**
- Use REST: Simpler, better caching, more tooling, easier to secure
- Use GraphQL: Flexible queries, less over-fetching, better for mobile

**Comparison 3: Client-side vs Server-side Auth**
- Client-side: Simpler, works with static hosting, better for SPAs
- Server-side: More secure, better for SSR, protects sensitive operations

**Comparison 4: Monolith vs Microservices**
- Monolith: Faster to develop, simpler deployment, easier debugging
- Microservices: Better scalability, independent deployments, team autonomy

## Examples

**Example 1**: `/compare-app Compare React SPA vs Next.js SSR for customer portal`
Output: Detailed comparison with recommendation based on SEO, auth, performance needs

**Example 2**: `/compare-app Compare PostgreSQL vs MongoDB for user data storage`
Output: Analysis of data model, queries, scalability, transactions

**Example 3**: `/compare-app Compare Vercel vs AWS deployment for our application`
Output: Cost analysis, DX comparison, scalability considerations

**Example 4**: `/compare-app Compare Context API vs Zustand for state management`
Output: Performance, DX, bundle size, complexity comparison

## References

Constitution: (pre-loaded above)
