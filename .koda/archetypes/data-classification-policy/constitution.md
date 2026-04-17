# Data Classification Policy Constitution

## Purpose

Establishes guardrails for governing Sensitive Personal Information (SPI) and Personally Identifiable Information (PII) in accordance with AT&T data classification policy, regulatory mandates, and zero-trust security posture.

---

## Scope: What Constitutes a Violation

### ✅ **NOT Violations (Metadata/Schema References)**

The following scenarios **do NOT** constitute data leakage and should be **dismissed** during compliance reviews:

- **Variable names** containing SPI/PII terms (e.g., `email_address`, `customer_ssn`, `ban_column`)
- **Column names** in DataFrames or SQL schemas (e.g., `df['email']`, `SELECT account_id FROM...`)
- **File names** that reference data types (e.g., `process_email_addresses.py`, `ban_lookup_table`)
- **DataFrame names** or table identifiers (e.g., `email_df`, `customer_account_table`)
- **Function/method parameters** named after data types (e.g., `def anonymize_email(email_col)`)
- **Configuration keys** or schema definitions (e.g., `"email_field": "user_email"`)
- **Comments or documentation** describing SPI/PII fields without exposing values

**Rationale**: Metadata and schema identifiers are necessary for data engineering and do not expose actual sensitive values.

---

### 🔴 **VIOLATIONS (Actual Data Exposure)**

The following scenarios **DO** constitute violations and require remediation:

- **Hardcoded actual values** (e.g., `email = "john.doe@att.com"`, `ssn = "123-45-6789"`)
- **Display calls showing raw data** (e.g., `df.display()` exposing actual email addresses or BANs)
- **Logs containing real values** (e.g., `print(f"Processing email: {user_email}")` where `user_email` is a real address)
- **API calls with unmasked data** (e.g., sending 1,000 rows with real customer IDs to external service)
- **CSV/files in Git with actual values** (e.g., `customer_data.csv` containing real names, emails, BANs)
- **Test fixtures with production data** (e.g., mock data using real customer records)
- **Error messages exposing values** (e.g., `ValueError: Invalid email john@example.com`)

**Rationale**: Actual data values constitute real SPI/PII exposure and must be masked, tokenized, or pseudonymized.

---

### 📋 **Examples for Clarity**

| Scenario | Violation? | Explanation |
|----------|------------|-------------|
| `df = spark.read.table("customer_email")` | ❌ NO | Table name is metadata |
| `df.select("email", "phone")` | ❌ NO | Column selection is schema reference |
| `df.filter(col("ban").isNotNull())` | ❌ NO | Column name in filter logic |
| `df.filter(col("ban").isin(['12345', '67890']))` | ✅ YES | Hardcoded BAN values (actual data) |
| `print(f"Column: {email_col_name}")` | ❌ NO | Variable contains column name string |
| `df.display()` showing actual emails | ✅ YES | Displays raw data values |
| `email = "john.doe@att.com"` | ✅ YES | Hardcoded actual email value |
| `logger.info(f"User: {user_email}")` | ✅ YES | Logs real email if `user_email` is value |
| File name: `2023_policy_data_imsi.csv` | ❌ NO | Filename is metadata (must verify content) |
| File content: actual IMSI values in CSV | ✅ YES | File contains actual sensitive data |
| CSV with headers: `ban,email,account_id` | ❌ NO | Schema/column names only |
| CSV with classification tags: `CPNI;HSPI;CDR` | ❌ NO | Classification metadata, not customer data |
| `# Column: ban (Billing Account Number)` | ❌ NO | Comment describing schema |
| `raise ValueError(f"Invalid: {email}")` | ✅ YES | Error exposes actual value |

---

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** any solution that:

- ✘ **Lacks classification mapping**: Do not process datasets without an explicit SPI/PII inventory, owner approval, and policy alignment documented.
- ✘ **Violates least privilege**: Reject architectures that grant standing access to SPI/PII beyond the minimum required service identities.
- ✘ **Bypasses encryption**: Refuse designs that omit AES-256 at rest and TLS 1.2+ in transit, or that expose raw SPI/PII in logs, caches, or test fixtures.
- ✘ **Ignores consent/legal basis**: Do not proceed if data usage lacks recorded consent, contractual right, or regulatory justification (e.g., CPNI, GDPR, CCPA).
- ✘ **Skips breach response plans**: Reject deployments without incident playbooks, DLP monitors, and defined notification SLAs for policy violations.

## II. Mandatory Patterns (Must Apply)

The LLM **must** ensure:

- ✔ **Data minimization** with field-level masking, tokenization, or pseudonymization for SPI/PII before analytics workloads.
- ✔ **Automated classification** tags propagated through data catalogs, lineage graphs, and CI/CD guardrails.
- ✔ **Access governance** via Just-In-Time elevation, Privileged Access Workstations, and auditable approval workflows.
- ✔ **Continuous monitoring** using SIEM alerts, anomaly detection, and DLP policies tied to AT&T classification tiers.
- ✔ **Retention enforcement** with automated purge schedules, legal holds, and archival encryption keys rotated per policy cadence.
- ✔ **Third-party assurances** requiring DPAs, SOC 2 reports, and zero-trust controls before sharing SPI/PII externally.
- ✔ **Comprehensive audit trails** capturing who accessed SPI/PII, when, why, and through which service path.

## III. Preferred Patterns (Recommended)

The LLM **should** adopt:

- ➜ **Privacy-by-design templates** embedding classification checkpoints in solution review boards and architecture diagrams.
- ➜ **Synthetic data sandboxes** that replace SPI/PII during development and testing to limit blast radius.
- ➜ **Attribute-based access control** (ABAC) layered with device posture and geofencing signals for SPI/PII stores.
- ➜ **Automated policy drift detection** comparing live configurations against codified AT&T data classification baselines.
- ➜ **Secure analytics patterns** leveraging privacy-enhancing technologies (e.g., differential privacy, secure enclaves) when analyzing SPI/PII.
- ➜ **Stakeholder scorecards** that track compliance KPIs, remediation backlog burn-down, and security debt tied to SPI/PII assets.

## IV. SPI/PII Classification Inventory (Top 40)

Derived from `TOP_SPI_PII_classifications.csv`, the following nodes are designated SPI/PII and must inherit the hard-stop and mandatory controls above. Flags reference policy dimensions (CD-SS, CPNI, SPI, HSPI, PSPI, PI, PCI) and residual risk tiers (RSKLVL_0-3).

**Flag Legend**
- CD-SS: Consent Decree Sunday Sky
- CPNI: Customer Proprietary Network Information
- SPI: Sensitive Protected Information
- HSPI: Highly Sensitive Protected Information
- PSPI: Privacy Sensitive Protected Information
- PI: Personally Identifiable Information
- PCI: Payment Card Information
- RSKLVL_0-3: Residual risk levels (0 = lowest, 3 = highest)

**Electronic Network Activity**
- Email Content | Flags: CD-SS, SPI, HSPI, RSKLVL_1
- Text Message Content | Flags: CD-SS, CPNI, SPI, HSPI, RSKLVL_1
- Call Detail (time, date, duration, disposition) | Flags: CD-SS, CPNI, SPI, HSPI, PSPI, RSKLVL_1
- Browsing URLs and Clickstream Data | Flags: SPI, HSPI, RSKLVL_1
- Web browsing information | Flags: SPI, HSPI, RSKLVL_1

**Geolocation**
- Coarse Location (lat/long 0-2 decimal places) | Flags: SPI, RSKLVL_2
- Latitude and Longitude – GPS level (≥ 3 decimal places) | Flags: CD-SS, SPI, HSPI, PSPI, RSKLVL_1
- Latitude, Longitude, and Altitude – GPS level | Flags: CD-SS, SPI, HSPI, PSPI, RSKLVL_1
- Zip code plus four digits | Flags: CD-SS, SPI, HSPI, PSPI, RSKLVL_1

**Identifiers**
- ICCID (Integrated Circuit Card Identifier) | Flags: SPI, HSPI, RSKLVL_1
- Access Credentials for mobile account | Flags: CD-SS, SPI, PSPI, RSKLVL_1
- Account User Name | Flags: PI, RSKLVL_3
- Billing Account Number (BAN) | Flags: PI, RSKLVL_3
- Birth Certificate Number | Flags: CD-SS, SPI, PSPI, RSKLVL_1
- Card Verification Code (CVV, CVC2, CID, CVV2) | Flags: CD-SS, SPI, PCI, RSKLVL_1
- Cardholder Name | Flags: CD-SS, PI, PCI, RSKLVL_3
- Credential Hint | Flags: CD-SS, SPI, PSPI, RSKLVL_1
- Credit Card Number (PAN) | Flags: SPI, PCI, RSKLVL_1
- Driver License Number | Flags: CD-SS, SPI, PSPI, RSKLVL_1
- Email Address | Flags: PI, RSKLVL_3
- Expiration Date | Flags: CD-SS, PI, PCI, RSKLVL_3
- Full Name | Flags: PI, RSKLVL_3
- IMEI | Flags: PI, RSKLVL_3
- IMSI | Flags: PI, RSKLVL_3
- IP Address | Flags: PI, RSKLVL_3
- Mobile Account PIN Data | Flags: CD-SS, SPI, PSPI, RSKLVL_1
- MSISDN (Mobile Subscriber International Directory Number) | Flags: PI, RSKLVL_3
- Passport Number | Flags: CD-SS, SPI, PSPI, RSKLVL_1
- Password | Flags: CD-SS, SPI, PSPI, RSKLVL_1
- PIN | Flags: CD-SS, SPI, PSPI, PCI, RSKLVL_1
- Postal Full Address | Flags: CD-SS, PI, RSKLVL_3
- Social Security Number | Flags: CD-SS, SPI, PSPI, RSKLVL_1

**Protected Characteristics**
- Date of Birth (MM/DD/YYYY) | Flags: CD-SS, SPI, PSPI, RSKLVL_1
- Gender Identity | Flags: SPI, HSPI, RSKLVL_0
- Ethnicity | Flags: CD-SS, SPI, HSPI, PSPI, RSKLVL_1
- Nationality | Flags: CD-SS, SPI, HSPI, PSPI, RSKLVL_1
- Religious Belief | Flags: CD-SS, SPI, HSPI, PSPI, RSKLVL_0
- Skin Color | Flags: CD-SS, SPI, HSPI, PSPI, RSKLVL_1
- Political Affiliations | Flags: CD-SS, SPI, HSPI, PSPI, RSKLVL_0
- Political Opinions | Flags: CD-SS, SPI, HSPI, PSPI, RSKLVL_0

> Note: Source file enumerates 40 high-priority SPI/PII elements. Update this inventory in lockstep with taxonomy revisions to avoid configuration drift.

---

**Version**: 1.1.0
**Last Updated**: 2025-11-20
**Changelog**: Added "Scope: What Constitutes a Violation" section to distinguish metadata/schema references from actual data exposure
