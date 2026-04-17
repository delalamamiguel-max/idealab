---
description: Analyze upstream and downstream dependencies to assess the impact of schema or logic changes (Impact Analyzer)
---

User input: $ARGUMENTS

## Execution Steps (Analysis-Only)

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype impact-analyzer --json ` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
-- The constitution rules are already loaded in context above.
-- Load `${ARCHETYPES_BASEDIR}/impact-analyzer/templates/env-config.yaml` for ignored paths and search depth limits.

### 3. Parse Input
Extract from $ARGUMENTS:
- **Target Object**: The table, column, or file being changed (e.g., `CIM_HIST`, `ncloc`).
- **Change Type**: `ADD_COLUMN`, `DROP_COLUMN`, `MODIFY_LOGIC`, `RENAME`.
- **Codebase Path**: Absolute path to the codebase root (e.g., `/Users/jdoe/workspaces/CCDM`).

If the Codebase Path is missing or does not exist, pause execution and ask the user to provide a valid absolute path before continuing.

### 4. Dependency Scanning
Perform a multi-layer scan across the workspace:
- **SQL Layer**: Scan `*.sql` files for table usage (`FROM`, `JOIN`, `INTO`) and column usage (`SELECT`, `WHERE`, `GROUP BY`).
- **Orchestration Layer**: Scan `*.txt` (TWS) and `*.py` (Airflow) for job dependencies and file references.
- **Code Layer**: Scan `*.py` (Spark/Pandas) for dataframe operations referencing the object.
- **Config Layer**: Scan `*.yaml`, `*.json` for metadata or schema definitions.

*Note: Use `grep` or AST parsing to distinguish between exact matches and partial string matches.*

### 5. Quantify Impact (Automated Metrics)
Run `python ../../scripts/python/collect-impact-stats.py --root "$CODEBASE_PATH" --target "$TARGET_OBJECT" --output ../../cache/impact_scope_stats.json` to capture impacted-file counts and risk scoring only. Do not include development or implementation guidance.

### 6. Impact Graph Construction
Build a dependency graph:
- **Direct Impact**: Files that explicitly name the target object.
- **Downstream Impact**: Files that depend on the "Direct Impact" files (e.g., a TWS job that runs a SQL script).
- **Breaking Changes**: Flag usages that will break based on the `Change Type` (e.g., `SELECT *` is a risk for `ADD_COLUMN`, explicit reference is a break for `DROP_COLUMN`).

### 7. Generate Impact Report (Findings + Single Estimate Table)
Create a Markdown report (`impact_report_<timestamp>.md`) containing:
- **Executive Summary**: Total files affected, Risk Level (High/Med/Low).
- **Affected Artifacts**: List of files grouped by type (SQL, Pipeline, Code).
- **Visual Graph**: (Optional) Mermaid or DOT diagram of the dependency tree.
- Exclude implementation guidance: Do not list fix tasks, archetypes to run, or PR steps.
- Include one unified informational estimate table: real-world phase hours (analysis, development, testing, deployment) using `phase_models` + `buffer_defaults` from `estimation-config.json`. No separate "analysis-only" table.
Make sure the estimates are in 'number of hours' required to perform a certain phase.
Unified Estimate Table columns: `Phase`, `Task Focus`, `Complexity`, `Base Hours`, `Multiplier`, `Total Hours`.

Example skeleton (multi_layer):

| Phase | Task Focus | Complexity | Base Hours | Multiplier | Total Hours |
|-------|------------|------------|------------|------------|-------------|
| Analysis & Design | Requirements, lineage, contracts | High | 12 | 1.00 | 12.0 |
| Development | Ingest, transforms, views | High | 36 | 1.00 | 36.0 |
| Unit Testing | Component tests | High | 18 | 1.00 | 18.0 |
| Integration Testing | Orchestration, data quality | High | 16 | 1.00 | 16.0 |
| Deployment/Ops | Promotion, monitoring | High | 8 | 1.00 | 8.0 |
| Subtotal |  |  | 90.0 |  | 90.0 |
| Buffer | Based on `buffer_defaults` (multi_layer) | 35% |  | 1.35 | 121.5 |
| Total Estimate |  |  |  |  | 121.5 |

Note: Table is informational; archetype remains analysis-only (no implementation actions).

### 8. Validate and Report

## Error Handling

**Ambiguous Target**: If the search term matches multiple objects (e.g., `id` column exists in 10 tables), pause and ask user to qualify the object (e.g., `CIM_HIST.id`).

**No Usage Found**: If no dependencies are found, verify the spelling of the target object and report "No Impact Detected" with a warning to check external systems.

**Environment Failure**: Report missing search tools (grep, find) or invalid configuration.

## Examples

**Example 1: Column Addition**
```
/impact-analysis Check impact of adding column 'loyalty_score' to table 'CIM_CUST'

Input: Target='CIM_CUST', Change='ADD_COLUMN'
Output: Report listing 3 SQL files using 'SELECT *' (High Risk) and 2 TWS jobs (Low Risk).
```

**Example 2: Table Rename**
```
/impact-analysis I am renaming 'STG_SALES' to 'RAW_SALES'. What breaks?

Input: Target='STG_SALES', Change='RENAME'
Output: List of 15 files (Ingest SQL, Transformation SQL, TWS Streams) that need Find/Replace.
```

## References

Constitution: (pre-loaded above)

Scope Boundaries:
- Analysis-only; no patches, PRs, rollback, or change commands.
- Reports must focus on findings, risks, dependencies, and timing.
