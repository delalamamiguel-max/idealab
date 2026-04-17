# TWS (Tivoli Workload Scheduler) Best Practices

> Aligned with **Code Reviewer Constitution §1 (Cross-cutting) & §5 (TWS Scheduling)**

---

## 1. Job Definition Header Block (Mandatory)

Every job definition must include a metadata block that documents lineage, SLA, and ownership.

```
# ──────────────────────────────────────────────────────────────
# JOB STREAM      : JS_LOAD_FACT_SALES
# DESCRIPTION     : Orchestrates nightly FACT_SALES incremental load
# SOURCE_SYSTEMS  : Oracle OLTP (PROD) → Snowflake STG
# TARGET_TABLES   : CORE.FACT_SALES
# SLA_PRIORITY    : P1 — must complete by 06:00 UTC
# OWNER           : <team>@company.com
# CREATED         : 2026-01-15
# ──────────────────────────────────────────────────────────────
```

---

## 2. No Cyclic Dependencies (✘ Hard-Stop)

Job graphs must be strictly **Directed Acyclic Graphs (DAGs)**. Circular dependencies cause deadlocks and are undetectable at runtime.

```
✘ BAD — circular dependency (deadlock)
JOB_A → JOB_B → JOB_C → JOB_A

✔ GOOD — clean DAG
JS_EXTRACT
  ├── JOB_EXTRACT_ORACLE
  └── JOB_EXTRACT_S3
        ↓
JS_TRANSFORM
  └── JOB_MERGE_STAGING
        ↓
JS_LOAD
  └── JOB_LOAD_FACT_SALES
        ↓
JS_VALIDATE
  └── JOB_ROW_COUNT_CHECK
```

**Validation**: Before promoting any job stream, render the dependency graph and confirm it's acyclic. Use `conman` or `planman` validation exports to verify.

---

## 3. No Hard-Coded Agents/Workstations (✘ Hard-Stop)

Agents and workstations must be parameterized via TWS variable tables — never hard-coded into job definitions.

```
# ✘ BAD — breaks if agent name changes or migrates
JSDL:
  SCRIPTNAME: /opt/etl/load.ksh
  AGENT: PROD_AGENT_01

# ✔ GOOD — references a variable table entry
JSDL:
  SCRIPTNAME: /opt/etl/load.ksh
  AGENT: &ETL_AGENT_PRIMARY.
```

**Variable Table Definition:**
```
VARTABLE: VT_ETL_CONFIG
  ETL_AGENT_PRIMARY  = "PROD_AGENT_01"
  ETL_AGENT_FAILOVER = "PROD_AGENT_02"
  ETL_WH_SIZE        = "LARGE"
```

---

## 4. Concurrency Controls (✔ Mandatory)

Set explicit concurrency limits to prevent resource contention, especially for jobs hitting the same warehouse or database.

```
# ✔ GOOD — resource-level mutual exclusion
RESOURCE: RES_SNOWFLAKE_ETL_WH
  QUANTITY: 3          # Max 3 concurrent jobs on this warehouse
  USAGE: EXCLUSIVE     # Or SHARED depending on pattern

JOB: JOB_LOAD_FACT_SALES
  NEEDS: RES_SNOWFLAKE_ETL_WH(1)
```

**Why**: Without concurrency limits, parallel jobs can starve the warehouse, cause queue pileups, or trigger Snowflake auto-suspend at the worst possible time.

---

## 5. Alerting & Escalation (✔ Mandatory)

Every job stream must have failure notifications AND SLA-breach warnings configured. No silent failures.

```
# ✔ GOOD — alert on failure
JOB: JOB_LOAD_FACT_SALES
  ON_FAILURE:
    NOTIFY: etl-oncall@company.com
    SEVERITY: CRITICAL
    MESSAGE: "FACT_SALES load failed — batch_id: &BATCH_ID. | Check logs at /var/log/etl/"

# ✔ GOOD — SLA warning before breach
JOB_STREAM: JS_LOAD_FACT_SALES
  SLA_DEADLINE: 06:00 UTC
  SLA_WARNING:  05:30 UTC    # 30-minute early warning
  ON_SLA_WARNING:
    NOTIFY: etl-oncall@company.com
    MESSAGE: "WARNING: JS_LOAD_FACT_SALES approaching SLA deadline (06:00 UTC)"
  ON_SLA_BREACH:
    NOTIFY: etl-oncall@company.com, etl-manager@company.com
    SEVERITY: CRITICAL
    ESCALATION: PAGE
```

---

## 6. Duration-Based Safeguards (✔ Mandatory)

If a job completes in less than 5% of its usual duration, it probably did nothing (empty source, skipped logic, misconfigured env). Trigger a failure, not a success.

```
# ✔ GOOD — detect suspiciously fast runs
JOB: JOB_LOAD_FACT_SALES
  EXPECTED_DURATION: 45m
  MIN_DURATION: 2m           # 5% of 45m ≈ 2.25m
  ON_MIN_DURATION_BREACH:
    ACTION: FAIL
    MESSAGE: "Job completed in < 2 min (expected ~45 min). Likely no-op or misconfiguration."

  MAX_DURATION: 120m         # 2.6x expected = something is stuck
  ON_MAX_DURATION_BREACH:
    ACTION: KILL_AND_FAIL
    NOTIFY: etl-oncall@company.com
    MESSAGE: "Job exceeded 120 min (expected ~45 min). Killed."
```

---

## 7. Idempotent Job Design (✔ Mandatory)

Jobs must be safe to rerun. This means the scripts they invoke are idempotent, and the TWS definition supports restart.

```
# ✔ GOOD — restartable job with recovery action
JOB: JOB_LOAD_FACT_SALES
  RECOVERY:
    ACTION: RERUN          # Safe because the underlying MERGE is idempotent
    MAX_RERUN: 2
    RERUN_DELAY: 5m
```

**Why**: If a job fails due to a transient issue (network blip, warehouse auto-suspend), TWS should be able to rerun it without human intervention and without creating duplicate data.

---

## 8. Externalized Configuration (✔ Mandatory)

Environment-specific settings (paths, warehouse names, credentials references) must come from variable tables, not job definitions.

```
# ✔ GOOD — all env-specific values parameterized
VARTABLE: VT_PROD
  SNOWFLAKE_ACCOUNT     = "xy12345.us-east-1"
  SNOWFLAKE_WAREHOUSE   = "ETL_WH_LARGE"
  ETL_SCRIPT_DIR        = "/opt/etl/prod/scripts"
  LOG_DIR               = "/var/log/etl/prod"
  BATCH_ID_PREFIX       = "PROD"

VARTABLE: VT_UAT
  SNOWFLAKE_ACCOUNT     = "xy12345.us-east-1"
  SNOWFLAKE_WAREHOUSE   = "ETL_WH_SMALL"
  ETL_SCRIPT_DIR        = "/opt/etl/uat/scripts"
  LOG_DIR               = "/var/log/etl/uat"
  BATCH_ID_PREFIX       = "UAT"
```

---

## 9. Logging from TWS Jobs (✔ Mandatory)

Job output must be captured, timestamped, and tied to run metadata.

```
JOB: JOB_LOAD_FACT_SALES
  SCRIPTNAME: &ETL_SCRIPT_DIR./load_fact_sales.ksh
  STDOUTPUT:  &LOG_DIR./JOB_LOAD_FACT_SALES_&ODATE._&SCHEDTIME..log
  STDERROR:   &LOG_DIR./JOB_LOAD_FACT_SALES_&ODATE._&SCHEDTIME..err
```

**Why**: Without captured logs, debugging a 3 AM failure becomes archaeology instead of engineering.

---

## 10. Dependency Best Practices (✔ Mandatory)

Use file-based or status-based dependencies, not time-based waits.

```
# ✘ BAD — time-based wait (brittle, wastes time or causes races)
JOB: JOB_LOAD_FACT_SALES
  START_TIME: 04:00 UTC    # "Oracle extract is usually done by then"

# ✔ GOOD — explicit predecessor dependency
JOB: JOB_LOAD_FACT_SALES
  FOLLOWS: JOB_EXTRACT_ORACLE(SUCCESS)

# ✔ ALSO GOOD — file-based trigger
JOB: JOB_LOAD_FACT_SALES
  OPENS: /data/triggers/oracle_extract_complete.flag
```

---

## 11. Full Template

```
# ──────────────────────────────────────────────────────────────
# JOB STREAM      : JS_EXAMPLE_ETL
# DESCRIPTION     : Template TWS job stream adhering to code-reviewer constitution
# SOURCE_SYSTEMS  : <source>
# TARGET_TABLES   : <target>
# SLA_PRIORITY    : P2
# OWNER           : <team>@company.com
# CREATED         : 2026-02-19
# ──────────────────────────────────────────────────────────────

# ── Variable Table ────────────────────────────────────────────
VARTABLE: VT_EXAMPLE_CONFIG
  ETL_AGENT        = "PROD_AGENT_01"
  ETL_SCRIPT_DIR   = "/opt/etl/prod/scripts"
  LOG_DIR          = "/var/log/etl/prod"
  SF_WAREHOUSE     = "ETL_WH_MEDIUM"

# ── Resources ────────────────────────────────────────────────
RESOURCE: RES_SF_ETL_WH
  QUANTITY: 3

# ── Job Stream ───────────────────────────────────────────────
JOB_STREAM: JS_EXAMPLE_ETL
  SLA_DEADLINE: 06:00 UTC
  SLA_WARNING:  05:30 UTC
  ON_SLA_BREACH:
    NOTIFY: etl-oncall@company.com
    SEVERITY: CRITICAL

# ── Step 1: Extract ──────────────────────────────────────────
JOB: JOB_EXTRACT
  AGENT: &ETL_AGENT.
  SCRIPTNAME: &ETL_SCRIPT_DIR./extract.ksh
  STDOUTPUT:  &LOG_DIR./JOB_EXTRACT_&ODATE..log
  STDERROR:   &LOG_DIR./JOB_EXTRACT_&ODATE..err
  NEEDS: RES_SF_ETL_WH(1)
  EXPECTED_DURATION: 15m
  MIN_DURATION: 1m
  ON_FAILURE:
    NOTIFY: etl-oncall@company.com

# ── Step 2: Transform & Load ─────────────────────────────────
JOB: JOB_TRANSFORM_LOAD
  AGENT: &ETL_AGENT.
  FOLLOWS: JOB_EXTRACT(SUCCESS)
  SCRIPTNAME: &ETL_SCRIPT_DIR./transform_and_load.ksh
  STDOUTPUT:  &LOG_DIR./JOB_TRANSFORM_LOAD_&ODATE..log
  STDERROR:   &LOG_DIR./JOB_TRANSFORM_LOAD_&ODATE..err
  NEEDS: RES_SF_ETL_WH(1)
  EXPECTED_DURATION: 45m
  MIN_DURATION: 2m
  MAX_DURATION: 120m
  RECOVERY:
    ACTION: RERUN
    MAX_RERUN: 2
    RERUN_DELAY: 5m
  ON_FAILURE:
    NOTIFY: etl-oncall@company.com
    SEVERITY: CRITICAL

# ── Step 3: Validate ─────────────────────────────────────────
JOB: JOB_VALIDATE
  AGENT: &ETL_AGENT.
  FOLLOWS: JOB_TRANSFORM_LOAD(SUCCESS)
  SCRIPTNAME: &ETL_SCRIPT_DIR./validate_row_counts.ksh
  STDOUTPUT:  &LOG_DIR./JOB_VALIDATE_&ODATE..log
  ON_FAILURE:
    NOTIFY: etl-oncall@company.com
```
