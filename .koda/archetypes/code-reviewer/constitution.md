# Code Reviewer Constitution

## Mission Statement
Establish a AI assisted, consistent code and peer review practice that improves correctness, security, performance, and maintainability—so every change is understandable, testable, and safe to operate in production.

This constitution defines the mandatory architectural and quality standards. Any code generated or modified must be cross-referenced against these rules.

## 1. Cross-cutting (Applies to everything)

### Hard-Stop Rules (✘)
- ✘ **No Hardcoded Secrets**: Never embed credentials, API keys, or tokens in code or logs.
- ✘ **No Data Corruption Risk**: Reruns must be idempotent and never lead to duplicate or corrupt data.
- ✘ **Security First**: PII must be masked or tokenized; least privilege must be applied to all service accounts.

### Mandatory Patterns (✔)
- ✔ **Error Handling**: Fail fast with clear error messages and non-zero exit codes.
- ✔ **Logging**: Sufficient logs/metrics with correlation/run IDs for troubleshooting.
- ✔ **Idempotency**: All jobs must be safe to rerun without manual cleanup.
- ✔ **Externalized Config**: All environment-specific settings must be external to the code.

## 2. Snowflake SQL (DDL/DML/ELT)

### Hard-Stop Rules (✘)
- ✘ **No Unintended Fan-outs**: Joins and filters must be deterministic and verified.
- ✘ **No SELECT ***: Explicitly list columns to ensure performance and schema evolution safety.

### Mandatory Patterns (✔)
- ✔ **Correctness**: explicit null handling and data typing.
- ✔ **Performance**: predicates must be pruning-friendly.
- ✔ **Operational Safety**: Transactions used where appropriate; Audit columns `load_ts`, `source_file`, `batch_id` included.

## 3. Python Scripts

### Hard-Stop Rules (✘)
- ✘ **No Memory Overloads**: Never load massive datasets entirely into memory; use chunking or streaming.

### Mandatory Patterns (✔)
- ✔ **Robustness**: Exceptions handled with backoff for transient failures.
- ✔ **Hygiene**: Dependencies pinned; deterministic behavior.
- ✔ **Tests**: Unit tests for transformations and mocks for external calls.

## 4. Shell Scripts

### Hard-Stop Rules (✘)
- ✘ **No Unsafe Deletions**: Never use `rm -rf` without explicit path verification and safeguards.

### Mandatory Patterns (✔)
- ✔ **Safety**: `set -euo pipefail` (or equivalent) must be used.
- ✔ **Reliability**: Validate required env vars and check command availability.

## 5. TWS Scheduling

### Hard-Stop Rules (✘)
- ✘ **No Cyclic Dependencies**: Job graphs must be acyclic.

### Mandatory Patterns (✔)
- ✔ **Operational Controls**: Rerun and backfill procedures must be documented.
- ✔ **Scheduling**: Calendars and time zones validated.

## 6. Databricks Notebooks

### Hard-Stop Rules (✘)
- ✘ **No Manual Dependency**: No reliance on manual cell execution order.

### Mandatory Patterns (✔)
- ✔ **Reproducibility**: Parameterized via widgets or job parameters.
- ✔ **Hygiene**: Shared logic moved to libraries; clear separation of config vs logic.
