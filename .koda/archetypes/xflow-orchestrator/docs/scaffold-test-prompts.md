# XFlow Orchestrator — 28 Scaffold Test Prompts

Generated from scanning **15,284 production configs** across 94 application directories.

Each prompt is a self-contained `/scaffold-xflow-orchestrator` invocation. Prompts are ordered by production frequency.

---

## P01 — JDBC Oracle → Parquet, partitioned, no transforms (24.2% of production)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/opusc/agency_fan_details.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-opusc-jdbc
- No SQL bind parameters

**Schema**
- agency_fan_detail_id string
- session_id string
- location_account_id string
- agency_name string
- street_address string
- city string
- state string
- zip string
- fan_type string
- fan_creation_date timestamp
- dealer_code1 string
- source_system string
- ggs_commit_ts string
- ggs_op_type string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://opus-stg@datalakeeastus2prd.dfs.core.windows.net/agency_fan_details
- Format: Parquet
- Write mode: append
- Schedule: daily at 4:30 PM UTC

**No transformations, no validations, no global transform, no error handling overrides.**

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_agency_fan_details
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: dtvsupportcenter@directv.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: FIN-103
- Mots ID: 25048
```

---

## P02 — File (ADLS) → legacy (no target format), partitioned (15.6%)

```
/scaffold-xflow-orchestrator

- Source: ADLS file (already landed)
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/tech_order_data_prestg
- Source file format: fixed-width
- Fixed-width column widths: 10, 20, 15, 8, 12, 30, 6

**Schema**
- order_id string
- order_type string
- tech_id string
- order_dt string
- region_cd string
- description string
- status string

Partition by order_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/tech_order_data
- Format: Parquet
- Retain source files for 7 days

**No transformations, no validations, no global transform, no error handling.**

**Metadata**
- Application: bpmrd
- Feed name: tech_order_data
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 18500
```

---

## P03 — JDBC Oracle → CSV, partitioned, no transforms (12.9%)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/yoda/df_shipment.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-yoda
- No SQL bind parameters

**Schema**
- shipment_id string
- order_id string
- carrier_code string
- tracking_number string
- ship_date string
- delivery_date string
- shipment_status string
- warehouse_id string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://yoda-stg@datalakeeastus2prd.dfs.core.windows.net/df_shipment
- Format: CSV
- CSV target properties: separator=|

**Schedule:** daily at 6:00 AM UTC

**No transformations, no validations, no global transform, no error handling.**

**Metadata**
- Application: bpmrd
- Feed name: yoda_df_shipment
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 30200
```

---

## P04 — DataRouter → CSV, append, transforms, partitioned (7.7%)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/sunrs_store_dly_sls_dtl_prestg
- Subscriber ID: 277
- Feed ID: ecdwsunrisetax360
- File filter regex: ^txcrdt_trfcnt_extract_mly_.*$
- Duplicate file check: Yes
- Source file format: CSV (pipe-delimited)
- File has header (1 line) and trailer (1 line)
- Need record count validation from trailer

**Schema**
- ACTVT_DT string
- STORE_LOC_ID string
- OPUS_ID string
- STORE_LOC_NM string
- ADDR_LN_1_TXT string
- CTY_NM string
- ST_CD string
- ZIP_CD string
- ACTVTN_MRC_AMT decimal(19,4)
- UPGRD_MRC_AMT decimal(19,4)
- TRFC_OUT_CNT decimal(19,4)
- TRFC_IN_CNT decimal(19,4)

Partition by load_dt using SYSDATE (yyyyMMdd format).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/sunrs_store_dly_sls_dtl
- Format: CSV
- Write mode: append
- CSV target properties: separator=|

**Transformations:**
- Add LOAD_TS column: generated value SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**No validations, no global transform, no error handling.**

**Schedule:** every hour

**Metadata**
- Application: bpmrd
- Feed name: STG_sunrs_store_dly_sls_dtl
- Feed type: ING
- Support team: ECDW
- Created by: us2472@att.com
- Contact: lg9762@att.com
- Data Library: DP DataLibrary-Finance
- Rim Policy: NET-300
- Mots ID: 24169
```

---

## P05 — DataRouter → Parquet, append, no transforms, partitioned (6.9%)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/srv_ord_prod_itm_prestg
- Subscriber ID: 150
- Feed ID: oms
- File filter regex: ^oms_srv_ord_prod_itm_.*\.dat$
- Duplicate file check: No
- Source file format: Parquet

**Schema**
- srv_ord_id string
- prod_itm_id string
- itm_desc string
- qty long
- unit_price decimal(19,2)
- total_price decimal(19,2)
- status_cd string
- create_dt string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/srv_ord_prod_itm
- Format: Parquet
- Write mode: append
- Retain source files for 7 days

**No transformations, no validations, no global transform, no error handling.**

**Schedule:** every 2 hours (0 0 0/2 * * ?)

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_oms_srv_ord_prod_itm_src
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 19062
```

---

## P06 — JDBC Oracle → Parquet + globalTransform (6.6%)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/scoop/hardwarematrix.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-scoop
- No SQL bind parameters

**Schema**
- hw_matrix_id string
- hw_model string
- manufacturer string
- hw_category string
- compatible_os string
- eol_date string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://scoop-stg@datalakeeastus2prd.dfs.core.windows.net/hardwarematrix
- Format: Parquet
- Write mode: append

**Global transformation:**
- Replace "", "NULL" with Null

**No transformations, no validations, no error handling.**

**Schedule:** daily at 5:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_scoop_hardwarematrix
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 22100
```

---

## P07 — Kafka → CSV + transforms + globalTransform, append, partitioned (2.0%)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667,dicore-prod-01-gg-kafka2.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: GIOM.IOMDBO.MANAGE_OPT
- Consumer group: com.att.nifi.kafka.azure.giom.iomdbo_manage_opt
- Credentials: scope=dl-prod-xflow-kv-scope, key=logon-kafka-prod
- Security protocol: PLAINTEXT
- Starting offsets: EARLIEST
- Source file format: CSV
- CSV source properties: lineSep=\u001D, quote="" (empty)
- CSV delimiter: \u001F (unit separator)

**Schema**
- KAFKA_OP_TYPE string
- KAFKA_TABLE_NAME string
- KAFKA_OP_TS string
- MANAGE_OPT_ID decimal(19,0)
- IOM_ORDER_ID decimal(19,0)
- MANAGE_OPTION string
- SITE_NAME string
- GGS_COMMIT_TS string
- GGS_OP_TYPE string

Partition by load_dt (generated).

**Target**
- Write to: abfss://giom-stg@datalakeeastus2prd.dfs.core.windows.net/iomdbo_manage_opt
- Format: CSV
- Write mode: append
- File naming: {CONFIG_ID}_{APP_ID}_{SRC_ID}_{TIMESTAMP, 'mmddhhmmssSSS'}_{UNIQUE_ID}

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- load_dt: generated SYSDATE, format "yyyyMMdd"

**Global transformation:**
- Replace "", "NULL" with Null (no newValue = remove)

**No validations, no error handling.**

**Schedule:** every hour (0 0 0-23 * * ?)

**Metadata**
- Application: bpmrd
- Feed name: iomdbo_manage_opt
- Feed type: ING
- Support team: ecdw
- Created by: us2472@att.com
- Contact: DL-GCP_ADBA@att.com
- Data Library: DP-DLIB-OrdPE, DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 30831
```

---

## P08 — DataRouter → Parquet + GT + TX + errorHandling, full-featured (2.0%)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/G_LEGALENTITY_prestg
- Subscriber ID: 310
- Feed ID: gaim
- File filter regex: ^G_LEGALENTITY_.*\.csv$
- Source file format: CSV (pipe-delimited)
- File has header (1 line), no trailer

**Schema**
- LEGAL_ENTITY_ID decimal(19,0)
- LEGAL_ENTITY_NAME string
- COUNTRY_CODE string
- CURRENCY_CODE string
- TAX_ID string
- STATUS string
- CREATE_DATE string
- MODIFY_DATE string

Partition by data_dt (generated from SYSDATE).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/G_LEGALENTITY
- Format: Parquet
- Write mode: append

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- data_dt: generated SYSDATE, format "yyyyMMdd"

**Global transformation:**
- Replace "", "NULL", "null" with Null
- Trim spaces

**Error handling:**
- Strict: fail on any error (threshold 0%)
- Error table location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/G_LEGALENTITY_stlerror

**Schedule:** every 30 minutes (0 0/30 * * * ?)
**Retain source files for 7 days.**

**Metadata**
- Application: bpmrd
- Feed name: STG_gaim_G_LEGALENTITY_src
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-Fin
- Rim Policy: FIN-103
- Mots ID: 28400
```

---

## P09 — File → overwrite, no partitions (1.0%)

```
/scaffold-xflow-orchestrator

- Source: ADLS file (pre-landed)
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/attwifi_phonebook_prestg
- Source file format: Parquet

**Schema**
- phone_id string
- phone_number string
- phone_type string
- contact_name string
- location_id string

No partitions.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/attwifi_phonebook
- Format: Parquet
- Write mode: overwrite (small lookup table, replace entirely each run)

**No transformations, no validations, no global transform, no error handling.**

**Schedule:** daily at 3:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: wifi_attwifi_phonebook_src
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 20100
```

---

## P10 — Kafka → Parquet + TX + GT, append, partitioned (1.2%)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667,dicore-prod-01-gg-kafka2.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: GIOM.IOMDBO.NETWORX
- Consumer group: com.att.nifi.kafka.azure.giom.iomdbo_networx
- Credentials: scope=dl-prod-xflow-kv-scope, key=logon-kafka-prod
- Starting offsets: LATEST

**Schema**
- KAFKA_OP_TYPE string
- NETWORX_ID decimal(19,0)
- CIRCUIT_ID string
- ORDER_ID decimal(19,0)
- PRODUCT_TYPE string
- STATUS string

Partition by load_dt (generated).

**Target**
- Write to: abfss://giom-stg@datalakeeastus2prd.dfs.core.windows.net/iomdbo_networx
- Format: Parquet
- Write mode: append

**Transformations:**
- load_ts: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- load_dt: generated SYSDATE, format "yyyyMMdd"

**Global transformation:**
- Replace "", "NULL" with Null

**No validations, no error handling.**

**Schedule:** every hour
**Retain source files for 7 days.**

**Metadata**
- Application: bpmrd
- Feed name: iomdbo_networx
- Feed type: ING
- Support team: ecdw
- Created by: us2472@att.com
- Contact: DL-GCP_ADBA@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 30831
```

---

## P11 — Azure Files → Parquet + TX + GT, append, partitioned (0.8%)

```
/scaffold-xflow-orchestrator

- Source: Azure File Share
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/customer_prestg
- Subscriber ID: 367
- Feed ID: nggni
- File share name: nggni-prod01
- Storage account: dicoreprod01sftp
- SAS token vault: dl-prod-xflow-kv
- SAS token key: sas-token-sftp-files
- Resource path: (root)
- File filter regex: ^CUSTOMER\.\d+\.txt.gz$
- Duplicate file check: Yes
- Source file format: CSV (pipe-delimited)
- CSV source properties: quote="" (empty)
- File has header (1 line) and trailer (1 line)
- Need record count validation from trailer
- File is compressed (gzip)
- Partition from filename: regex \.(\d{8})\..*, date format yyyyMMdd

**Schema**
- customer_id decimal(38,18)
- customer_name string
- strata_id string
- bill_str1 string
- bill_city string
- bill_state_province_id decimal(38,18)
- bill_zip string
- mcn string
- tcon_name string
- tcon_phone string
- tcon_email string
- bcon_name string
- bcon_phone string
- bcon_email string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/customer
- Format: Parquet
- Write mode: append

**Transformations:**
- load_ts: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**Global transformation:**
- Replace "", " ", "null", "NULL" with Null
- Trim spaces
- Remove start/end single quote characters (')

**No validations, no error handling.**

**Schedule:** weekdays at 2:00 PM UTC (0 0 14 ? * MON-FRI)

**Metadata**
- Application: bpmrd
- Feed name: STG_customer
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: sfiawoo@us.ibm.com
- Data Library: DP-DLIB-BillE,DP-DLIB-NetC
- Rim Policy: SAL-100
- Mots ID: 14226
```

---

## P12 — JDBC → Upsert (delta) with merge keys (0.06%)

```
/scaffold-xflow-orchestrator

- Source: MySQL database to ADLS Delta
- SQL File: abfss://stl@datalakeeastus2prd.dfs.core.windows.net/mysql/query/stl_config/STL_FEED_JOB_CONTROL.txt
- Database credentials: scope=dl-prod-xflow-kv-scope, key=stljdbc-mysql-connect-secret
- SQL has bind parameters:
  - Parameter 1: FETCH_ON_NULL, "select MIN(LAST_MODIFIED_AT) as param1 FROM STL_CONFIG.STL_FEED_JOB_CONTROL", saveValueFromIndex: 2
  - Parameter 2: FETCH_ALWAYS, "select MAX(LAST_MODIFIED_AT) as param2 FROM STL_CONFIG.STL_FEED_JOB_CONTROL"

**Schema**
- ID string (primary key)
- APP_ID string
- FEED_ID string
- JOB_ID string
- JOB_RUN_ID string
- STATUS string
- ERROR_CODE string
- ERROR_MESSAGE string
- JOB_START_TIMESTAMP string
- JOB_END_TIMESTAMP string
- LAST_MODIFIED_AT string
- DATA_DT string

No partitions.

**Target**
- Write to: abfss://stl@datalakeeastus2prd.dfs.core.windows.net/mysql/stl_config/stl_feed_job_control
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: upsert (primary key: ID)

**No transformations, no validations, no global transform, no error handling.**

**Schedule:** daily at 7:05 AM UTC
**Retain source files for 0 days (no retention).**

**Metadata**
- Application: bpmrd
- Feed name: mysqltodelta_stl_config_stl_feed_job_control
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-Wrkf
- Rim Policy: NET-300
- Mots ID: 30636
```

---

## P13 — JDBC → Delta, overwritePartition (0.01%)

```
/scaffold-xflow-orchestrator

- Source: MySQL database to ADLS Delta
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/cricket/sim_swap_details.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=stljdbc-sqlserver-cricket-abiprod-secret
- No SQL bind parameters

**Schema**
- calendardate string
- simchangescnt string
- successfulfraudulentcnt string
- failedsimchangescnt string
- successfulsimchangescnt string
- avgremediatetime string
- complaintsreceivedcnt string

Partition by calendardate.

**Target**
- Write to: abfss://cricket@datalakeeastus2prd.dfs.core.windows.net/sim_swap_details
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: overwritePartition

**Transformations:**
- calendardate: dateFormat conversion, source format "yyyy-MM-dd", target format "yyyy-MM-dd"

**No validations, no global transform, no error handling.**

**Schedule:** daily at 2:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: cricket_sim_swap_extract
- Feed type: ING
- Support team: Datalake
- Created by: us2472@att.com
- Contact: CricketNonDoxOperations@amdocs.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: NET-300
- Mots ID: 22538
```

---

## P14 — Kafka → JSON target + transforms (0.03%)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: broker-east-1:9093,broker-east-2:9093
- Topic: TDATA.IM_HNM_DATA
- Consumer group: com.att.kafka.azure.tdata.im_hnm_data
- Credentials: scope=dl-prod-xflow-kv-scope, key=logon-kafka-prod
- Starting offsets: LATEST
- Source file format: JSON

**Schema**
- event_id string
- event_type string
- device_id string
- hnm_status string
- timestamp_utc string
- payload string

Partition by data_dt (generated).

**Target**
- Write to: abfss://tdata-stg@datalakeeastus2prd.dfs.core.windows.net/im_hnm_data
- Format: JSON
- Write mode: append

**Transformations:**
- data_dt: generated SYSDATE, format "yyyyMMdd"

**No validations, no global transform, no error handling.**

**Schedule:** every 15 minutes (0 0/15 * * * ?)

**Metadata**
- Application: bpmrd
- Feed name: STG_tdata_im_hnm_data
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 31500
```

---

## P15 — DataRouter → Delta + errorHandling (0.03%)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/ccpa_temp_donotsell_prestg
- Subscriber ID: 420
- Feed ID: cmp
- File filter regex: ^ccpa_temp_dns_.*\.csv$
- Source file format: CSV

**Schema**
- ban string
- ctn string
- dns_flag string
- dns_effective_date string
- dns_expiration_date string
- create_ts string
- modify_ts string

Partition by data_dt (generated from SYSDATE).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/ccpa_temp_donotsell
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append

**Error handling:**
- Strict: fail on any error (threshold 0%)
- Error table: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/ccpa_temp_donotsell_stlerror

**No transformations, no validations, no global transform.**

**Schedule:** daily at 8:00 AM UTC
**Retain source files for 7 days.**

**Metadata**
- Application: bpmrd
- Feed name: STG_cmp_ccpa_temp_donotsell_src
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: CUST-100
- Mots ID: 29800
```

---

## P16 — File → overwritePartition + errorHandling (0.06%)

```
/scaffold-xflow-orchestrator

- Source: ADLS file
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/route_call_variable_mobility_prestg
- Source file format: CSV (comma-delimited)

**Schema**
- call_id string
- variable_name string
- variable_value string
- call_type string
- call_date string
- agent_id string

Partition by call_date.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/route_call_variable_mobility
- Format: Parquet
- Write mode: overwritePartition

**Error handling:**
- Standard: fail on error, skip malformed, bad file for debugging
- Error table: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/route_call_variable_mobility_stlerror

**No transformations, no validations, no global transform.**

**Schedule:** daily at 4:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: route_call_variable_mobility
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 18900
```

---

## P17 — File → fixed-width source format (9.8%)

```
/scaffold-xflow-orchestrator

- Source: ADLS file
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/order_tariff_prestg
- Source file format: fixed-width
- Fixed-width column lengths: 15, 30, 10, 8, 12, 20, 6

**Schema**
- tariff_id string
- tariff_name string
- tariff_type string
- eff_date string
- exp_date string
- rate_code string
- status string

Partition by eff_date.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/order_tariff
- Format: Parquet
- Write mode: append

**Error handling:**
- Strict: threshold 0%, bad file for debugging

**No transformations, no validations, no global transform.**

**Schedule:** daily at 6:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: stl_order_tariff
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 14226
```

---

## P18 — JDBC with bind parameters (34.7%)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/opusc/agency_fan_details.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-opusc-jdbc
- SQL has bind parameters:
  - Parameter 1 (FETCH_ON_NULL): "select TO_CHAR(to_date(TO_DATE(SUBSTR(MAX(ECDW_BATCH_ID),1,8),'YYYYMMDD') - INTERVAL '1' DAY),'yyyymmdd') AS RESULT1 FROM ECDW_SLOPUS_STG.OPUS_BATCH_SCN_LOG WHERE lower(TABLE_NAME) ='agency_fan_details'", saveValueFromIndex: 2
  - Parameter 2 (FETCH_ALWAYS): "select MAX(ECDW_BATCH_ID) AS RESULT2 FROM ECDW_SLOPUS_STG.OPUS_BATCH_SCN_LOG WHERE lower(TABLE_NAME) ='agency_fan_details'"

**Schema**
- agency_fan_detail_id string
- session_id string
- agency_name string
- fan_type string
- fan_creation_date timestamp
- ggs_commit_ts string
- ggs_op_type string
- ecdw_batch_id string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://opus-stg@datalakeeastus2prd.dfs.core.windows.net/agency_fan_details
- Format: Parquet
- Write mode: append

**Schedule:** daily at 4:30 PM UTC
**Retain source files for 7 days.**

**No transformations, no validations, no global transform, no error handling.**

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_agency_fan_details_v2
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: dtvsupportcenter@directv.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: FIN-103
- Mots ID: 25048
```

---

## P19 — Config with hashingAndEncrypt PII (0.4%)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/tlgmob/port_request_phi.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-tlgmob
- No SQL bind parameters

**Schema**
- request_id string
- customer_name string
- ssn string
- account_number string
- phone_number string
- email_address string
- request_date string
- status string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://tlgmob-stg@datalakeeastus2prd.dfs.core.windows.net/port_request_phi
- Format: CSV
- Write mode: append

**Transformations:**
- Encrypt ssn column (hashingAndEncrypt, identity: DL_IDENTITY@ATT.COM, format: ALPHA_NUM)
- Encrypt email_address column (hashingAndEncrypt, identity: DL_IDENTITY@ATT.COM, format: ALPHA_NUM)

**Error handling:**
- Standard: fail on error, skip malformed, bad file

**No validations, no global transform.**

**Schedule:** daily at 5:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_port_request_phi
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: CUST-100
- Mots ID: 19500
```

---

## P20 — Kafka → continuous processing (0.06%)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: EDM.DELTA_EDM_ECMI
- Consumer group: com.att.nifi.kafka.azure.edm.ecmi
- Credentials: scope=dl-prod-xflow-kv-scope, key=logon-kafka-prod
- Starting offsets: LATEST

**Schema**
- event_id string
- event_type string
- customer_id string
- timestamp_utc string
- payload string

No partitions.

**Target**
- Write to: abfss://edm-stg@datalakeeastus2prd.dfs.core.windows.net/delta_edm_ecmi
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append

**Job mode: continuous processing (no cron schedule)**

**No transformations, no validations, no global transform, no error handling.**

**Metadata**
- Application: bpmrd
- Feed name: stl_delta_edm_ecmi
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: NET-300
- Mots ID: 31000
```

---

## P21 — Azure Files → Delta + globalTransform (0.01%)

```
/scaffold-xflow-orchestrator

- Source: Azure File Share
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/cbs_vtns_prestg
- Subscriber ID: 500
- Feed ID: cbsvtns
- File share name: cbsvtns-prod01
- Storage account: dicoreprod01sftp
- SAS token vault: dl-prod-xflow-kv
- SAS token key: sas-token-sftp-vtns
- Resource path: lz/inbound
- File filter regex: ^CBS_VTNS_.*\.csv$
- Source file format: CSV (pipe-delimited)

**Schema**
- vtns_id string
- circuit_id string
- service_type string
- status string
- activate_date string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/cbs_vtns
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append

**Transformations:**
- load_ts: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**Global transformation:**
- Replace "", "NULL", "null" with Null
- Trim spaces

**No validations, no error handling.**

**Schedule:** weekdays at 10:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_cbs_vtns
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 15000
```

---

## P22 — Config with csvSourceProperties (12.5%)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/wo_sec_group_members_prestg
- Subscriber ID: 200
- Feed ID: edge
- File filter regex: ^edge_wo_sec_group_members_.*\.csv$
- Source file format: CSV
- CSV source properties: delimiter=|, header=true, multiLine=false, quote="
- Duplicate file check: No

**Schema**
- GROUP_ID string
- MEMBER_ID string
- MEMBER_NAME string
- MEMBER_TYPE string
- EFFECTIVE_DATE string
- data_dt string

Partition by data_dt (generated from SYSDATE).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/wo_sec_group_members
- Format: CSV
- Write mode: append

**Global transformation:**
- Replace "", "NULL" with Null

**No transformations, no validations, no error handling.**

**Schedule:** every 2 hours
**Retain source files for 7 days.**

**Metadata**
- Application: bpmrd
- Feed name: STG_edge_wo_sec_group_members
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 22000
```

---

## P23 — Config with Unity Catalog (0.4%)

```
/scaffold-xflow-orchestrator

- Source: Oracle database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/esbnis/GALGEH_IPLAN_POD_RAN_MV.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-esbnis
- No SQL bind parameters

**Schema**
- pod_id string
- ran_id string
- site_name string
- latitude double
- longitude double
- market_code string
- region string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://esbnis-stg@datalakeeastus2prd.dfs.core.windows.net/GALGEH_IPLAN_POD_RAN_MV
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append

**Transformations:**
- load_ts: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**Global transformation:**
- Replace "", "NULL" with Null

**No validations, no error handling.**

**Schedule:** daily at 6:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_esbnis_GALGEH_IPLAN_POD_RAN_MV_src
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 18200
```

---

## P24 — DataRouter with moveToReject + retryFile (0.1%)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/sales_order_misc_prestg
- Subscriber ID: 180
- Feed ID: usrp
- File filter regex: ^sales_order_misc_.*\.dat$
- Source file format: Parquet

**Schema**
- order_id string
- misc_code string
- misc_value string
- create_date string
- modify_date string

No partitions.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/sales_order_misc
- Format: Parquet
- Write mode: overwrite

**Error handling: Custom**
- Threshold: 1%
- Skip malformed: Yes
- Move failed files to reject: Yes, reject location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/sales_order_misc_reject
- Bad file: Yes
- Retry failed files: Yes

**No transformations, no validations, no global transform.**

**Schedule:** every 4 hours

**Metadata**
- Application: bpmrd
- Feed name: sales_order_misc_src
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 27000
```

---

## P25 — File → XML source (0.01%)

```
/scaffold-xflow-orchestrator

- Source: ADLS file
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/registration_vrss_prestg
- Source file format: XML
- XML row path: registrations/registration

**Schema**
- registration_id string
- device_id string
- service_type string
- registration_date string
- status string
- customer_id string

Partition by registration_date.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/registration_vrss
- Format: Parquet
- Write mode: append

**Transformations:**
- data_dt: generated SYSDATE, format "yyyyMMdd"

**No validations, no global transform, no error handling.**

**Schedule:** daily at 7:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_rss_registration_vrss
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 25500
```

---

## P26 — JDBC Snowflake with extra fields (0.3%)

```
/scaffold-xflow-orchestrator

- Source: Snowflake database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/analytics/customer_segments.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-snowflake-analytics
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
- expiry_date string
- model_version string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://analytics-stg@datalakeeastus2prd.dfs.core.windows.net/customer_segments
- Format: Parquet
- Write mode: append

**No transformations, no validations, no global transform, no error handling.**

**Schedule:** weekly on Mondays at 6:00 AM UTC (0 0 6 ? * MON)

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_customer_segments
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: CUST-100
- Mots ID: 32000
```

---

## P27 — JDBC Teradata (0.03%)

```
/scaffold-xflow-orchestrator

- Source: Teradata database to ADLS
- SQL File: abfss://adl@datalakeeastus2prd.dfs.core.windows.net/jdbc/sql/edw/customer_account_summary.sql
- Database credentials: scope=dl-prod-xflow-kv-scope, key=xflow-teradata-edw
- No SQL bind parameters

**Schema**
- account_id string
- customer_name string
- account_type string
- balance decimal(15,2)
- open_date string
- close_date string
- region_code string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://edw-stg@datalakeeastus2prd.dfs.core.windows.net/customer_account_summary
- Format: Parquet
- Write mode: append

**No transformations, no validations, no global transform, no error handling.**

**Schedule:** daily at 4:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_JDBC_customer_account_summary
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: FIN-103
- Mots ID: 16000
```

---

## P28 — Kafka → kafkatext raw text (0.2%)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: EDM.ECMI
- Consumer group: com.att.nifi.kafka.azure.edm.ecmi_text
- Credentials: scope=dl-prod-xflow-kv-scope, key=logon-kafka-prod
- Starting offsets: LATEST
- Source file format: kafkatext (raw message stored as-is)

**Schema**
- data_dt string (partition column only — kafkatext stores raw message as-is, no data columns in schema)

Partition by data_dt.

**Target**
- Write to: abfss://edm-stg@datalakeeastus2prd.dfs.core.windows.net/ecmi
- Format: CSV (kafkatext requires csv target, not text)
- Write mode: append

**No transformations, no validations, no global transform, no error handling.**

**Schedule:** every hour

**Metadata**
- Application: bpmrd
- Feed name: STG_ecmi
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: NET-300
- Mots ID: 31000
```

---

## Coverage Matrix

| # | Source | Target | WriteMode | TX | GT | EH | Special Features |
|---|--------|--------|-----------|----|----|-----|-----------------|
| P01 | JDBC Oracle | Parquet | (default) | - | - | - | Baseline JDBC |
| P02 | File | Parquet | (default) | - | - | - | Fixed-width source |
| P03 | JDBC Oracle | CSV | (default) | - | - | - | CSV target props |
| P04 | DataRouter | CSV | append | dateFormat | - | - | Header/trailer, record count, DEST_PARTITIONING |
| P05 | DataRouter | Parquet | append | - | - | - | Baseline DR |
| P06 | JDBC Oracle | Parquet | (default) | - | replaceValues | - | GT only |
| P07 | Kafka | CSV | append | dateFormat x2 | replaceValues | - | csvSourceProperties, kafkatext delimiters |
| P08 | DataRouter | Parquet | append | dateFormat x2 | replaceValues+trim | threshold 0% | Full-featured |
| P09 | File | Parquet | overwrite | - | - | - | Small lookup table |
| P10 | Kafka | Parquet | append | dateFormat x2 | replaceValues | - | Kafka + Parquet |
| P11 | Azure Files | Parquet | append | dateFormat | replaceValues+trim+removeQuotes | - | Compression, filename partition, file share |
| P12 | JDBC MySQL | Delta | upsert | - | - | - | Bind params, PK, upsert |
| P13 | JDBC MySQL | Delta | overwritePartition | dateFormat | - | - | Delta OWP |
| P14 | Kafka | JSON | append | dateFormat | - | - | JSON target |
| P15 | DataRouter | Delta | append | - | - | threshold 0% | DR → Delta + EH |
| P16 | File | Parquet | overwritePartition | - | - | Standard | File OWP + EH |
| P17 | File | Parquet | (default) | - | - | threshold 0% | Fixed-width |
| P18 | JDBC Oracle | Parquet | (default) | - | - | - | Bind params (FETCH_ON_NULL + FETCH_ALWAYS) |
| P19 | JDBC Oracle | CSV | (default) | hashingAndEncrypt | - | Standard | PII encryption (ssn, email) |
| P20 | Kafka | Delta | append | - | - | - | Continuous processing (no cron) |
| P21 | Azure Files | Delta | append | dateFormat | replaceValues+trim | - | AzFiles → Delta |
| P22 | DataRouter | CSV | append | - | replaceValues | - | csvSourceProperties |
| P23 | JDBC Oracle | Delta | append | dateFormat | replaceValues | - | Unity Catalog |
| P24 | DataRouter | Parquet | overwrite | - | - | Custom (reject+retry) | moveToReject, retryFile |
| P25 | File | Parquet | append | dateFormat | - | - | XML source |
| P26 | JDBC Snowflake | Parquet | (default) | - | - | - | sfDatabase, sfSchema, sfWarehouse |
| P27 | JDBC Teradata | Parquet | (default) | - | - | - | Teradata driver |
| P28 | Kafka | text | append | - | - | - | kafkatext raw |
