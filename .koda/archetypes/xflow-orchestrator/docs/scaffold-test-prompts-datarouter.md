# XFlow Orchestrator — 11 DataRouter Source Test Prompts

Generated from scanning **4,012 DataRouter production configs** across the enterprise data lake.

---

## S-02a — DR → CSV + transforms, append, partitioned (1,180 configs)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_store_daily_sales_prestg
- Subscriber ID: 277
- Feed ID: bpmrd
- File filter regex: ^store_dly_sls_.*$
- Source file format: CSV (pipe-delimited)

**Schema**
- ACTVT_DT string
- STORE_LOC_ID string
- STORE_LOC_NM string
- ST_CD string
- ZIP_CD string
- SLS_AMT decimal(19,4)
- SLS_CNT long

Partition by load_dt (generated).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_store_daily_sales
- Format: CSV
- Write mode: append
- CSV target properties: separator=|
- Retain source files for 7 days

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- load_dt: generated SYSDATE, format "yyyyMMdd"

**No validations, no global transform, no error handling overrides.**

**Schedule:** every hour

**Metadata**
- Application: bpmrd
- Feed name: STG_dr_store_daily_sales
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-Fin
- Rim Policy: NET-300
- Mots ID: 24169
```

---

## S-02b — DR → Parquet, append, no transforms, partitioned (1,056 configs)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_srv_ord_prod_itm_prestg
- Subscriber ID: 150
- Feed ID: bpmrd
- File filter regex: ^srv_ord_prod_itm_.*\.dat$
- Source file format: Parquet

**Schema**
- srv_ord_id string
- prod_itm_id string
- itm_desc string
- qty long
- unit_price decimal(19,2)
- status_cd string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_srv_ord_prod_itm
- Format: Parquet
- Write mode: append
- Retain source files for 7 days

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** every 2 hours (0 0 0/2 * * ?)

**Metadata**
- Application: bpmrd
- Feed name: STG_dr_srv_ord_prod_itm
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 19062
```

---

## S-02c — DR → Parquet + GT + transforms, append, partitioned (299 configs)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_person_data_prestg
- Subscriber ID: 310
- Feed ID: bpmrd
- File filter regex: ^G_PERSON_.*\.csv$
- Source file format: CSV (pipe-delimited)

**Schema**
- PERSON_ID decimal(19,0)
- FIRST_NAME string
- LAST_NAME string
- COUNTRY_CODE string
- STATUS string

Partition by data_dt (generated).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_person_data
- Format: Parquet
- Write mode: append
- Retain source files for 7 days

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- data_dt: generated SYSDATE, format "yyyyMMdd"

**Global transformation:**
- Trim spaces
- Replace "", "NULL", "null" with Null

**No validations, no error handling overrides.**

**Schedule:** every 30 minutes (0 0/30 * * * ?)

**Metadata**
- Application: bpmrd
- Feed name: STG_dr_person_data
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-Fin
- Rim Policy: FIN-103
- Mots ID: 28400
```

---

## S-02d — DR → Parquet + transforms, no GT, partitioned (231 configs)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_country_ref_prestg
- Subscriber ID: 310
- Feed ID: bpmrd
- File filter regex: ^G_COUNTRY_.*\.csv$
- Source file format: CSV (pipe-delimited)

**Schema**
- COUNTRY_ID decimal(19,0)
- COUNTRY_CODE string
- COUNTRY_NAME string
- CURRENCY_CODE string

Partition by data_dt (generated).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_country_ref
- Format: Parquet
- Write mode: append
- Retain source files for 7 days

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- data_dt: generated SYSDATE, format "yyyyMMdd"

**No validations, no global transform, no error handling overrides.**

**Schedule:** every hour

**Metadata**
- Application: bpmrd
- Feed name: STG_dr_country_ref
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-Fin
- Rim Policy: FIN-103
- Mots ID: 28400
```

---

## S-02e — DR → Parquet + GT, no transforms, partitioned (195 configs)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_vintoesn_prestg
- Subscriber ID: 200
- Feed ID: bpmrd
- File filter regex: ^vintoesn_.*\.dat$
- Source file format: Parquet

**Schema**
- esn_id string
- vin_number string
- vehicle_type string
- status string
- last_update string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_vintoesn
- Format: Parquet
- Write mode: append
- Retain source files for 7 days

**Global transformation:**
- Replace "", "NULL" with Null

**No transformations, no validations, no error handling overrides.**

**Schedule:** every 2 hours (0 0 0/2 * * ?)

**Metadata**
- Application: bpmrd
- Feed name: STG_dr_vintoesn
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 20100
```

---

## S-02f — DR → overwrite, no partitions (139 configs)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_item_master_prestg
- Subscriber ID: 180
- Feed ID: bpmrd
- File filter regex: ^item_master_.*\.dat$
- Source file format: Parquet

**Schema**
- item_id string
- item_name string
- category string
- uom string
- status string

No partitions (lookup table).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_item_master
- Format: Parquet
- Write mode: overwrite

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 3:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_dr_item_master
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 27000
```

---

## S-02g — DR → Parquet + errorHandling (100 configs)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_shm_activity_prestg
- Subscriber ID: 250
- Feed ID: bpmrd
- File filter regex: ^shm_activity_.*\.csv$
- Source file format: CSV (pipe-delimited)

**Schema**
- activity_id string
- activity_type string
- work_order_id string
- tech_id string
- status string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_shm_activity
- Format: Parquet
- Write mode: append
- Retain source files for 7 days

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**Error handling:**
- Standard: fail on error, skip malformed, bad file

**No validations, no global transform.**

**Schedule:** every 4 hours (0 0 0/4 * * ?)

**Metadata**
- Application: bpmrd
- Feed name: STG_dr_shm_activity
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 18900
```

---

## S-02h — DR → Delta, transforms (53 configs)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_order_lines_hist_prestg
- Subscriber ID: 320
- Feed ID: bpmrd
- File filter regex: ^oe_order_lines_.*\.csv$
- Source file format: CSV (pipe-delimited)

**Schema**
- order_line_id string
- order_id string
- item_id string
- quantity long
- unit_price decimal(19,2)
- status string

Partition by data_dt (generated).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_order_lines_hist
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append
- Retain source files for 7 days

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- data_dt: generated SYSDATE, format "yyyyMMdd"

**No validations, no global transform, no error handling overrides.**

**Schedule:** daily at 6:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_dr_order_lines_hist
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 22538
```

---

## S-02j — DR → CSV + GT + errorHandling (10 configs)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_con_work_request_prestg
- Subscriber ID: 200
- Feed ID: bpmrd
- File filter regex: ^con_work_request_.*\.csv$
- Source file format: CSV (pipe-delimited)

**Schema**
- work_request_id string
- request_type string
- priority string
- assigned_to string
- status string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_con_work_request
- Format: CSV
- Write mode: append
- CSV target properties: separator=|
- Retain source files for 7 days

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**Global transformation:**
- Trim spaces
- Replace "", "NULL", "null" with Null

**Error handling:**
- Standard: fail on error, skip malformed, bad file

**No validations.**

**Schedule:** daily at 6:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_dr_con_work_request
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 20100
```

---

## S-02i — DR → Delta + errorHandling (4 configs)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_ccpa_donotsell_prestg
- Subscriber ID: 420
- Feed ID: bpmrd
- File filter regex: ^ccpa_dns_.*\.csv$
- Source file format: CSV (pipe-delimited)

**Schema**
- ban string
- ctn string
- dns_flag string
- dns_effective_date string
- dns_expiration_date string

Partition by data_dt (generated from SYSDATE).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_ccpa_donotsell
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append
- Retain source files for 7 days

**Error handling:**
- Standard: fail on error, skip malformed, bad file

**No transformations, no validations, no global transform.**

**Schedule:** daily at 8:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_dr_ccpa_donotsell
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: CUST-100
- Mots ID: 29800
```

---

## S-02k — DR → overwritePartition (2 configs)

```
/scaffold-xflow-orchestrator

- Source: DataRouter (httpFileSource)
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_callback_allowed_prestg
- Subscriber ID: 160
- Feed ID: bpmrd
- File filter regex: ^CallbackAllowed_.*\.csv$
- Source file format: CSV (pipe-delimited)

**Schema**
- callback_id string
- queue_name string
- caller_id string
- callback_time string
- status string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dr_callback_allowed
- Format: Parquet
- Write mode: overwritePartition
- Retain source files for 7 days

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 4:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_dr_callback_allowed
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 18900
```
