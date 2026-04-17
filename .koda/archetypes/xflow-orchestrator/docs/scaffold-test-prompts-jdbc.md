# XFlow Orchestrator — 16 JDBC Source Test Prompts

Generated from scanning **6,268 JDBC production configs** across the enterprise data lake.

---

## S-01o — JDBC with bind parameters (5,302 configs — 34.7%)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/order_extract_incremental.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-opusc-jdbc
- SQL has bind parameters:
  - Parameter 1 (FETCH_ON_NULL): "select TO_CHAR(TO_DATE(SUBSTR(MAX(BATCH_ID),1,8),'YYYYMMDD') - INTERVAL '1' DAY,'yyyymmdd') AS RESULT1 FROM BPMRD.ORDER_BATCH_LOG WHERE lower(TABLE_NAME)='orders'", saveValueFromIndex: 2
  - Parameter 2 (FETCH_ALWAYS): "select MAX(BATCH_ID) AS RESULT2 FROM BPMRD.ORDER_BATCH_LOG WHERE lower(TABLE_NAME)='orders'"

**Schema**
- order_id string
- customer_id string
- order_date string
- order_amount decimal(19,2)
- status string
- batch_id string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/order_extract_incremental
- Format: Parquet
- Write mode: append
- Retain source files for 7 days

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 4:30 PM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_order_extract_incremental
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 25048
```

---

## S-01b — JDBC Oracle → Parquet, no transforms, partitioned (2,448 configs)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/agency_master.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-opusc-jdbc
- No SQL bind parameters

**Schema**
- agency_id string
- agency_name string
- agency_type string
- region string
- status string
- create_date timestamp
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/agency_master
- Format: Parquet
- Write mode: append

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 6:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_agency_master
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: FIN-103
- Mots ID: 25048
```

---

## S-01a — JDBC Oracle → CSV, no transforms, partitioned (1,969 configs)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/shipment_details.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-bpmrd-jdbc
- No SQL bind parameters

**Schema**
- shipment_id string
- order_id string
- carrier_code string
- tracking_number string
- ship_date string
- status string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/shipment_details
- Format: CSV
- Write mode: append
- CSV target properties: separator=|

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 5:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_shipment_details
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 30200
```

---

## S-01c — JDBC Oracle → Parquet + globalTransform, partitioned (1,009 configs)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/message_queue.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-bpmrd-jdbc
- No SQL bind parameters

**Schema**
- msg_id string
- msg_type string
- msg_body string
- priority string
- create_ts string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/message_queue
- Format: Parquet
- Write mode: append

**Global transformation:**
- Replace "", "NULL" with Null

**No transformations, no validations, no error handling overrides.**

**Schedule:** daily at 7:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_message_queue
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 19062
```

---

## S-01p — JDBC without partitions (160 configs)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/transaction_status_vl.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-opusc-jdbc
- No SQL bind parameters

**Schema**
- status_code string
- status_desc string
- category string
- active_ind string

No partitions (small lookup table).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/transaction_status_vl
- Format: Parquet
- Write mode: overwrite

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 4:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_transaction_status_vl
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: FIN-103
- Mots ID: 25048
```

---

## S-01d — JDBC Oracle → CSV + globalTransform, partitioned (142 configs)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/sdrs_console.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-bpmrd-jdbc
- No SQL bind parameters

**Schema**
- console_id string
- console_name string
- region string
- status string
- last_update string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/sdrs_console
- Format: CSV
- Write mode: append
- CSV target properties: separator=|

**Global transformation:**
- Replace "", "NULL", "null" with Null

**No transformations, no validations, no error handling overrides.**

**Schedule:** daily at 8:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_sdrs_console
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 22100
```

---

## S-01e — JDBC Oracle → CSV with transforms, partitioned (95 configs)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/incident_master.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-bpmrd-jdbc
- No SQL bind parameters

**Schema**
- inc_id string
- inc_type string
- priority string
- create_date string
- resolve_date string
- status string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/incident_master
- Format: CSV
- Write mode: append
- CSV target properties: separator=|

**Transformations:**
- Add LOAD_TS column: generated value SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**No validations, no global transform, no error handling overrides.**

**Schedule:** daily at 6:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_incident_master
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 19500
```

---

## S-01f — JDBC Oracle → CSV + GT + errorHandling (66 configs)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/port_request.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-tlgmob
- No SQL bind parameters

**Schema**
- request_id string
- ctn string
- port_type string
- status string
- create_date string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/port_request
- Format: CSV
- Write mode: append
- CSV target properties: separator=|

**Transformations:**
- Add LOAD_TS column: generated value SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**Global transformation:**
- Trim spaces
- Replace "", "NULL", "null" with Null

**Error handling:**
- Standard: fail on error, skip malformed, bad file

**No validations.**

**Schedule:** daily at 5:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_port_request
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: CUST-100
- Mots ID: 19500
```

---

## S-01j — JDBC Snowflake → Delta (48 configs)

```
/scaffold-xflow-orchestrator

- Source: Snowflake database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/sf_customer_segments.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-snowflake-bpmrd
- Snowflake-specific:
  - Database: ANALYTICS_DB
  - Schema: PUBLIC
  - Warehouse: COMPUTE_WH
- No SQL bind parameters

**Schema**
- customer_id string
- segment_name string
- segment_score decimal(10,4)
- assigned_date string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/sf_customer_segments
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** weekly on Mondays at 6:00 AM UTC (0 0 6 ? * MON)

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_sf_customer_segments
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: CUST-100
- Mots ID: 32000
```

---

## S-01k — JDBC SQL Server → Delta (22 configs)

```
/scaffold-xflow-orchestrator

- Source: SQL Server database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/ss_ticket_master.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-sqlserver-bpmrd
- No SQL bind parameters

**Schema**
- ticket_id string
- ticket_type string
- priority string
- assigned_to string
- status string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/ss_ticket_master
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 7:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_ss_ticket_master
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 22538
```

---

## S-01l — JDBC Vertica → Delta (18 configs)

```
/scaffold-xflow-orchestrator

- Source: Vertica database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/vt_ipbb_swimlane.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-vertica-bpmrd
- No SQL bind parameters

**Schema**
- swimlane_id string
- from_state string
- to_state string
- transition_count long
- report_date string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/vt_ipbb_swimlane
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 8:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_vt_ipbb_swimlane
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 24169
```

---

## S-01m — JDBC MySQL → Delta (12 configs)

```
/scaffold-xflow-orchestrator

- Source: MySQL database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/my_app_config.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-mysql-bpmrd
- No SQL bind parameters

**Schema**
- config_id string
- config_key string
- config_value string
- env string
- last_modified string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/my_app_config
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 6:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_my_app_config
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-Wrkf
- Rim Policy: NET-300
- Mots ID: 30636
```

---

## S-01i — JDBC Teradata → Parquet, no transforms, partitioned (5 configs)

```
/scaffold-xflow-orchestrator

- Source: Teradata database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/td_account_summary.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-teradata-bpmrd
- No SQL bind parameters

**Schema**
- account_id string
- account_type string
- balance decimal(15,2)
- open_date string
- region_code string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/td_account_summary
- Format: Parquet
- Write mode: append

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 4:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_td_account_summary
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: FIN-103
- Mots ID: 16000
```

---

## S-01n — JDBC Oracle → Delta, partitioned (3 configs)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/network_pod_ran.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-bpmrd-jdbc
- No SQL bind parameters

**Schema**
- pod_id string
- ran_id string
- site_name string
- latitude double
- longitude double
- market_code string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/network_pod_ran
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 6:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_network_pod_ran
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 18200
```

---

## S-01g — JDBC Oracle → Delta, overwritePartition (2 configs)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/bpmrd/sim_swap_daily.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-bpmrd-jdbc
- No SQL bind parameters

**Schema**
- calendardate string
- sim_changes_cnt string
- failed_cnt string
- success_cnt string
- avg_remediate_time string

Partition by calendardate.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/sim_swap_daily
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: overwritePartition

**Transformations:**
- calendardate: dateFormat conversion, source format "yyyy-MM-dd", target format "yyyy-MM-dd"

**No validations, no global transform, no error handling overrides.**

**Schedule:** daily at 2:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_sim_swap_daily
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: CricketNonDoxOperations@amdocs.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: NET-300
- Mots ID: 22538
```

---

## API Test Results

**All 16 JDBC scenarios: 16/16 CREATED ✅ (100% first-attempt pass rate)**

| ID | Config | configId | srcId |
|----|--------|----------|-------|
| S-01o | S01o_jdbc_bind_parameters.json | 124599 | STG_JDBC_order_extract_incremental |
| S-01b | S01b_jdbc_oracle_parquet_partitioned.json | 124600 | STG_JDBC_agency_master |
| S-01a | S01a_jdbc_oracle_csv_partitioned.json | 124601 | STG_JDBC_shipment_details |
| S-01c | S01c_jdbc_oracle_parquet_gt.json | 124602 | STG_JDBC_message_queue |
| S-01p | S01p_jdbc_oracle_no_partitions.json | 124603 | STG_JDBC_transaction_status_vl |
| S-01d | S01d_jdbc_oracle_csv_gt.json | 124604 | STG_JDBC_sdrs_console |
| S-01e | S01e_jdbc_oracle_csv_transforms.json | 124605 | STG_JDBC_incident_master |
| S-01f | S01f_jdbc_oracle_csv_gt_eh.json | 124606 | STG_JDBC_port_request |
| S-01j | S01j_jdbc_snowflake_delta.json | 124607 | STG_JDBC_sf_customer_segments |
| S-01k | S01k_jdbc_sqlserver_delta.json | 124608 | STG_JDBC_ss_ticket_master |
| S-01l | S01l_jdbc_vertica_delta.json | 124609 | STG_JDBC_vt_ipbb_swimlane |
| S-01m | S01m_jdbc_mysql_delta.json | 124610 | STG_JDBC_my_app_config |
| S-01i | S01i_jdbc_teradata_parquet.json | 124611 | STG_JDBC_td_account_summary |
| S-01n | S01n_jdbc_oracle_delta_partitioned.json | 124612 | STG_JDBC_network_pod_ran |
| S-01g | S01g_jdbc_oracle_delta_owp.json | 124613 | STG_JDBC_sim_swap_daily |

## Coverage Matrix

| ID | Connection | Target | WriteMode | TX | GT | EH | Partitions | Bind Params |
|----|-----------|--------|-----------|----|----|-----|-----------|-------------|
| S-01o | Oracle | Parquet | append | - | - | - | ✓ | ✓ (2 params) |
| S-01b | Oracle | Parquet | append | - | - | - | ✓ | - |
| S-01a | Oracle | CSV | append | - | - | - | ✓ | - |
| S-01c | Oracle | Parquet | append | - | replaceValues | - | ✓ | - |
| S-01p | Oracle | Parquet | overwrite | - | - | - | - | - |
| S-01d | Oracle | CSV | append | - | replaceValues | - | ✓ | - |
| S-01e | Oracle | CSV | append | dateFormat | - | - | ✓ | - |
| S-01f | Oracle | CSV | append | dateFormat | trim+replace | Standard | ✓ | - |
| S-01j | Snowflake | Delta/UC | append | - | - | - | ✓ | - |
| S-01k | SQL Server | Delta/UC | append | - | - | - | ✓ | - |
| S-01l | Vertica | Delta/UC | append | - | - | - | ✓ | - |
| S-01m | MySQL | Delta/UC | append | - | - | - | ✓ | - |
| S-01i | Teradata | Parquet | append | - | - | - | ✓ | - |
| S-01n | Oracle | Delta/UC | append | - | - | - | ✓ | - |
| S-01g | Oracle | Delta/UC | OWP | dateFormat | - | - | ✓ | - |
