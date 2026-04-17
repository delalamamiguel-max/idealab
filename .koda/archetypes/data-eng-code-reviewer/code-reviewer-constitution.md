# Code Reviewer Constitution (Ultra-Refined)

## Mission Statement
Establish a AI assisted, consistent code and peer review practice that improves correctness, security, performance, and maintainability—so every change is understandable, testable, and safe to operate in production.

This constitution defines the mandatory architectural and quality standards. Any code generated or modified must be cross-referenced against these rules.

---

## Best Practices Reference (templates/)

Each section below is backed by a detailed best-practices template with examples, anti-patterns, and copy-paste-ready starter code. **Always consult the relevant template when implementing or reviewing code.**

| Section | Template | Description |
|---------|----------|-------------|
| §2 Snowflake SQL | [`templates/snowflake-best-practices.md`](templates/snowflake-best-practices.md) | Column pruning, MERGE idempotency, watermarks, injection prevention, pruning-friendly predicates |
| §3 Python | [`templates/python-best-practices.md`](templates/python-best-practices.md) | Type hints, context managers, chunking, exponential backoff, externalized config |
| §4 Shell | [`templates/shell-best-practices.md`](templates/shell-best-practices.md) | Strict mode, path anchoring, trap cleanup, local scoping, safe deletions |
| §5 TWS | [`templates/tws-best-practices.md`](templates/tws-best-practices.md) | Acyclic DAGs, parameterized agents, concurrency controls, SLA alerting, duration safeguards |
| §6 Databricks | [`templates/databricks-best-practices.md`](templates/databricks-best-practices.md) | Widget params, no driver OOM, streaming checkpoints, Delta MERGE, broadcast joins |
| Review Output | [`templates/Code_Review.md.template`](templates/Code_Review.md.template) | Standardized review output format with Hard-Stop / Quality / Advisory sections |

---

## 1. Cross-cutting (Universal Standards)

### Hard-Stop Rules (✘)
- ✘ **No Hardcoded Secrets**: Never embed credentials, API keys, or tokens in code or logs; use Secret Manager.
- ✘ **No Data Corruption Risk**: Reruns must be idempotent and never lead to duplicate or corrupt data.
- ✘ **Security First**: PII must be masked or tokenized; least privilege must be applied to all service accounts.
- ✘ **No Cryptic Shadows**: Variables like `a`, `tmp`, `val`, or "clever" one-liners that sacrifice clarity for brevity are prohibited.
- ✘ **No Unsafe Deletions**: Never use `rm -rf` without explicit path verification and safeguards.

### Mandatory Patterns (✔)
- ✔ **Idempotency**: All jobs must be safe to rerun/backfill without manual cleanup.
- ✔ **Error Handling**: Fail fast with clear error messages and non-zero exit codes.
- ✔ **Logging & Traceability**: Mandatory correlation/run IDs, record counts, and timing metrics in logs.
- ✔ **Intent-Based Documentation**: Comments must explain the "Why" (business decisions) and not the "How".
- ✔ **Low Cognitive Load**: Functions/modules must be decomposable if they exceed 50 lines. A mid-level dev must grasp logic flow in <30 seconds.
- ✔ **Lineage & Metadata**: Header blocks must define `SOURCE_SYSTEMS`, `TARGET_TABLES`, and `SLA_PRIORITY`.
- ✔ **Externalized Config**: All environment-specific settings (endpoints, paths) must be external to the code.

---

### Preferred Patterns (➜)
- ➜ **Functional Style**: Prefer pure functions and immutability where possible to reduce side effects.
- ➜ **Self-Documenting Code**: Choose descriptive variable names over comments; use comments for "why", not "what".

## 2. Snowflake SQL (DDL/DML/ELT)

### Hard-Stop Rules (✘)
- ✘ **No SELECT ***: Explicitly list columns to ensure performance and schema evolution safety.
- ✘ **No Unintended Fan-outs**: All joins must be deterministic; cross-joins require `/* CROSS JOIN INTENDED */`.
- ✘ **Procedure Injection**: Dynamic SQL in Stored Procedures must use binding variables or `IDENTIFIER()` wrappers.

### Mandatory Patterns (✔)
- ✔ **Watermarking**: Correct handling of late-arriving data and incremental logic (watermarks).
- ✔ **Performance**: Pruning-friendly predicates; large merges must review clustering implications.
- ✔ **Operational Safety**: Audit columns (`load_ts`, `source_file`, `batch_id`) are mandatory for all target tables.
- ✔ **Warehouse Awareness**: Procedures must explicitly set or verify session `WAREHOUSE` context.

> 📖 **Full examples & starter template** → [`templates/snowflake-best-practices.md`](templates/snowflake-best-practices.md)

---

## 3. Python Scripts

### Hard-Stop Rules (✘)
- ✘ **No Memory Overloads**: Never load massive datasets into memory; use chunking or streaming.
- ✘ **No Bare Exceptions**: `try: ... except: pass` is prohibited; catch specific classes only.

### Mandatory Patterns (✔)
- ✔ **Type Hinting**: All function signatures must include Python type hints.
- ✔ **Context Managers**: File I/O and DB connections must use `with` blocks.
- ✔ **Robustness**: Exceptions handled with exponential backoff for transient failures.
- ✔ **Hygiene**: Dependencies pinned; deterministic behavior; consistent formatting (Black/Ruff).

> 📖 **Full examples & starter template** → [`templates/python-best-practices.md`](templates/python-best-practices.md)

---

## 4. Shell Scripts

### Hard-Stop Rules (✘)
- ✘ **No Relative Paths**: All paths for critical files must be anchored using `$(dirname "$0")` or absolute paths.

### Mandatory Patterns (✔)
- ✔ **Strict Mode**: Use `set -euo pipefail` (or equivalent).
- ✔ **Cleanup**: Use `trap` for temporary directory/file cleanup on exit.
- ✔ **Reliability**: Validate required environment variables and command availability before execution.
- ✔ **Local Scoping**: Use `local` keyword for all variables inside functions.

> 📖 **Full examples & starter template** → [`templates/shell-best-practices.md`](templates/shell-best-practices.md)

---

## 5. TWS Scheduling (Job Orchestration)

### Hard-Stop Rules (✘)
- ✘ **No Cyclic Dependencies**: Job graphs must be acyclic.
- ✘ **No Hard-Coded Agents**: Workstations and agents must be parameterized via variable tables.

### Mandatory Patterns (✔)
- ✔ **Concurrency Controls**: Concurrency limits must be set to prevent resource contention.
- ✔ **Alerting**: Notifications and escalations must be configured for failures and SLA warnings.
- ✔ **Operational Health**: Duration-based safeguards must trigger failure if execution time is <5% of usual.

> 📖 **Full examples & starter template** → [`templates/tws-best-practices.md`](templates/tws-best-practices.md)

---

## 6. Databricks Notebooks

### Hard-Stop Rules (✘)
- ✘ **No Manual Dependency**: No reliance on manual cell execution order.
- ✘ **No Driver OOM**: Avoid `collect()` or `toPandas()` on large datasets.

### Mandatory Patterns (✔)
- ✔ **Reproducibility**: Parameterized via widgets or job parameters.
- ✔ **Checkpoints**: Use checkpoints/watermarks for all streaming workloads.
- ✔ **Separation of Concerns**: Shared logic moved to libraries; clear separation of config vs. transformation logic.

> 📖 **Full examples & starter template** → [`templates/databricks-best-practices.md`](templates/databricks-best-practices.md)

---

## Review Output Format

All code reviews produced by this archetype must follow the standardized output template:

> 📖 [`templates/Code_Review.md.template`](templates/Code_Review.md.template)

The template enforces:
- **✘ Hard-Stop Violations** — blocking issues with constitution references and fix-it snippets
- **✔ Quality Improvements** — mandatory patterns that must be addressed before approval
- **➜ Advisory Suggestions** — preferred patterns that improve long-term quality
- **Summary Metrics** — violation counts, files reviewed, lines analyzed
