# XFlow Orchestrator — 9 Kafka Source Test Prompts

Generated from scanning **1,324 Kafka production configs** across the enterprise data lake.

---

## S-04a — Kafka → CSV + transforms + GT, partitioned (312 configs)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667,dicore-prod-01-gg-kafka2.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: GIOM.IOMDBO.MANAGE_OPT
- Consumer group: com.att.kafka.azure.bpmrd.manage_opt
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
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/kafka_manage_opt
- Format: CSV
- Write mode: append
- File naming: {CONFIG_ID}_{APP_ID}_{SRC_ID}_{TIMESTAMP, 'mmddhhmmssSSS'}_{UNIQUE_ID}

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- load_dt: generated SYSDATE, format "yyyyMMdd"

**Global transformation:**
- Replace "", "NULL" with Null (no newValue = remove)

**No validations, no error handling overrides.**

**Schedule:** every hour (0 0 0-23 * * ?)
**Retain source files for 7 days.**

**Metadata**
- Application: bpmrd
- Feed name: STG_kafka_manage_opt
- Feed type: ING
- Support team: ecdw
- Created by: us2472@att.com
- Contact: DL-GCP_ADBA@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 30831
```

---

## S-04b — Kafka → GT only (streaming delta), partitioned (265 configs)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667,dicore-prod-01-gg-kafka2.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: GIOM.IOMDBO.ACCESS_TO_PAA
- Consumer group: com.att.kafka.azure.bpmrd.access_to_paa
- Credentials: scope=dl-prod-xflow-kv-scope, key=logon-kafka-prod
- Starting offsets: LATEST
- Source file format: CSV

**Schema**
- KAFKA_OP_TYPE string
- ACCESS_PAA_ID decimal(19,0)
- CIRCUIT_ID string
- STATUS string
- GGS_COMMIT_TS string
- GGS_OP_TYPE string

Partition by load_dt (generated).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/kafka_access_to_paa
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- load_dt: generated SYSDATE, format "yyyyMMdd"

**Global transformation:**
- Replace "", "NULL" with Null

**No validations, no error handling overrides.**

**Schedule:** every hour

**Metadata**
- Application: bpmrd
- Feed name: STG_kafka_access_to_paa
- Feed type: ING
- Support team: ecdw
- Created by: us2472@att.com
- Contact: DL-GCP_ADBA@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 30831
```

---

## S-04c — Kafka → Parquet + TX + GT, append, partitioned (183 configs)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667,dicore-prod-01-gg-kafka2.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: GIOM.IOMDBO.NETWORX
- Consumer group: com.att.kafka.azure.bpmrd.networx
- Credentials: scope=dl-prod-xflow-kv-scope, key=logon-kafka-prod
- Starting offsets: LATEST
- Source file format: CSV

**Schema**
- KAFKA_OP_TYPE string
- NETWORX_ID decimal(19,0)
- CIRCUIT_ID string
- ORDER_ID decimal(19,0)
- PRODUCT_TYPE string
- STATUS string

Partition by load_dt (generated).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/kafka_networx
- Format: Parquet
- Write mode: append

**Transformations:**
- load_ts: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- load_dt: generated SYSDATE, format "yyyyMMdd"

**Global transformation:**
- Replace "", "NULL" with Null

**No validations, no error handling overrides.**

**Schedule:** every hour

**Metadata**
- Application: bpmrd
- Feed name: STG_kafka_networx
- Feed type: ING
- Support team: ecdw
- Created by: us2472@att.com
- Contact: DL-GCP_ADBA@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 30831
```

---

## S-04d — Kafka → CSV + transforms, no GT, partitioned (105 configs)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667,dicore-prod-01-gg-kafka2.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: GIOM.IOMDBO.CP_NC3_CIRCUIT_1
- Consumer group: com.att.kafka.azure.bpmrd.cp_nc3_circuit_1
- Credentials: scope=dl-prod-xflow-kv-scope, key=logon-kafka-prod
- Starting offsets: LATEST
- Source file format: CSV

**Schema**
- KAFKA_OP_TYPE string
- KAFKA_TABLE_NAME string
- CP_NC3_CIRCUIT_ID decimal(19,0)
- CIRCUIT_ID string
- PROVIDER string
- STATUS string

Partition by load_dt (generated).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/kafka_cp_nc3_circuit
- Format: CSV
- Write mode: append

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- load_dt: generated SYSDATE, format "yyyyMMdd"

**No validations, no global transform, no error handling overrides.**

**Schedule:** every hour
**Retain source files for 7 days.**

**Metadata**
- Application: bpmrd
- Feed name: STG_kafka_cp_nc3_circuit
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: DL-GCP_ADBA@att.com
- Data Library: DP-DLIB-OrdPE
- Rim Policy: NET-300
- Mots ID: 30831
```

---

## S-04e — Kafka → Parquet + transforms, no GT, partitioned (102 configs)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667,dicore-prod-01-gg-kafka2.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: EDF.NC3_ASSET_EQP
- Consumer group: com.att.kafka.azure.bpmrd.nc3_asset_eqp
- Credentials: scope=dl-prod-xflow-kv-scope, key=logon-kafka-prod
- Starting offsets: LATEST
- Source file format: CSV

**Schema**
- KAFKA_OP_TYPE string
- ASSET_EQP_ID decimal(19,0)
- EQUIP_TYPE string
- SERIAL_NUM string
- STATUS string

Partition by load_dt (generated).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/kafka_nc3_asset_eqp
- Format: Parquet
- Write mode: append

**Transformations:**
- load_ts: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- load_dt: generated SYSDATE, format "yyyyMMdd"

**No validations, no global transform, no error handling overrides.**

**Schedule:** every hour

**Metadata**
- Application: bpmrd
- Feed name: STG_kafka_nc3_asset_eqp
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 18200
```

---

## S-04i — Kafka → GT + errorHandling (78 configs)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667,dicore-prod-01-gg-kafka2.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: GPS.SWBAPPS_AT_ATTRIBUTES
- Consumer group: com.att.kafka.azure.bpmrd.swbapps_attributes
- Credentials: scope=dl-prod-xflow-kv-scope, key=logon-kafka-prod
- Starting offsets: LATEST
- Source file format: CSV

**Schema**
- KAFKA_OP_TYPE string
- ATTR_ID string
- ATTR_NAME string
- ATTR_VALUE string
- STATUS string

Partition by load_dt (generated).

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/kafka_swbapps_attributes
- Format: Delta (Unity Catalog: catalog=30636_azuredl_prd, schema=bpmrd)
- Write mode: append

**Transformations:**
- LOAD_TS: generated SYSDATETIME, format "yyyy/MM/dd hh:mm:ss"
- load_dt: generated SYSDATE, format "yyyyMMdd"

**Global transformation:**
- Trim spaces
- Replace "", "NULL", "null" with Null

**Error handling:**
- Standard: fail on error, skip malformed, bad file

**No validations.**

**Schedule:** every hour

**Metadata**
- Application: bpmrd
- Feed name: STG_kafka_swbapps_attributes
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 20100
```

---

## S-04g — Kafka → JSON target + transforms (4 configs)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667,dicore-prod-01-gg-kafka2.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: TDATA.IM_HNM_DATA
- Consumer group: com.att.kafka.azure.bpmrd.im_hnm_data
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
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/kafka_im_hnm_data
- Format: JSON
- Write mode: append

**Transformations:**
- data_dt: generated SYSDATE, format "yyyyMMdd"

**No validations, no global transform, no error handling overrides.**

**Schedule:** every 15 minutes (0 0/15 * * * ?)

**Metadata**
- Application: bpmrd
- Feed name: STG_kafka_im_hnm_data
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-NetC
- Rim Policy: NET-300
- Mots ID: 31500
```

---

## S-04f — Kafka → CSV append, no transforms (2 configs)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667,dicore-prod-01-gg-kafka2.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: EDM.ORDER_GRAPH_AEH_EAST
- Consumer group: com.att.kafka.azure.bpmrd.order_graph_aeh
- Credentials: scope=dl-prod-xflow-kv-scope, key=logon-kafka-prod
- Starting offsets: LATEST
- Source file format: CSV

**Schema**
- KAFKA_OP_TYPE string
- KAFKA_TABLE_NAME string
- ORDER_ID string
- ORDER_TYPE string
- ORDER_STATUS string
- CREATE_DATE string

No partitions.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/kafka_order_graph_aeh
- Format: CSV
- Write mode: append

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** every hour

**Metadata**
- Application: bpmrd
- Feed name: STG_kafka_order_graph_aeh
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: NET-300
- Mots ID: 31000
```

---

## S-04h — Kafka → kafkatext (raw text target) (2 configs)

```
/scaffold-xflow-orchestrator

- Source: Kafka streaming topic
- Bootstrap servers: dicore-prod-01-gg-kafka1.cr4po4qgy4pendudhmrguavfsf.cx.internal.cloudapp.net:6667
- Topic: EDM.ECMI
- Consumer group: com.att.kafka.azure.bpmrd.ecmi_raw
- Credentials: scope=dl-prod-xflow-kv-scope, key=logon-kafka-prod
- Starting offsets: LATEST
- Source file format: kafkatext (raw message stored as-is)

**Schema**
- data_dt string (partition column only — kafkatext stores raw message as-is, no data columns in schema)

Partition by data_dt.

**Target**
- Write to: abfss://bpmrd-stg@datalakeeastus2prd.dfs.core.windows.net/kafka_ecmi_raw
- Format: CSV (kafkatext requires csv target, not text)
- Write mode: append

**No transformations, no validations, no global transform, no error handling overrides.**

**Schedule:** every hour

**Metadata**
- Application: bpmrd
- Feed name: STG_kafka_ecmi_raw
- Feed type: ING
- Support team: datalake
- Created by: us2472@att.com
- Contact: us2472@att.com
- Data Library: DP-DLIB-AcctC
- Rim Policy: NET-300
- Mots ID: 31000
```
