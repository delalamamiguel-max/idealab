# XFlow Orchestrator Archetype

The XFlow Orchestrator archetype owns XFlow JSON pipeline configuration generation, validation, and management. It standardizes how teams create, debug, refactor, and document XFlow configs for ingesting data from JDBC, Kafka, File, and HTTP sources into ADLS/Delta targets on Databricks.

## Repository Layout
```
xflow-orchestrator/
├── README.md
├── xflow-orchestrator-constitution.md
├── manifest.yaml
├── requirements.txt
├── templates/
│   └── env-config.yaml
└── .windsurf/
    └── workflows/
        ├── scaffold-xflow-orchestrator.md
        ├── debug-xflow-orchestrator.md
        ├── compare-xflow-orchestrator.md
        ├── refactor-xflow-orchestrator.md
        ├── document-xflow-orchestrator.md
        └── test-xflow-orchestrator.md
```

## Quick Start
1. **Validate the environment**
   ```bash
   python ../../00-core-orchestration/scripts/validate_env.py --archetype xflow-orchestrator --json
   ```
2. **Load governance artifacts**
   - Read `xflow-orchestrator-constitution.md` for hard-stop rules.
3. **Pick a workflow**
   - `/scaffold-xflow-orchestrator` → Generate a new XFlow JSON config
   - `/debug-xflow-orchestrator` → Fix config errors
   - `/refactor-xflow-orchestrator` → Improve an existing config
   - `/compare-xflow-orchestrator` → Compare approaches
   - `/document-xflow-orchestrator` → Generate documentation
   - `/test-xflow-orchestrator` → Validate a config
4. **Fill out template inputs**
   - Copy `templates/env-config.yaml` and populate secret scope, storage account, and source/target defaults.

## Workflows
| File | Purpose |
| --- | --- |
| `scaffold-xflow-orchestrator.md` | Generate a production-ready XFlow JSON config from natural language requirements. |
| `debug-xflow-orchestrator.md` | Diagnose and fix XFlow config errors, validation failures, and runtime issues. |
| `compare-xflow-orchestrator.md` | Compare source types, write modes, target formats, and architecture patterns. |
| `refactor-xflow-orchestrator.md` | Refactor an existing config to apply best practices, fix violations, and optimize. |
| `document-xflow-orchestrator.md` | Generate comprehensive documentation, schema references, and operational runbooks. |
| `test-xflow-orchestrator.md` | Generate validation test suites (pytest, standalone scripts, or checklists). |

## XFlow Configuration Scope

This archetype covers the full XFlow JSON configuration structure:

### Source Types
- **JDBC**: Oracle, SQL Server, PostgreSQL, MySQL, Snowflake, Vertica, Teradata, Trino
- **Kafka**: Streaming ingestion from Kafka topics
- **File**: CSV, Parquet, JSON, XML, Avro, ORC, Fixed-width from ADLS
- **HTTP**: File Gateway (FileGW) push-based ingestion
- **Azure Files**: Pull-based ingestion from Azure File Share

### Target Formats
- **Delta**: Default, with ACID properties and time-travel
- **Parquet**: Columnar format for analytics
- **CSV**: Interchange format
- **Database**: Direct database write

### Transformation Types
- `hashingAndEncrypt` — PII protection via Voltage
- `dateFormat` — Date/time format conversion and generation
- `regex` — Pattern extraction and reformatting
- `replace` — Value substitution with reserved keywords
- `uppercase` / `lowercase` — Case normalization
- `epochToTimestamp` — Unix time conversion
- `addColumn` — Derived column generation

### Validation Types
- `schema` — Schema and data type validation
- `regex` — Pattern-based column validation
- `duplicateFileCheck` — Duplicate file detection
- `notNull` — Required column checks
- `primaryKey` — Uniqueness validation

## Constitution Summary

### Hard-Stop Rules (Non-Negotiable)
- No missing mandatory root fields
- No plaintext credentials
- No schema columns without name and type
- No upsert without primary keys
- No JDBC/Kafka source without required fields
- No targets as single object
- No partition columns without partitionOrder
- No hashingAndEncrypt without encryption parameters

### Mandatory Patterns
- Structural validation on all configs
- Control columns on all targets
- Write mode aligned with data pattern
- Valid Spark SQL column types
- Default trimSpacesInd: true
- Derived columns must have transformations

### Preferred Patterns
- Delta target format with vacuumDaysOld
- Snappy compression
- JDBC fetchSize: 20000
- Global transformation for data quality
- Descriptive snake_case naming
- Error handling configuration

## Templates
- `templates/env-config.yaml` collects secret scope, storage account, source/target defaults, global transformation settings, error handling, and partition configuration.
- Copy it into your workspace before running workflows to ensure consistent defaults.

## Related Docs
- Router governance: `../00-core-orchestration/solution/router.md`
- Impact analysis patterns: `../00-core-orchestration/solution/solution-compare.md`
- Related archetypes: `data-pipeline-builder`, `transformation-alchemist`, `quality-guardian`
