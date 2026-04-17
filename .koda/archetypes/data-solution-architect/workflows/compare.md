---
description: Compare data solution architectures, technology choices, and design patterns (Data Solution Architect)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Comparison Scope

Extract from $ARGUMENTS:
- Items to compare (solutions, technologies, patterns)
- Comparison criteria (cost, performance, maintainability, governance)
- Decision context and constraints

**Comparison Types:**
- **Solution vs Solution**: Compare two SOLUTION_DESIGN.md documents
- **Technology Choice**: Compare technology options (Spark vs SQL, batch vs streaming)
- **Pattern Selection**: Compare architectural patterns (Lambda vs Kappa, ELT vs ETL)
- **Archetype Selection**: Compare which specialist archetypes to delegate to

### 2. Gather Comparison Data

**For Solution Comparison:**
- Load both SOLUTION_DESIGN.md documents
- Extract key attributes: technology stack, data volume, SLA, cost estimate

**For Technology Comparison:**
- Document capabilities of each technology
- Map to volume/complexity requirements from constitution

**For Pattern Comparison:**
- Document trade-offs of each pattern
- Map to use case requirements

### 3. Apply Comparison Framework

Evaluate against Data Solution Architect decision criteria:

**Volume-Based Decision:**
- Data volume < 10GB: Simpler tools acceptable
- Data volume 10GB-1TB: SQL or Spark depending on complexity
- Data volume > 1TB: Spark/Databricks required

**Complexity-Based Decision:**
- Simple joins/filters: sql-query-crafter
- Complex aggregations/ML: transformation-alchemist
- Cross-system dependencies: pipeline-orchestrator

**Governance Alignment:**
- Both options must meet enterprise standards
- Medallion pattern compatibility
- Configuration management approach

**Cost Comparison:**
- Compute costs (T-shirt sizing)
- Storage costs
- Operational overhead

### 4. Generate Comparison Matrix

Create structured comparison:

| Criterion | Option A | Option B | Winner |
|-----------|----------|----------|--------|
| Data Volume Support | | | |
| Processing Complexity | | | |
| Cost (T-shirt) | | | |
| SLA Achievement | | | |
| Governance Compliance | | | |
| Team Expertise | | | |
| Maintenance Burden | | | |

### 5. Provide Recommendation

Based on comparison matrix:
- Declare recommended option with justification
- Note trade-offs and risks
- Identify scenarios where alternative would be better
- Document any user constraints that influenced decision

### 6. Document Decision

If comparison leads to a decision:
- Update SOLUTION_DESIGN.md with chosen approach
- Document rationale in Technology Stack section
- Note alternatives considered

## Error Handling

**Insufficient Information**: If comparison criteria are unclear, switch to Interrogation Mode.

**Tie Situation**: If options are equivalent, recommend based on team expertise and maintainability.

**Constraint Conflicts**: If user constraints conflict with best practices, document trade-offs clearly.

## Examples

### Example 1: Technology Comparison

```
/compare-data-solution-architect "
Should we use Snowflake SQL or Databricks Spark for our transformation layer?
Data volume: 500GB daily
Complexity: Complex aggregations with window functions
Team: Strong SQL skills, learning Spark
"
```

### Example 2: Solution Comparison

```
/compare-data-solution-architect "
Compare the designs for customer-analytics-v1 vs customer-analytics-v2.
Which better meets our new SLA requirements?
"
```

### Example 3: Pattern Comparison

```
/compare-data-solution-architect "
ELT vs ETL for our new data lake ingestion.
Sources are mixed (APIs, files, databases).
Target is Snowflake with Bronze/Silver/Gold layers.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/data-solution-architect/data-solution-architect-constitution.md`
- **Decision Logic**: See Constitution Section III for technology selection rules
- **Related Workflows**: scaffold-data-solution-architect, refactor-data-solution-architect
