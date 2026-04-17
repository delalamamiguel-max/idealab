---
description: Compare SQL query approaches and patterns (SQL Query Crafter)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype sql-query-crafter --json ` and parse for SNOWFLAKE_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: problem description or existing query, comparison criteria (performance, readability, maintainability, cost), constraints (data volume, query complexity, team skills). Request clarification if incomplete.

### 4. Generate Alternatives

Create 2-3 different SQL approaches following constitution patterns:

**Approach 1: CTE-Based** (Recommended for readability)
**Approach 2: Subquery-Based** (Compact, fewer temp objects)
**Approach 3: Materialized View** (Best for repeated queries)

Each approach includes: complete SQL code, explanation of pattern, when to use, pros and cons.

### 5. Generate Comparison Matrix

Compare approaches on:
- **Performance**: Execution time, resource usage, query plan efficiency
- **Cost**: Compute cost, storage cost, maintenance cost
- **Maintainability**: Code clarity, debugging ease, modification effort
- **Complexity**: Lines of code, cognitive load, learning curve
- **Scalability**: Performance with data growth, resource scaling

Provide metrics table with scores (1-5) and detailed analysis.

### 6. Add Recommendations

Recommend best approach with justification based on: use case fit, team capabilities, performance requirements, cost constraints, long-term maintenance.

Include migration guidance if changing from existing approach, testing strategy, monitoring recommendations.

### 7. Validate and Report


Generate decision matrix. Report completion with recommendation and next steps.

## Error Handling

**Insufficient Context**: Request problem details, data volumes, and performance requirements.

**Unclear Criteria**: Suggest standard comparison dimensions.

**Too Similar**: Explain key differentiators or suggest alternative comparison.

## Examples

**Example 1**: `/compare-sql Compare CTE vs subquery for customer aggregation` - Output: 2 approaches with performance comparison

**Example 2**: `/compare-sql Should I use window functions or self-join for ranking?` - Output: 3 approaches with complexity analysis

**Example 3**: `/compare-sql Compare clustering strategies for large fact table` - Output: Clustering options with cost-benefit analysis

## References

Original: `vibe_cdo/sql_query_crafter/prompts/04_compare_prompt.md` | Constitution: `../../sql-query-crafter-constitution.md`
