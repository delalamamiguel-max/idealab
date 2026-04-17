# Python Script Best Practices

> Aligned with **Code Reviewer Constitution §1 (Cross-cutting) & §3 (Python Scripts)**

---

## 1. Script Header Block (Mandatory)

Every Python script must begin with a docstring header establishing lineage, intent, and ownership.

```python
#!/usr/bin/env python3
"""
Script        : load_fact_sales.py
Description   : Extracts daily FACT_SALES delta from Oracle and stages to Snowflake.
Source Systems: Oracle OLTP (PROD)
Target Tables : STG.FACT_SALES_DELTA
SLA Priority  : P1 — must complete by 06:00 UTC
Author        : <team>
Created       : 2026-01-15
"""
```

---

## 2. Type Hinting (✔ Mandatory)

All function signatures must include type hints. Use `typing` module for complex types.

```python
# ✘ BAD — no type information at all
def process_records(records, batch_size):
    ...

# ✔ GOOD — clear contract for callers
from typing import Optional

def process_records(
    records: list[dict[str, str]],
    batch_size: int = 1000,
    dry_run: bool = False,
) -> int:
    """Process records in batches. Returns count of records processed."""
    ...
```

---

## 3. No Bare Exceptions (✘ Hard-Stop)

Catch specific exception classes. Never swallow errors silently.

```python
# ✘ BAD — hides bugs, swallows everything
try:
    result = query_snowflake(sql)
except:
    pass

# ✘ ALSO BAD — too broad, catches KeyboardInterrupt and SystemExit
try:
    result = query_snowflake(sql)
except Exception:
    logger.error("Something went wrong")

# ✔ GOOD — specific, actionable, preserves stack trace
try:
    result = query_snowflake(sql)
except snowflake.connector.errors.ProgrammingError as exc:
    logger.error("SQL execution failed: %s | Query: %s", exc, sql)
    raise
except snowflake.connector.errors.DatabaseError as exc:
    logger.error("Snowflake connection error: %s", exc)
    raise SystemExit(1) from exc
```

---

## 4. Context Managers (✔ Mandatory)

All file I/O, database connections, and network sessions must use `with` blocks.

```python
# ✘ BAD — connection leak if exception occurs before .close()
conn = snowflake.connector.connect(**creds)
cursor = conn.cursor()
cursor.execute(sql)
conn.close()

# ✔ GOOD — guaranteed cleanup
with snowflake.connector.connect(**creds) as conn:
    with conn.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
```

---

## 5. No Memory Overloads (✘ Hard-Stop)

Never load entire large datasets into memory. Use chunking, streaming, or generators.

```python
# ✘ BAD — loads millions of rows into a single list
rows = cursor.fetchall()
df = pd.DataFrame(rows)

# ✔ GOOD — process in chunks
import pandas as pd

CHUNK_SIZE = 50_000

for chunk_df in pd.read_sql(sql, con=engine, chunksize=CHUNK_SIZE):
    transform_and_load(chunk_df)
    logger.info("Processed chunk: %d rows", len(chunk_df))
```

---

## 6. Exponential Backoff for Transient Failures (✔ Mandatory)

Wrap retryable operations with backoff logic. Don't just retry in a tight loop.

```python
import time
from typing import TypeVar, Callable

T = TypeVar("T")


def retry_with_backoff(
    func: Callable[..., T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0,
) -> T:
    """Retry a callable with exponential backoff on transient failures."""
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except (ConnectionError, TimeoutError) as exc:
            if attempt == max_retries:
                raise
            delay = base_delay * (backoff_factor ** (attempt - 1))
            logger.warning(
                "Attempt %d/%d failed: %s. Retrying in %.1fs...",
                attempt, max_retries, exc, delay,
            )
            time.sleep(delay)
    raise RuntimeError("Unreachable")  # satisfies type checker
```

---

## 7. Logging & Traceability (✔ Mandatory)

Use `logging` module with structured fields — never bare `print()` for operational output.

```python
import logging
import uuid

RUN_ID = str(uuid.uuid4())[:8]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(run_id)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
logger = logging.getLogger(__name__)

# Inject run_id into every log record
old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.run_id = RUN_ID
    return record

logging.setLogRecordFactory(record_factory)

logger.info("Starting FACT_SALES extraction | source=oracle_oltp | target=stg.fact_sales_delta")
```

---

## 8. No Hardcoded Secrets (✘ Hard-Stop)

Credentials must come from environment variables, secret managers, or config files excluded from version control.

```python
# ✘ BAD
SNOWFLAKE_PASSWORD = "SuperSecret123"

# ✔ GOOD — from environment
import os

SNOWFLAKE_PASSWORD = os.environ["SNOWFLAKE_PASSWORD"]

# ✔ ALSO GOOD — from a secrets manager
from your_infra_lib import secrets_manager

SNOWFLAKE_PASSWORD = secrets_manager.get("snowflake/prod/password")
```

---

## 9. Externalized Configuration (✔ Mandatory)

Environment-specific values must live outside the code.

```python
# ✘ BAD — environment baked into logic
SNOWFLAKE_ACCOUNT = "xy12345.us-east-1"

# ✔ GOOD — externalized via .env, YAML, or env vars
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    """Immutable application configuration loaded from environment."""
    snowflake_account: str
    snowflake_warehouse: str
    snowflake_database: str
    snowflake_schema: str
    batch_size: int = 50_000

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            snowflake_account=os.environ["SNOWFLAKE_ACCOUNT"],
            snowflake_warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
            snowflake_database=os.environ["SNOWFLAKE_DATABASE"],
            snowflake_schema=os.environ["SNOWFLAKE_SCHEMA"],
            batch_size=int(os.environ.get("BATCH_SIZE", "50000")),
        )

config = AppConfig.from_env()
```

---

## 10. Idempotency (✔ Mandatory)

Scripts must be safe to rerun without creating duplicates.

```python
def upsert_records(
    engine,
    records: list[dict],
    target_table: str,
    key_columns: list[str],
) -> int:
    """Idempotent upsert using MERGE semantics.

    Why: Reruns after partial failure must not duplicate data.
    """
    merge_sql = f"""
        MERGE INTO {target_table} AS tgt
        USING (SELECT * FROM @~/staged_data) AS src
        ON {' AND '.join(f'tgt.{k} = src.{k}' for k in key_columns)}
        WHEN MATCHED THEN UPDATE SET ...
        WHEN NOT MATCHED THEN INSERT ...
    """
    with engine.begin() as conn:
        result = conn.execute(merge_sql)
    return result.rowcount
```

---

## 11. Code Hygiene (✔ Mandatory)

- Pin all dependencies in `requirements.txt` or `pyproject.toml`.
- Format with **Black** or **Ruff**.
- Lint with **Ruff** (replaces flake8, isort, pyflakes).

```toml
# pyproject.toml
[tool.ruff]
line-length = 120
target-version = "py311"
select = ["E", "F", "W", "I", "N", "UP", "S", "B", "A", "C4", "SIM"]

[tool.black]
line-length = 120
target-version = ["py311"]
```

---

## 12. Low Cognitive Load (✔ Mandatory)

Functions exceeding 50 lines must be decomposed. A mid-level dev should grok the flow in under 30 seconds.

```python
# ✘ BAD — monolithic 200-line function
def run_pipeline():
    # ... 200 lines of mixed concerns ...

# ✔ GOOD — composed of small, testable units
def run_pipeline(config: AppConfig) -> None:
    """Orchestrate the full ETL pipeline."""
    raw_data = extract_from_source(config)
    validated = validate_schema(raw_data)
    transformed = apply_business_rules(validated)
    load_to_target(transformed, config)
    log_completion_metrics(config)
```

---

## 13. Full Template

```python
#!/usr/bin/env python3
"""
Script        : example_etl.py
Description   : Template Python script adhering to code-reviewer constitution.
Source Systems: <source>
Target Tables : <target>
SLA Priority  : P2
Author        : <team>
Created       : 2026-02-19
"""
import logging
import os
import sys
import time
import uuid
from dataclasses import dataclass
from typing import Any

# ── Configuration ─────────────────────────────────────────────

RUN_ID = str(uuid.uuid4())[:8]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [run:%(run_id)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
logger = logging.getLogger(__name__)

_old_factory = logging.getLogRecordFactory()
def _record_factory(*args: Any, **kwargs: Any) -> logging.LogRecord:
    record = _old_factory(*args, **kwargs)
    record.run_id = RUN_ID  # type: ignore[attr-defined]
    return record
logging.setLogRecordFactory(_record_factory)


@dataclass(frozen=True)
class AppConfig:
    """Immutable app config from environment variables."""
    source_dsn: str
    target_table: str
    batch_size: int = 50_000

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            source_dsn=os.environ["SOURCE_DSN"],
            target_table=os.environ["TARGET_TABLE"],
            batch_size=int(os.environ.get("BATCH_SIZE", "50000")),
        )


# ── Core Functions ────────────────────────────────────────────

def extract(config: AppConfig) -> list[dict[str, Any]]:
    """Extract data from source system."""
    logger.info("Extracting from %s", config.source_dsn)
    # TODO: implement extraction with chunking
    return []


def transform(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Apply business rules to extracted records."""
    logger.info("Transforming %d records", len(records))
    return records


def load(records: list[dict[str, Any]], config: AppConfig) -> int:
    """Load transformed records into target (idempotent via MERGE)."""
    logger.info("Loading %d records into %s", len(records), config.target_table)
    return len(records)


# ── Entrypoint ────────────────────────────────────────────────

def main() -> None:
    """Orchestrate the ETL pipeline."""
    start = time.monotonic()
    config = AppConfig.from_env()
    logger.info("Pipeline started | run_id=%s", RUN_ID)

    raw = extract(config)
    transformed = transform(raw)
    count = load(transformed, config)

    elapsed = time.monotonic() - start
    logger.info("Pipeline complete | records=%d | elapsed=%.2fs", count, elapsed)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        sys.exit(130)
    except Exception:
        logger.exception("Pipeline failed")
        sys.exit(1)
```
