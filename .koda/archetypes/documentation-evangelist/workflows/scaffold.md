---
description: Generate comprehensive documentation from scratch (Documentation Evangelist)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype documentation-evangelist --json ` and parse for DOC_FORMAT, DIAGRAM_TOOL, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/documentation-evangelist/templates/env-config.yaml` for format (Markdown/Confluence), diagram tools, max line length

### 3. Parse Input
Extract from $ARGUMENTS: component/system to document, audience (developers/operators/business), documentation scope (architecture/operations/troubleshooting/API), diagram requirements. Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse line length > 100 characters
- ✘ Refuse documentation without metadata block (version, author, last updated)
- ✘ Refuse non-Mermaid diagram syntax or invalid Mermaid code
- ✘ Refuse hard-coded links or references (must be parameterized)
- ✘ Refuse missing required sections: Overview, Data Flow, Schema Definitions, Metrics Glossary
If violated, explain clearly and suggest compliant alternative.

### 5. Generate Documentation Scaffold

Create comprehensive documentation with standard structure:

**Metadata Block** (YAML frontmatter or company template):
```yaml
---
title: <Component Name> Documentation
author: <Author Name>
date: <YYYY-MM-DD>
version: 1.0.0
status: Draft
---
```

**Required Sections**:
1. **Overview**: Purpose, scope, audience, key features
2. **Architecture**: Component diagram (Mermaid), technology stack, design decisions
3. **Data Flow**: Source to destination with Mermaid diagram, transformations, quality gates
4. **Schema Definitions**: Tables/entities with Markdown tables, field descriptions, data types
5. **Metrics Glossary**: Key metrics, calculations, thresholds
6. **Operations**: Deployment, monitoring, alerting, runbook
7. **Troubleshooting**: Common issues, debug steps, escalation paths
8. **Appendix**: Glossary, references, change log

**Diagram Templates**:
- Architecture diagram (Mermaid flowchart)
- Data flow diagram (Mermaid graph)
- Sequence diagram for interactions
- Entity relationship diagram for data models

Apply mandatory patterns: metadata header with title/author/date/version, Mermaid diagram validation, company doc template compliance, parameterized external references (links to code, schemas, dashboards).

### 6. Add Recommendations

Include optional sections: performance characteristics, cost considerations, security notes, disaster recovery procedures, future enhancements, FAQ section.

### 7. Validate and Report


Generate separate diagram files (.mmd) if requested. Report completion with file paths, diagram previews, validation results, review checklist, next steps.

## Error Handling

**Hard-Stop Violations**: Explain violation (e.g., line too long, missing metadata), suggest compliant alternative with example.

**Incomplete Input**: List missing information (component details, audience, scope), provide well-formed example.

**Environment Failure**: Report missing tools (markdownlint, mermaid-cli), suggest installation steps.

## Examples

**ETL Pipeline**: `/scaffold-documentation Document customer ETL pipeline: S3 ingestion, Spark transformation, Snowflake loading. Include architecture diagram, data flow, schema definitions, operational runbook, troubleshooting guide. Audience: data engineers.`
Output: Complete documentation with all required sections, Mermaid diagrams, schema tables, troubleshooting guide.

**REST API**: `/scaffold-documentation Create API documentation for customer service: 5 endpoints (CRUD + search), OAuth2 authentication, rate limiting, error codes. Audience: external developers.`
Output: API doc with endpoint specs, auth flow diagram, request/response examples, error handling guide.

**Data Warehouse**: `/scaffold-documentation Document customer data warehouse: 10 dimension tables, 3 fact tables, ETL processes, data lineage. Include ERD, schema definitions, metrics glossary. Audience: analysts and data engineers.`
Output: DW documentation with ERD diagram, table schemas, metric definitions, query examples.

## References

Constitution: (pre-loaded above) | Env Config: `${ARCHETYPES_BASEDIR}/documentation-evangelist/templates/env-config.yaml`
