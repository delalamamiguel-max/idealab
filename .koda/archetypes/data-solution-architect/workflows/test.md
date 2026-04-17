---
description: Validate data solution designs for completeness, governance compliance, and delegation accuracy (Data Solution Architect)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Test Scope

Extract from $ARGUMENTS:
- SOLUTION_DESIGN.md location
- Test scope (full validation, specific section, governance only)
- Known areas of concern

### 2. Run MVI Completeness Test

Validate Minimum Viable Information is complete. Check for:
- Source: Location, format, frequency, volume
- Target: System, database, schema, table name
- Logic: Business rules, transformations, quality expectations
- Security: PII identification, access controls
- NFRs: Data retention policy, SLA requirements, history handling (SCD type)

**FAIL** if any required element is missing.

### 3. Run Enterprise Standards Test

Validate compliance with hard-stop rules:

**Medallion Pattern:**
- Target classified as Bronze, Silver, or Gold
- Classification is appropriate for data state

**Failure Strategy:**
- Failure strategy defined (Fail Fast, Dead Letter Queue, Alert)
- Recovery procedures documented

**Cost Awareness:**
- T-shirt size estimate provided (S/M/L)
- Compute and storage considerations documented

**Configuration Standard:**
- No hardcoded paths detected
- No hardcoded credentials detected
- No hardcoded database/schema names
- env-config.yaml referenced appropriately

### 4. Run Architecture Test

Validate design decisions:

**Technology Selection:**
- Technology matches volume requirements (SQL for smaller datasets, Spark for larger)
- Stack is justified in documentation
- User overrides are documented if applicable

**Security:**
- PII handling defined
- RBAC requirements specified
- No insecure data transfer methods

**Scalability:**
- Design can handle stated volume
- Growth considerations documented

### 5. Run Delegation Test

Validate Implementation Plan assignments:

For each task in the plan:
1. Run archetype discovery against task description
2. Compare assigned archetype to recommended archetype
3. Flag mismatches

**Validation Criteria:**
- Each task has an assigned archetype
- Assigned archetype matches discovery recommendation (or override documented)
- Test requirements specified for each task
- Integration points identified between tasks

### 6. Generate Test Report

Produce validation report covering:
- Solution name and test date
- MVI completeness status (PASS/FAIL)
- Enterprise standards compliance (PASS/FAIL per category)
- Architecture validation status
- Delegation validation with mismatch count
- Overall verdict (PASS/PASS WITH WARNINGS/FAIL)
- Summary and recommendations

## Error Handling

**Missing SOLUTION_DESIGN.md**: Cannot test what doesn't exist. Route to `/scaffold-data-solution-architect`.

**Partial Design**: If design is incomplete, report which sections need completion before full validation.

## Examples

### Example 1: Full Validation

```
/test-data-solution-architect "
Validate the complete solution design for customer-360-pipeline.
Location: projects/customer-360/docs/SOLUTION_DESIGN.md
"
```

### Example 2: Governance Focus

```
/test-data-solution-architect "
Check governance compliance only for the data-lake-ingestion solution.
Concerned about hardcoded values after recent audit.
"
```

### Example 3: Pre-Implementation Check

```
/test-data-solution-architect "
Final validation before implementation begins.
Solution: real-time-inventory
Scope: full
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/data-solution-architect/data-solution-architect-constitution.md`
- **Related Workflows**: scaffold-data-solution-architect, debug-data-solution-architect
- **Quality Guardian**: For data quality test implementation after design approval
