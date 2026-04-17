---
description: Compare two archetype design approaches (Archetype Architect)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Parse Comparison Request

Extract from $ARGUMENTS:
- Archetype options to compare (2-3)
- Comparison criteria
- Use case context

### 2. Define Comparison Dimensions

Compare across:
- **Scope**: What problems each solves
- **Complexity**: Implementation difficulty
- **Discovery**: Keyword overlap and conflicts
- **Maintenance**: Long-term update burden
- **Reusability**: How well patterns transfer
- **Category Fit**: Alignment with category purpose

### 3. Analyze Each Option

For each archetype option:
- List technologies covered
- List use cases
- Identify unique patterns
- Identify overlaps with existing archetypes
- Estimate implementation time

### 4. Generate Comparison Matrix

```
| Dimension | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Scope | ... | ... | ... |
| Complexity | ... | ... | ... |
| Discovery | ... | ... | ... |
| Maintenance | ... | ... | ... |
| Reusability | ... | ... | ... |
| Category Fit | ... | ... | ... |
```

### 5. Recommend Approach

Based on:
- Use case frequency
- Overlap with existing archetypes
- Implementation effort
- Long-term value

### 6. Provide Decision Guidance

```
RECOMMENDATION: {Option}

Rationale:
- {reason_1}
- {reason_2}
- {reason_3}

Trade-offs:
- Pros: {list}
- Cons: {list}

Alternative: If {condition}, consider {alternative}
```

## Comparison Patterns

### Pattern 1: Broad vs Narrow Scope

**Broad Archetype:**
- Covers multiple related technologies
- More complex constitution
- Harder to discover (generic keywords)
- Example: "Cloud Infrastructure Builder"

**Narrow Archetype:**
- Focuses on specific tool/pattern
- Simpler constitution
- Easier to discover (specific keywords)
- Example: "Terraform Module Builder"

**When to choose:**
- Broad: When patterns are highly similar
- Narrow: When tools have distinct patterns

### Pattern 2: Single vs Multiple Archetypes

**Single Archetype:**
- One archetype handles variations
- Uses conditional logic in workflows
- Simpler discovery
- Example: "Container Orchestrator" (K8s, Docker Swarm, ECS)

**Multiple Archetypes:**
- Separate archetype per tool
- Cleaner workflows
- More maintenance
- Example: "Kubernetes Operator", "Docker Compose Builder", "ECS Task Builder"

**When to choose:**
- Single: When >70% patterns overlap
- Multiple: When <50% patterns overlap

### Pattern 3: New vs Extend Existing

**New Archetype:**
- Clean slate
- No legacy constraints
- More files to maintain

**Extend Existing:**
- Add to existing archetype
- Leverage existing patterns
- Risk of bloat

**When to choose:**
- New: When fundamentally different problem
- Extend: When natural evolution of existing

### Pattern 4: Overlap Analysis Between Existing Archetypes

**Purpose:** Evaluate whether two or more archetypes have significant overlap and should be merged, refactored, or kept separate.

**archetype-architect provides structural context:**
- Manifest keyword overlap analysis
- Constitution rule similarity
- Workflow pattern comparison
- Discovery routing conflicts

**Delegate detailed domain comparison to specialists:**
- Domain-specific comparison via `/solution-compare`
- User provides comparison criteria and context

**Execution:**

Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py --query "{archetype_1_keywords}" --top 5 --json`

Then compare against archetype_2 results.

**Overlap Analysis Steps:**

1. **Keyword Overlap Calculation:**
   ```
   Archetype A keywords: [k1, k2, k3, k4, k5]
   Archetype B keywords: [k2, k4, k6, k7, k8]
   
   Common: [k2, k4] = 2
   Total unique: [k1, k2, k3, k4, k5, k6, k7, k8] = 8
   Overlap: 2/8 = 25%
   ```

2. **Cross-Discovery Test:**
   - Query archetype A's keywords → Does B match with high score?
   - Query archetype B's keywords → Does A match with high score?
   - High cross-match indicates routing confusion

3. **Purpose Statement Comparison:**
   - Extract descriptions from both manifests
   - Identify shared problem domains
   - Flag potential user confusion scenarios

**Decision Matrix:**

| Overlap % | Cross-Match Score | Recommendation |
|-----------|------------------|----------------|
| <30% | <15 | Keep separate (distinct purposes) |
| 30-50% | 15-29 | Review boundaries, consider refactor |
| 50-70% | ≥30 | Strong candidate for merge |
| >70% | ≥30 | Merge recommended, significant duplication |

**Output:**
```
OVERLAP ANALYSIS REPORT
─────────────────────────────────────────────────────
Archetype A: {archetype_a}
Archetype B: {archetype_b}

KEYWORD ANALYSIS:
  A keywords: [{list}]
  B keywords: [{list}]
  Common: [{list}]
  Overlap: {percentage}%

CROSS-DISCOVERY:
  Query A keywords → B matches: {score}
  Query B keywords → A matches: {score}
  Routing conflict risk: {LOW/MEDIUM/HIGH}

PURPOSE COMPARISON:
  A: {description_a}
  B: {description_b}
  Shared domains: [{list}]

RECOMMENDATION: {KEEP SEPARATE / REFACTOR BOUNDARIES / MERGE}

Rationale:
- {reason_1}
- {reason_2}
- {reason_3}
```

### Pattern 5: Purpose Coverage Validation

**Purpose:** Verify an archetype fully addresses its stated scope without gaps or overreach.

**archetype-architect provides structural validation:**
- Constitution use cases vs workflow coverage
- Stated keywords vs actual routing effectiveness
- Dependency completeness

**Delegate domain validation to specialists via user context:**

**Execution Steps:**

1. **Extract Stated Purpose:**
   - Read constitution "Use Cases" section
   - Read manifest description
   - List all claimed capabilities

2. **Verify Workflow Coverage:**
   - For each use case, identify which workflow handles it
   - Flag use cases with no clear workflow path
   - Flag workflows that don't map to stated use cases

3. **Test Discovery Coverage:**
   - For each stated use case, run discovery
   - Verify archetype routes correctly
   - Flag routing gaps

**Output:**
```
PURPOSE COVERAGE REPORT
─────────────────────────────────────────────────────
Archetype: {archetype}

STATED USE CASES:
1. {use_case_1} → Covered by: {workflow} ✓
2. {use_case_2} → Covered by: {workflow} ✓
3. {use_case_3} → NOT COVERED ❌

ROUTING COVERAGE:
1. Query: "{use_case_1}" → Score: {score} ✓
2. Query: "{use_case_2}" → Score: {score} ✓
3. Query: "{use_case_3}" → Score: {score} (below threshold) ⚠️

GAPS IDENTIFIED:
- {gap_1}
- {gap_2}

OVERREACH IDENTIFIED:
- Workflow handles {capability} not in stated purpose

RECOMMENDATION:
- Add workflow coverage for: {list}
- Add keywords for: {list}
- Remove or document: {list}
```

### Pattern 6: Delegation to Domain Specialists

**Key Principle:** archetype-architect provides structural and form-based comparison context; detailed domain comparison is delegated.

**What archetype-architect compares directly:**
- Manifest schema compliance
- Constitution structure and completeness
- Workflow organization and naming
- Discovery routing effectiveness
- File organization and naming conventions

**What archetype-architect delegates:**
- Domain-specific technical comparison → `/solution-compare` with user context
- Code quality comparison → relevant domain archetype
- Documentation quality → `/compare-documentation`

**Delegation Pattern:**
```
User: /compare-archetype-architect "Compare kubernetes-operator vs helm-chart-builder"

archetype-architect:
1. Analyze structural differences (manifest, constitution, workflows)
2. Calculate keyword overlap
3. Test cross-discovery routing
4. Generate structural comparison report

5. Delegate domain comparison:
   "For detailed Kubernetes domain comparison, invoke:
   /solution-compare 'kubernetes-operator vs helm-chart-builder
   for {user_provided_criteria}'"

6. Combine structural insights with delegation guidance
```

**User Input Integration:**
- User provides: comparison criteria, use case context, decision factors
- archetype-architect provides: structural form, routing analysis, ecosystem context
- Combined: comprehensive comparison with appropriate specialist delegation

## Examples

### Example 1: Kubernetes Archetypes
```
/compare-archetype-architect "
Compare approaches for Kubernetes development:

Option A: Single 'Kubernetes Developer' archetype
- Covers operators, controllers, CRDs, Helm charts
- Broad scope, complex workflows

Option B: Multiple specialized archetypes
- 'K8s Operator Builder'
- 'K8s Controller Builder'
- 'Helm Chart Builder'
- 'K8s CRD Designer'

Context: Team builds all types of K8s resources
"

Output:
→ Analyzing options...

Option A (Single Broad):
- Pros: One archetype to maintain, unified patterns
- Cons: Complex discovery, large constitution, conditional logic
- Complexity: High
- Discovery confidence: Medium (60-70%)

Option B (Multiple Narrow):
- Pros: Clear discovery, focused patterns, easier maintenance
- Cons: 4x files, potential duplication
- Complexity: Medium per archetype
- Discovery confidence: High (85-95%)

RECOMMENDATION: Option B (Multiple Narrow)

Rationale:
- K8s operators vs Helm charts have distinct patterns
- Better discovery with specific keywords
- Easier for users to find right tool
- Patterns don't overlap enough to justify single archetype

Trade-off: More files, but cleaner architecture
```

### Example 2: API Documentation
```
/compare-archetype-architect "
Compare:
Option A: Extend 'Documentation Evangelist' with API docs
Option B: New 'API Documentation Generator' archetype

Context: Need OpenAPI/Swagger generation
"

Output:
→ Analyzing overlap with existing archetypes...

Option A (Extend Existing):
- Current: General documentation
- Add: API-specific patterns
- Overlap: 40% (both generate docs)
- Risk: Bloat existing archetype

Option B (New Archetype):
- Focused: API documentation only
- Technologies: OpenAPI, Swagger, Postman
- Overlap: 20% (general doc patterns)
- Benefit: Clear discovery

RECOMMENDATION: Option B (New Archetype)

Rationale:
- API docs have unique patterns (schemas, endpoints)
- Different tools (OpenAPI vs Markdown)
- Low overlap with general documentation
- Better keyword discovery ("swagger" vs "documentation")
```

## Error Handling

**Insufficient Information**:
```
⚠️ Need More Details

Please provide for each option:
1. Scope (what it covers)
2. Technologies
3. Use cases (3-5)
4. Overlaps with existing archetypes

Example:
/compare-archetype-architect "
Option A: {name}
  Scope: {description}
  Technologies: {list}
  Use Cases: {list}

Option B: {name}
  ...
"
```

**No Clear Winner**:
```
⚠️ Options Are Equally Valid

Both approaches have merit:
- Option A: {pros}
- Option B: {pros}

Recommendation: Start with {simpler option}
- Easier to implement
- Can evolve to other option later
- Lower risk
```

## References

- **Existing Archetypes**: Browse .windsurf/workflows/ for patterns
- **Category Definitions**: See CATEGORY_ROUTING.yaml
- **System Quick Start**: ../QUICK_START.md
