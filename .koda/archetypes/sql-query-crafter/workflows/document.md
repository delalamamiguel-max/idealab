---
description: Generate documentation for SQL queries and database schemas (SQL Query Crafter)
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
Extract from $ARGUMENTS: SQL file path or query, target audience (developers, analysts, business users), documentation scope (query explanation, schema docs, data dictionary). Request clarification if incomplete.

### 4. Analyze Code/System

Analyze SQL query/schema: identify tables and columns, understand JOIN relationships, document aggregations and calculations, explain WHERE filters and business logic, identify parameters and variables, note performance considerations.

### 5. Generate Documentation

Create comprehensive documentation with: query purpose and business context, input parameters and expected values, output schema and column descriptions, data flow diagram (tables → transformations → output), example usage with sample data, performance characteristics, troubleshooting guide.

Include README format, inline SQL comments, data dictionary, ER diagrams (if schema documentation).

### 6. Add Recommendations

Include recommendations for documentation maintenance (update on schema changes, version control docs with code), usage guidance (when to use query, parameter guidelines), optimization notes (indexing recommendations, query tuning tips), monitoring (query performance tracking).

### 7. Validate and Report


Generate documentation artifacts. Report completion with documentation files and publishing guidance.

## Error Handling

**Insufficient Context**: Request complete SQL code and business context.

**Complex Query**: Break documentation into sections (extract, transform, aggregate).

**Missing Business Logic**: Request stakeholder input for business rules.

## Examples

**Example 1**: `/document-sql Create docs for customer_aggregation.sql` - Output: README with query explanation, parameters, examples

**Example 2**: `/document-sql Generate data dictionary for sales schema` - Output: Schema docs with table/column descriptions, relationships

**Example 3**: `/document-sql Document reporting query for business users` - Output: Non-technical docs with business context and usage

## References

Original: `vibe_cdo/sql_query_crafter/prompts/06_document_prompt.md` | Constitution: `../../sql-query-crafter-constitution.md`
