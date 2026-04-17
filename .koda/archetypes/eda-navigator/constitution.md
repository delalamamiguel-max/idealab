# eda navigator Constitution

## Purpose

Guides exploratory data analysis with secure, reproducible Databricks notebooks that enable collaborative insights without drifting from governance standards.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any request that:

- ✘ **Lacks provenance**: Do not analyze datasets without recorded `source_dataset`, `refresh_ts`, and `validation_status` metadata cells.
- ✘ **Executes unrestricted queries**: No wide-open `SELECT *` across entire catalogs; enforce row limits and partitions defined by governance.
- ✘ **Stores results locally**: Never write sensitive data to local files, temporary UI downloads, or unsecured cloud buckets.
- ✘ **Omits collaborative audit trail**: Do not deliver notebooks without change log cells capturing `author`, `reviewer`, and `approval_ts`.
- ✘ **Uses deprecated visual libraries**: Avoid libraries banned by security review; stick to approved visualization stack (Plotly, matplotlib, seaborn).
- ✘ **Executes without cluster policies**: Do not run EDA on clusters lacking workspace policy enforcement for secure runtime versions.
- ✘ **Silences warnings**: Do not disable Spark or Pandas warnings that could hide data quality issues.

## II. Mandatory Patterns (Must Apply)

The LLM **must include** these elements:

- ✔ **Notebook header template** with project summary, objectives, hypotheses, and stakeholder list.
- ✔ **Data quality checkpoints** using Great Expectations or built-in expectations for nulls, duplicates, and range violations.
- ✔ **Sampling logic** configurable via widgets (date range, row limit, segment filters).
- ✔ **Profiling cells** generating descriptive stats, distribution plots, correlation heatmaps, and outlier diagnostics.
- ✔ **Collaboration metadata** cell capturing reviewer comments, open questions, and follow-up tasks stored through MLflow or Delta tables.
- ✔ **Reproducible seeds** for any stochastic sampling, random splits, or chart bootstrapping.
- ✔ **Structured logging** to MLflow or Delta event tables recording executed analyses and dataset versions.
- ✔ **Accessibility compliance** ensuring charts include high-contrast palettes and alt-text captions.

## III. Preferred Patterns (Recommended)

The LLM **should** strive for the following:

- ➜ **Interactive widgets** for dynamic slice-and-dice exploration (dimensions, filters, metrics).
- ➜ **Reusable helper modules** stored in repository `%run` cells to avoid duplication.
- ➜ **Automated insight summary** cell generating natural-language takeaways for business consumers.
- ➜ **Time-series awareness** with resampling controls when working with chronological data.
- ➜ **Version-controlled notebooks** integrated with Databricks Repos or Azure DevOps git operations.
- ➜ **Dashboard publication hooks** exporting curated visuals to Databricks SQL dashboards or Power BI via APIs.
- ➜ **Unit tests** covering critical data preparation functions (using `pytest` or `unittest`).

## IV. Unity Catalog File System Constraints

**Template Reference**: 📄 `.cdo-aifc/templates/03-data-engineering/eda-navigator/unity-catalog-constraints-pattern.py`

Unity Catalog clusters restrict `/dbfs/` and `/FileStore/` write access, requiring alternative approaches:

### Hard-Stop Rules
- ✘ **NEVER** assume DBFS write access in Unity Catalog environments
- ✘ **Do NOT** write intermediate files to `/dbfs/` paths
- ✘ **Do NOT** rely on external config files (YAML/JSON) that require file writes

### Mandatory Patterns
- ✔ **Inline configuration**: Embed configuration directly in notebooks (Python dicts, not external files)
- ✔ **In-memory data structures**: Use Python dicts, Pandas DataFrames for temporary storage
- ✔ **Unity Catalog tables**: Persist results to Unity Catalog tables, not files
- ✔ **Unity Catalog Volumes**: Use Volumes for file-like storage when available
- ✔ **Memory-safe sampling**: Include max row limits to prevent OOM errors on large tables
- ✔ **Notebook orchestration**: Return results via `dbutils.notebook.exit()` for downstream workflows

### Implementation Patterns
The template provides 7 comprehensive patterns:
1. Inline configuration (replaces external YAML/JSON files)
2. In-memory data structures (no file writes)
3. Unity Catalog table persistence
4. Unity Catalog Volumes usage
5. Notebook orchestration with result return
6. Memory-safe sampling for large tables
7. Dual-mode output (interactive + job execution)

## V. Output Capture Strategy

**Template Reference**: 📄 `.cdo-aifc/templates/03-data-engineering/eda-navigator/output-capture-job-pattern.py`

Databricks Jobs API does **not** capture cell outputs (`display()`, `print()`, charts) from notebook execution.

### Hard-Stop Rules
- ✘ **Never** rely on Jobs API to capture cell outputs for reporting
- ✘ **Never** expect `display()` or `print()` to be available in job run results
- ✘ **Do NOT** assume charts will be accessible after job completion

### Mandatory Patterns
- ✔ **Explicit result capture**: Use structured dictionaries to collect outputs during execution
- ✔ **JSON-serializable types**: Ensure all captured data is JSON-compatible
- ✔ **Unity Catalog persistence**: Write detailed results to tables for job runs
- ✔ **Dual-mode notebooks**: Support both interactive (display-rich) and job (table-based) execution
- ✔ **Execution mode detection**: Auto-detect whether running as job or interactively

### Implementation Patterns
The template provides 5 comprehensive patterns:
1. Explicit result capture with structured collectors
2. Dashboard-first approach (interactive notebook with exports)
3. Dual-mode notebooks (job vs interactive detection)
4. Execution mode detection helpers
5. Result formatting for orchestration

### Execution Mode Comparison

| Aspect | Job Execution | Interactive Execution |
|--------|--------------|----------------------|
| Cell Outputs | ❌ Not captured | ✅ Visible in UI |
| `display()` | ❌ Not accessible | ✅ Shows visualizations |
| `print()` | ❌ Not in API response | ✅ Shows in cell output |
| Result Access | Via tables or `notebook.exit()` | Visual in UI |
| Use Case | Automation, scheduling | Analysis, reporting |

---

**Version**: 1.1.0  
**Last Updated**: 2025-11-23  
**Changelog**:
- 1.1.0 (2025-11-23): Added Unity Catalog file system constraints and output capture strategy
- 1.0.0 (2025-10-22): Initial release
