---
description: Compare data quality validation approaches and frameworks (Quality Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype quality-guardian --json ` and parse for GE_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/quality-guardian/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: quality problem, comparison criteria (coverage, performance, ease of use), data characteristics, constraints. Request clarification if incomplete.

### 4. Generate Alternatives

Create 2-3 quality approaches: Great Expectations (Python, comprehensive), Deequ (Scala/Spark, big data), Custom validation (lightweight). Each with configuration examples, use cases, pros/cons.

### 5. Generate Comparison Matrix

Compare on: coverage, performance, ease of use, integration, reporting, maintenance, learning curve, community support. Provide scores and analysis.

### 6. Add Recommendations

Recommend approach with justification. Include implementation guidance, integration strategy, testing approach, monitoring setup.

### 7. Validate and Report


## Error Handling

**Insufficient Context**: Request data volume, validation complexity, team skills.

**Framework Confusion**: Explain key differences with examples.

**Performance Concerns**: Address scalability and optimization strategies.

## Examples

**Example 1**: `/compare-quality Compare Great Expectations vs Deequ for Spark pipeline` - Output: Framework comparison with Spark integration analysis

**Example 2**: `/compare-quality Rule-based vs ML-based anomaly detection` - Output: Approach comparison with accuracy trade-offs

**Example 3**: `/compare-quality Compare inline vs separate quality checks` - Output: Pattern comparison with performance impact

## References

