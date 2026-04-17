# XFlow Orchestrator — 9 ADLS File Source Test Prompts

Generated from scanning **3,410 File source production configs** across the enterprise data lake.

---

## S-03a — File → minimal (no TX/GT/EH), partitioned (2,379 configs)

```
/scaffold-xflow-orchestrator

- Source: ADLS file
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/file_tech_order_data_prestg
- Source file format: CSV

**Schema**
- order_id string
- order_type string
- tech_id string
- dispatch_date string
- region_cd string
- status string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/file_tech_order_data
- Format: Parquet
- Write mode: append
- Retain source files for 7 days

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 6:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_file_tech_order_data
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 18500
```

---

## S-03b — File → errorHandling, partitioned (415 configs)

```
/scaffold-xflow-orchestrator

- Source: ADLS file
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/file_order_tariff_prestg
- Source file format: fixed-width
- Fixed-width column widths: 15, 30, 10, 8, 12, 6

**Schema**
- tariff_id string
- tariff_name string
- tariff_type string
- eff_date string
- rate_code string
- status string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/file_order_tariff
- Format: Parquet
- Write mode: append
- Retain source files for 7 days

**Error handling:**
- Standard: fail on error, skip malformed, bad file

**No transformations, no validations, no global transform.**

**Schedule:** daily at 5:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_file_order_tariff
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 14226
```

---

## S-03c — File → transforms, partitioned (189 configs)

```
/scaffold-xflow-orchestrator

- Source: ADLS file
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/supplier_address_prestg
- Source file format: CSV (pipe-delimited)

**Schema**
- supplier_id string
- supplier_name string
- address_line1 string
- city string
- state string
- zip string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/supplier_address
- Format: Parquet
- Write mode: append
- Retain source files for 7 days

**Transformations:**
- Add LOAD_TS column: generated value SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**No validations, no global transform, no error handling overrides.**

**Schedule:** daily at 7:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_file_supplier_address
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 20100
```

---

## S-03d — File → overwrite, no partitions (156 configs)

```
/scaffold-xflow-orchestrator

- Source: ADLS file
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/phonebook_lookup_prestg
- Source file format: Parquet

**Schema**
- phone_id string
- phone_number string
- phone_type string
- contact_name string
- location_id string

No partitions (small lookup table).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/phonebook_lookup
- Format: Parquet
- Write mode: overwrite

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 3:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_file_phonebook_lookup
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 20100
```

---

## S-03e — File → transforms + errorHandling (74 configs)

```
/scaffold-xflow-orchestrator

- Source: ADLS file
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/work_request_prestg
- Source file format: CSV (pipe-delimited)

**Schema**
- work_request_id string
- request_type string
- priority string
- assigned_to string
- create_date string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/work_request
- Format: Parquet
- Write mode: append
- Retain source files for 7 days

**Transformations:**
- Add LOAD_TS column: generated value SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"

**Error handling:**
- Standard: fail on error, skip malformed, bad file

**No validations, no global transform.**

**Schedule:** daily at 6:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_file_work_request
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 20100
```

---

## S-03f — File → overwritePartition (55 configs)

```
/scaffold-xflow-orchestrator

- Source: ADLS file
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/tax_fees_prestg
- Source file format: CSV

**Schema**
- tax_code string
- tax_desc string
- rate decimal(9,4)
- eff_date string
- exp_date string
- region string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/tax_fees
- Format: Parquet
- Write mode: overwritePartition
- Retain source files for 7 days

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 4:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_file_tax_fees
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-Fin
- Rim Policy: FIN-103
- Mots ID: 19500
```

---

## S-03g — File → overwrite with transforms (21 configs)

```
/scaffold-xflow-orchestrator

- Source: ADLS file
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dvr_tune_pre_prestg
- Source file format: CSV

**Schema**
- dvr_id string
- channel_id string
- tune_start string
- tune_end string
- duration_sec long
- status string

No partitions in source. Partition by data_dt (generated).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/dvr_tune_pre
- Format: Parquet
- Write mode: overwrite

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- data_dt: generated SYSDATE, format "yyyyMMdd"

**No validations, no global transform, no error handling overrides.**

**Schedule:** daily at 2:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_file_dvr_tune_pre
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: NET-300
- Mots ID: 18900
```

---

## S-03i — File → Parquet target, append (17 configs)

```
/scaffold-xflow-orchestrator

- Source: ADLS file
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/privline_data_prestg
- Source file format: Parquet

**Schema**
- circuit_id string
- circuit_type string
- bandwidth string
- site_a string
- site_z string
- status string
- data_dt string

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/privline_data
- Format: Parquet
- Write mode: append
- Retain source files for 7 days

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** daily at 8:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_file_privline_data
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 18200
```

---

## S-03h — File → overwritePartition + errorHandling (9 configs)

```
/scaffold-xflow-orchestrator

- Source: ADLS file
- Source location: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/call_variable_mobility_prestg
- Source file format: CSV

**Schema**
- call_id string
- variable_name string
- variable_value string
- call_type string
- call_date string
- agent_id string

Partition by call_date.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/call_variable_mobility
- Format: Parquet
- Write mode: overwritePartition
- Retain source files for 7 days

**Error handling:**
- Standard: fail on error, skip malformed, bad file

**No transformations, no validations, no global transform.**

**Schedule:** daily at 4:00 AM UTC

**Metadata**
- Application: bpmrd
- Feed name: STG_file_call_variable_mobility
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 18900
```
