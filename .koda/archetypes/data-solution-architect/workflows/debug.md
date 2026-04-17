---
description: Debug data solution design issues, requirement gaps, and delegation failures (Data Solution Architect)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Issue Type

Extract from $ARGUMENTS:
- Issue description (design flaw, missing requirements, delegation failure)
- Affected solution components
- Error messages or symptoms
- Current SOLUTION_DESIGN.md state (if exists)

**Issue Categories:**
- **Design Issues**: Architecture flaws, technology mismatches, scalability problems
- **Requirement Gaps**: Missing MVI elements, incomplete business rules
- **Delegation Failures**: Wrong archetype assigned, integration issues between specialists
- **Governance Violations**: Security gaps, compliance failures, hardcoded values

### 2. Analyze Root Cause

**For Design Issues:**
1. Review SOLUTION_DESIGN.md architecture diagram
2. Check technology stack against volume/complexity requirements
3. Validate Medallion layer assignments (Bronze/Silver/Gold)
4. Verify failure strategy is defined and appropriate

**For Requirement Gaps:**
1. Run MVI checklist against current documentation:
   - Source: Location, format, frequency, volume
   - Target: Destination, database, schema, table name
   - Logic: Business rules, transformations, quality expectations
   - Security: PII identification, access controls
   - NFRs: Retention, SLA, history handling
2. Identify missing elements

**For Delegation Failures:**
1. Review Implementation Plan task assignments
2. Verify archetype selection matches task type:
   - Ingestion → data-sourcing-specialist or pipeline-builder
   - Transformation → transformation-alchemist (Spark) or sql-query-crafter (SQL)
   - Quality → quality-guardian
   - Orchestration → pipeline-orchestrator
3. Check for integration gaps between delegated components

**For Governance Violations:**
1. Scan for hardcoded paths, credentials, database names
2. Verify env-config.yaml usage
3. Check PII handling and RBAC definitions

### 3. Generate Diagnostic Report

Present findings in structured format:
- Solution name and issue type
- Severity assessment (HIGH/MEDIUM/LOW)
- Root cause analysis details
- Affected components and their impact
- Recommended fixes prioritized by urgency
- Delegation adjustments if applicable

### 4. Apply Fixes

Based on issue type:

**Design Issues:**
- Update SOLUTION_DESIGN.md with corrected architecture
- Regenerate Mermaid diagrams
- Adjust technology stack recommendations

**Requirement Gaps:**
- Switch to Interrogation Mode
- Generate numbered list of missing information
- Do not proceed until gaps filled

**Delegation Failures:**
- Re-run archetype discovery for affected tasks
- Update Implementation Plan assignments
- Ensure test requirements are included

**Governance Violations:**
- Replace hardcoded values with configuration references
- Update env-config.yaml
- Add missing security controls

### 5. Validate Fix

1. Re-check against constitution hard-stop rules
2. Verify MVI completeness
3. Confirm delegation assignments are correct
4. Run discovery script to validate archetype selections

## Error Handling

**Missing SOLUTION_DESIGN.md**: Cannot debug what doesn't exist. Route to `/scaffold-data-solution-architect` first.

**Circular Dependencies**: If delegated archetypes have conflicts, escalate to manual review.

**Scope Creep**: If debugging reveals need for complete redesign, recommend starting fresh with scaffold workflow.

## Examples

### Example 1: Missing Requirements
```
/debug-data-solution-architect "
The data pipeline is failing but we don't have clear SLA requirements.
Solution: customer-360-pipeline
"
```

### Example 2: Wrong Technology Selection
```
/debug-data-solution-architect "
SQL queries are timing out processing 500GB of data.
Should we have used Spark instead?
"
```

### Example 3: Delegation Issue
```
/debug-data-solution-architect "
The transformation-alchemist output doesn't match what quality-guardian expects.
Schema mismatch between pipeline stages.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/data-solution-architect/data-solution-architect-constitution.md`
- **Related Workflows**: scaffold-data-solution-architect, refactor-data-solution-architect
- **Specialist Archetypes**: data-sourcing-specialist, transformation-alchemist, sql-query-crafter, quality-guardian, pipeline-orchestrator
