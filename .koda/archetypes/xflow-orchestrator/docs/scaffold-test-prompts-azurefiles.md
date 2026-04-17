# XFlow Orchestrator — 6 Azure Files Source Test Prompts

Generated from scanning **270 Azure Files production configs** across the enterprise data lake.

---

## S-05a — AzFiles → Parquet + TX + GT, append, partitioned (128 configs)

```
/scaffold-xflow-orchestrator

- Source: Azure File Share
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/az_customer_prestg
- Subscriber ID: 367
- Feed ID: bpmrd
- File share name: bpmrd-prod01
- Storage account: dicoreprod01sftp
- SAS token vault: dl-prod-xflow-kv
- SAS token key: sas-token-sftp-bpmrd
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
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/az_customer
- Format: Parquet
- Write mode: append

**Transformations:**
- load_ts: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**Global transformation:**
- Replace "", " ", "null", "NULL" with Null
- Trim spaces
- Remove start/end single quote characters (')

**No validations, no error handling overrides.**

**Schedule:** weekdays at 2:00 PM UTC (0 0 14 ? * MON-FRI)

**Metadata**
- Application: bpmrd
- Feed name: STG_az_customer
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-BillE,DP-DLIB-NetC
- Rim Policy: SAL-100
- Mots ID: 14226
```

---

## S-05b — AzFiles → Parquet + TX, no GT, partitioned (29 configs)

```
/scaffold-xflow-orchestrator

- Source: Azure File Share
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/az_swavail_prestg
- Subscriber ID: 400
- Feed ID: bpmrd
- File share name: bpmrd-prod01
- Storage account: dicoreprod01sftp
- SAS token vault: dl-prod-xflow-kv
- SAS token key: sas-token-sftp-bpmrd
- Resource path: lz/inbound
- File filter regex: ^swavail_.*\.csv$
- Source file format: CSV (pipe-delimited)

**Schema**
- switch_id string
- switch_name string
- avail_pct decimal(9,2)
- report_date string
- region string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/az_swavail
- Format: Parquet
- Write mode: append

**Transformations:**
- load_ts: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**No validations, no global transform, no error handling overrides.**

**Schedule:** daily at 8:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_az_swavail
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 20100
```

---

## S-05c — AzFiles → Parquet, no TX, partitioned (17 configs)

```
/scaffold-xflow-orchestrator

- Source: Azure File Share
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/az_datalake_src_prestg
- Subscriber ID: 410
- Feed ID: bpmrd
- File share name: bpmrd-prod01
- Storage account: dicoreprod01sftp
- SAS token vault: dl-prod-xflow-kv
- SAS token key: sas-token-sftp-bpmrd
- Resource path: lz/data
- File filter regex: ^datalake_src_.*\.parquet$
- Source file format: Parquet

**Schema**
- record_id string
- record_type string
- source_system string
- create_date string
- status string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/az_datalake_src
- Format: Parquet
- Write mode: append

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 6:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_az_datalake_src
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 18200
```

---

## S-05d — AzFiles → errorHandling (6 configs)

```
/scaffold-xflow-orchestrator

- Source: Azure File Share
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/az_access_spec_prestg
- Subscriber ID: 367
- Feed ID: bpmrd
- File share name: bpmrd-prod01
- Storage account: dicoreprod01sftp
- SAS token vault: dl-prod-xflow-kv
- SAS token key: sas-token-sftp-bpmrd
- Resource path: (root)
- File filter regex: ^aoste_access_spec_.*\.csv.gz$
- Duplicate file check: Yes
- Source file format: CSV (pipe-delimited)
- File is compressed (gzip)

**Schema**
- access_spec_id string
- spec_name string
- spec_type string
- bandwidth string
- status string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/az_access_spec
- Format: Parquet
- Write mode: append

**Transformations:**
- load_ts: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**Error handling:**
- Standard: fail on error, skip malformed, bad file

**No validations, no global transform.**

**Schedule:** weekdays at 2:00 PM UTC (0 0 14 ? * MON-FRI)

**Metadata**
- Application: bpmrd
- Feed name: STG_az_access_spec
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 14226
```

---

## S-05e — AzFiles → CSV + TX + GT, append, partitioned (4 configs)

```
/scaffold-xflow-orchestrator

- Source: Azure File Share
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/az_usps_container_scan_prestg
- Subscriber ID: 450
- Feed ID: bpmrd
- File share name: bpmrd-prod01
- Storage account: dicoreprod01sftp
- SAS token vault: dl-prod-xflow-kv
- SAS token key: sas-token-sftp-bpmrd
- Resource path: lz/macs
- File filter regex: ^adi_usps_container_scan_.*\.csv$
- Source file format: CSV (pipe-delimited)

**Schema**
- scan_id string
- container_id string
- scan_date string
- location string
- scan_type string
- status string

Partition by data_dt (generated).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/az_usps_container_scan
- Format: CSV
- Write mode: append
- CSV target properties: separator=|

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- data_dt: generated SYSDATE, format "yyyyMMdd"

**Global transformation:**
- Replace "", "NULL" with Null
- Trim spaces

**No validations, no error handling overrides.**

**Schedule:** daily at 7:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_az_usps_container_scan
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 22000
```

---

## S-05f — AzFiles → Delta + GT (2 configs)

```
/scaffold-xflow-orchestrator

- Source: Azure File Share
- Prestaging location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/az_cbs_vtns_prestg
- Subscriber ID: 500
- Feed ID: bpmrd
- File share name: bpmrd-prod01
- Storage account: dicoreprod01sftp
- SAS token vault: dl-prod-xflow-kv
- SAS token key: sas-token-sftp-bpmrd
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
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/az_cbs_vtns
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append

**Transformations:**
- load_ts: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**Global transformation:**
- Replace "", "NULL", "null" with Null
- Trim spaces

**No validations, no error handling overrides.**

**Schedule:** weekdays at 10:00 AM UTC (0 0 10 ? * MON-FRI)

**Metadata**
- Application: bpmrd
- Feed name: STG_az_cbs_vtns
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 15000
```
