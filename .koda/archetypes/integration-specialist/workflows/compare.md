---
description: Compare REST/GraphQL API approaches and patterns (Integration Specialist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype integration-specialist --json ` and parse for API_FRAMEWORK, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/integration-specialist/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: API problem, comparison criteria (performance, flexibility, complexity), use case characteristics, constraints. Request clarification if incomplete.

### 4. Generate Alternatives

Create 2-3 API approaches: REST (standard, widely supported), GraphQL (flexible queries), gRPC (high performance). Each with implementation examples, use cases, pros/cons.

### 5. Generate Comparison Matrix

Compare on: performance, flexibility, complexity, client support, tooling, learning curve, network efficiency, caching. Provide scores and analysis.

### 6. Add Recommendations

Recommend approach with justification. Include implementation guidance, client library considerations, migration strategy, testing approach.

### 7. Validate and Report


## Error Handling

**Insufficient Context**: Request use case details, client requirements, performance needs.

**Protocol Confusion**: Explain key differences with concrete examples.

**Client Compatibility**: Address client support and tooling availability.

## Examples

**Example 1**: `/compare-api Compare REST vs GraphQL for mobile app` - Output: Protocol comparison with mobile considerations

**Example 2**: `/compare-api Synchronous vs asynchronous API patterns` - Output: Pattern comparison with latency analysis

**Example 3**: `/compare-api Compare authentication approaches (OAuth2 vs JWT)` - Output: Security pattern comparison

## References

