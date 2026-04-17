---
description: Refactor data solution designs to improve architecture, delegation, and governance compliance (Data Solution Architect)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Refactoring Scope

Extract from $ARGUMENTS:
- Current SOLUTION_DESIGN.md location
- Refactoring goals (scalability, governance, cost optimization, modernization)
- Constraints (timeline, budget, existing dependencies)
- Technology preferences or mandates

### 2. Assess Current State

Review existing SOLUTION_DESIGN.md for:

**Architecture Assessment:**
- Current technology stack and its appropriateness
- Medallion layer assignments (Bronze/Silver/Gold)
- Data flow patterns and bottlenecks
- Scalability headroom

**Governance Assessment:**
- Configuration management (hardcoded vs parameterized)
- Security controls (PII handling, RBAC)
- Compliance with enterprise standards

**Delegation Assessment:**
- Current archetype assignments in Implementation Plan
- Integration points between specialist archetypes
- Test coverage requirements

### 3. Generate Refactoring Recommendations

Based on assessment, recommend changes:

**Technology Modernization:**
- SQL to Spark migration for volume scaling
- Batch to streaming for latency reduction
- On-prem to cloud migration patterns

**Governance Improvements:**
- Extract hardcoded values to env-config.yaml
- Add missing security controls
- Implement proper failure strategies

**Delegation Optimization:**
- Reassign tasks to more appropriate archetypes
- Add missing integration tests between components
- Improve task breakdown granularity

### 4. Update SOLUTION_DESIGN.md

Apply approved changes:

1. Update Executive Summary with refactoring context
2. Regenerate Architecture Diagram with new components
3. Revise Technology Stack section with justifications
4. Update Data Flow with new patterns
5. Enhance Security & Governance section
6. Revise Implementation Plan with new assignments

### 5. Re-validate Against Constitution

Ensure refactored design still meets all hard-stop rules:
- No implementation without design approval
- MVI checklist complete
- Enterprise standards (Medallion, failure strategy, cost awareness)
- No hardcoded values
- Security first
- Appropriate technology for data volume

### 6. Update Delegation Assignments

Re-run archetype discovery for affected tasks:

```bash
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py --query "<task description>" --json
```

Update Implementation Plan with:
- New archetype assignments
- Updated test requirements
- Integration checkpoints

## Error Handling

**No Existing Design**: Cannot refactor what doesn't exist. Route to `/scaffold-data-solution-architect`.

**Breaking Changes**: If refactoring would break downstream dependencies, generate impact analysis first.

**Scope Expansion**: If refactoring scope exceeds original boundaries, switch to Interrogation Mode for additional requirements.

## Examples

### Example 1: Scale Improvement
```
/refactor-data-solution-architect "
Current SQL-based pipeline can't handle growing data volume (now 800GB).
Need to migrate to Spark while maintaining existing data contracts.
Solution: sales-analytics-pipeline
"
```

### Example 2: Governance Compliance
```
/refactor-data-solution-architect "
Audit found hardcoded database names in our pipeline.
Need to refactor for proper configuration management.
Solution: customer-data-lake
"
```

### Example 3: Architecture Modernization
```
/refactor-data-solution-architect "
Convert batch processing to near-real-time streaming.
Current SLA is T+1, need to get to T+15min.
Solution: inventory-sync-pipeline
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/data-solution-architect/data-solution-architect-constitution.md`
- **Related Workflows**: scaffold-data-solution-architect, debug-data-solution-architect
- **Specialist Archetypes**: transformation-alchemist, sql-query-crafter, pipeline-orchestrator
