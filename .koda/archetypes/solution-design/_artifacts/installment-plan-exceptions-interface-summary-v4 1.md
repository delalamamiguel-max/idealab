# Interface Summary Table — v4
## Epic: Installment Plan Exception Handling (BSSe/ACC)

**Version:** 4.0
**Epic Scope:** C01 · C02 · C03 · C06 · C07 · C08 · C09 · C10 · C18
**Source Graph:** `dependency_graph_cleaned.json` · 2,340 relationships within BFS cutoff=2
**Companion Document:** `installment-plan-exceptions-application-summary-v4.md`

---

### Interface Type Legend

| Type | Meaning |
|---|---|
| **API** | Synchronous REST/SOAP service call |
| **Event** | Asynchronous event publication (Kafka, ISBUS topic, etc.) |
| **Batch** | Scheduled file or batch data exchange |
| **mS** | Microservice-to-microservice interaction (legacy SI shorthand) |

---

## Interface Summary Table

### Core Exception Orchestration Interfaces

| Source | Target | Interface Name | Type | Description | Impact Type | LoE | Graph Evidence |
|---|---|---|---|---|---|---|---|
| BSSe-ACF | ILS | Loan Lifecycle Operations | API | Initiates loan acceleration, cancellation, reinstatement, and status updates for all exception scenarios (C01–C09). New lifecycle states: termination-by-non-payment, death/military suspension, forced acceleration, reinstatement. | Enhance | Complex (ILS) | hop=1 · edges 5cd88603c473279b, 4762d05db783c6b0 |
| BSSe-ACF | ASPEN | GL Accounting Entry | API | Posts accounting journal entries to GL for loan acceleration events and death/military deployment scenarios (C01, C02, C03, C08). New entry types required for each exception category. | Enhance | Moderate | hop=1 · edge 46880832acd2bf54 |
| BSSe-ACF | BSSe-RTB | Billing Update Event | Event | Triggers real-time billing adjustments on loan acceleration and subscriber change exceptions (C01, C06, C07, C08). New exception reason codes added to existing event payload. | Enhance | Easy | hop=1 · edges bad67248c23f9d71, 37bcd02e3f9c4c0e |
| BSSe-ACF | BSSe-SkyFM | Customer Notification Event | Event | Publishes customer-facing notification events for all exception scenarios requiring customer communication (C01, C02, C03, C06, C07). New notification templates per exception type. | Enhance | Moderate | hop=1 · edges 68579137831092dc, c097b80cae4a1c30 |
| BSSe-ACF | OCE | Loan Modification Orchestration | API | Coordinates OCE loan management operations for subscriber changes, service cancellation, and reinstatement flows (C06, C07, C09). Routes to OCE LoanManagementMs and ExternalEventHandlerMs. | Enhance | Easy | hop=1 · edge f7236f0996a3f7d3 |
| BSSe-ACF | CFM | Customer Financial Update | API | Sends financial management updates for service cancellation billing and forced acceleration payment adjustments (C07, C08). New exception states for CFM payment records. | Enhance | Moderate | hop=1 · edges b30670e49dfe96b9, 30546ed66bb2e83c |
| BSSe-ACF | IDP-Customer Graph Cloud | Customer Data Query | API | Retrieves customer account data for death/no-TOBR eligibility checks and subscriber change identity validation (C02, C06). Read-only; includes CustomerGraphProductMs `GET /installments` call path. | Enhance | Moderate | hop=1 · edges 9c1ed463f91abc33, 15637c924adad2a7 |
| BSSe-ACF | CAPM | Payment Plan Management | API | Manages payment plans for service cancellation payoff, forced acceleration balance settlement, and reinstatement payment schedules (C07, C08, C09). | Enhance | Moderate | hop=1 · edge d0ef5da6260741ce |
| BSSe-ACF | IDP-BUPS | Billing Validation | API | Validates loan modification states, outstanding balances, and payment eligibility before exception processing commits (C06, C07, C09). | Enhance | Moderate | hop=1 · edges 1f48ea028f1601b7, e0cfb04b1f0e0ddc |
| BSSe-ACF | ISBUS | Loan Exception Event Routing | Event | Routes loan exception lifecycle events through integration service bus for downstream consumer notification (C01–C10). Regression test only — no new interface work. | No Change | Non-Development | hop=0 (ISBUS seed) · edge 2b9be72b76c1a7d1 |

---

### ILS Downstream Interfaces

| Source | Target | Interface Name | Type | Description | Impact Type | LoE | Graph Evidence |
|---|---|---|---|---|---|---|---|
| ILS | BSSe-MMap | Loan Status Financial Map Event | Event | Pushes accelerated, cancelled, and reinstated loan financial data to BSSe-MMap for RECON PLUS reconciliation and C18 audit reporting (C01, C08, C09, C18). New loan exception status codes required. | Enhance | Difficult | hop=1 · edges c2bb5bded261e70a, cf3cec5864520680 |
| ILS | ISBUS | ILS Lifecycle Event | Event | Publishes ILS loan state change events onto ISBUS for downstream consumers (C01–C10). Existing routing; regression testing only. | No Change | Non-Development | hop=0 (both seeds) · edges ca905efc7f77418f, 7a4e0f38045bacde |
| ILS | CorpFin-Integration | GL Journalization Feed | API | Sends ILS exception transaction records (CIPID, amounts, dates) to CorpFin-Integration for GL journalization and SOX audit trail (C01, C08). Integration test only — no code changes to ILS interface. | Test | Test | hop=1 · edge 8880029e0e2a18c0 |
| ILS | DPG - Customer & Accounts | Loan Exception Data Product Feed | Batch | Delivers accelerated/reinstated loan data to DPG-C&A data product for C18 operational reporting and executive dashboards (C18). New exception loan status fields added to feed. | Enhance | Moderate | hop=1 · edge 952e8c4211851ce9 |
| BSSe-MMap | ASPEN | Accounting Reconciliation Feed | Batch | Feeds BSSe-MMap-reconciled financial data to ASPEN GL for exception transaction posting and period-close reconciliation (C01, C08). New exception transaction type codes. | Enhance | Difficult | hop=1 (BSSe-MMap) + hop=0 (ASPEN) · edge 8fb15a0ce35216d1 |

---

### OCE Orchestration Interfaces

| Source | Target | Interface Name | Type | Description | Impact Type | LoE | Graph Evidence |
|---|---|---|---|---|---|---|---|
| BSSe-NEO | OCE | Exception Order Initiation | API | Initiates loan exception order workflows from BSSe-NEO core platform into OCE for subscriber changes, service cancellation, and reinstatement (C06, C07, C09). New exception order types. | Enhance | Moderate | hop=1 · edges 51567bb83fa35ac7, 1e864959aafb3e2f |
| OCE (LoanManagementMs) | ILS | Loan Accelerate / Cancel / Reinstate | mS | OCE LoanManagementMs calls ILS to execute `accelerate`, `reverseAcceleration`, and `cancel` operations on installment loan records (C01, C06, C07, C08, C09). Confirmed via OCE-Bsse-Platform-Summary.md. | Enhance | Complex (ILS) | hop=1 (OCE) + hop=0 (ILS seed) · SI evidence: OCE-Bsse-Platform-Summary.md |
| OCE (LoanManagementMs) | IDP-DTAP | CIPID / CTN Update | API | Updates CIPID/CTN binding on loan record when subscriber CTN changes (C06) or reinstated loan requires new CTN association (C09). Called by both LoanManagementMs and NumberManagementMs. | Enhance | Easy | hop=0 (IDP-DTAP seed) · SI evidence: OCE-Bsse-Platform-Summary.md (v3 new) |
| OCE | BSSe-OC | Order Submission | API | Submits subscriber change, service cancellation, and reinstatement orders from OCE order management to BSSe-OC order hub (C06, C07, C09). Existing interface; new exception order types added. | Enhance | Easy | hop=0 (BSSe-OC seed) · edges 0008a983a9a8272b, add0a9619ce7a161 |
| OCE (ExternalEventHandlerMs) | IDP-OMNI-ODS | Cancel-Order Event | Event | Delivers cancel-order / remove-line events to ODS for service cancellation line processing (C07). Existing cancel flow fires automatically; ODS interface requires no code changes. | TestSupport | TestSupport (TSO) | hop=1 (IDP-OMNI-ODS) · edge 396ef2459762ee6b (SCOR→IDP-OMNI-ODS) · OCE-Bsse-Platform-Summary.md |
| OCE | SCOR | Supply Chain Notification Event | Event | Notifies SCOR supply chain orchestrator for device handling on customer death scenarios and device return workflows (C02, C10). New exception event types for death and rate/feature change returns. | Enhance | Moderate | hop=1 (SCOR) · SI evidence: SI 1279127 |

---

### Supply Chain Interfaces

| Source | Target | Interface Name | Type | Description | Impact Type | LoE | Graph Evidence |
|---|---|---|---|---|---|---|---|
| SCOR | ORACLE SCM | Device Return Orchestration | API | Orchestrates device return logistics and supply chain operations for customer death and rate/feature change scenarios (C02, C10). SCOR routes return instructions to Oracle SCM fulfillment. | Enhance | Moderate | hop=1 (both) · edge da9df3c2035cb91d |
| ORACLE SCM | DPG - Orders & Supply Chain | Supply Chain Data Product Feed | Batch | Feeds Oracle SCM device return and supply chain event data to DPG-Orders&SC data product for C18 exception reporting (C02, C10, C18). | Enhance | Easy | hop=1 (ORACLE SCM) · edge e10a84a2dc671a7e |

---

### Billing Interfaces

| Source | Target | Interface Name | Type | Description | Impact Type | LoE | Graph Evidence |
|---|---|---|---|---|---|---|---|
| BSSe-RTB | BSSe-ACF | Billing Exception Notification | Event | Notifies BSSe-ACF of billing state changes to trigger exception handling orchestration (C01, C06, C07, C08). Reverse feedback loop from billing subsystem. | Enhance | Easy | hop=0 (BSSe-RTB seed) + hop=1 (BSSe-ACF) · edge 1120e46dabd0585a |
| BSSe-RTB | BSSe-BB | Bill Presentation Update | Event | Sends updated billing records to BSSe-BriteBill for customer bill presentation on exception scenarios (C01, C06, C07). Existing interface; test validation only. | Test | Test | hop=0 (BSSe-RTB seed) + hop=1 (BSSe-BB) · edge ab5356dca3cd447d |
| BSSe-RTB | ISBUS | Billing Event | Event | Routes real-time billing events through ISBUS for downstream subscriber billing notification (C01, C06, C07, C08). No changes; regression testing only. | No Change | Non-Development | hop=0 (both seeds) · edge dac3329b1b7366ac |
| CFAS-CS | ASPEN | Corporate Finance Entry | API | Sends corporate financial accounting entries for loan acceleration events from CFAS-CS to ASPEN GL (C01, C08). New exception entry types for termination-by-non-payment and forced acceleration. | Enhance | Moderate | hop=1 (CFAS-CS) + hop=0 (ASPEN) · edge 4113048c5b706ba6 |

---

### Finance & Reporting Interfaces

| Source | Target | Interface Name | Type | Description | Impact Type | LoE | Graph Evidence |
|---|---|---|---|---|---|---|---|
| ILS | RECON PLUS | ILS CIPID Transaction Detail Feed | Batch | Delivers ILS exception transaction CIPID details to RECON PLUS for Oracle AR reconciliation and C18 audit (C18). New exception transaction codes required. | Enhance | Moderate | SI app table · SI 1279103 |
| CorpFin-Integration | CorpFin-GL | GL Journalization | API | Integration testing for GL journal entry flow from ILS exception transactions through CorpFin-Integration into CorpFin-GL (C01, C08). No code changes to interface. | Test | Test | hop=1 (CorpFin-Integration) + hop=2 (CorpFin-GL) · via ILS edge 8880029e0e2a18c0 |
| CFM | DPG - Finance | Finance Data Product Feed | Batch | Journalization feed from CFM to DPG-Finance for ILS billed exception records supporting C18 financial reporting (C18). New exception billing record types. | Enhance | Easy | hop=1 (both) · via BSSe-ACF chain |
| BSSe-MMap | RECON PLUS | Reconciliation Summary Feed | Batch | Provides BSSe-MMap financial reconciliation summary to RECON PLUS for period-close exception validation (C01, C08, C18). | Enhance | Moderate | hop=1 (BSSe-MMap) · SI app table · SI 1279103 |
| IDP-CTX-Evt-HUB | BSSe-OC | Subscriber Change Context Event | Event | Publishes subscriber context events to BSSe-OC for order state validation on CTN change and service cancellation flows (C06, C07). Test validation only. | Test | Test | hop=1 (IDP-CTX-Evt-HUB) + hop=0 (BSSe-OC seed) · edge 84a01379999ddd33 |

---

## Interface Summary Statistics

| Metric | Count |
|---|---|
| **Total Interfaces** | **25** |
| Enhance | 16 |
| Test | 4 |
| TestSupport | 1 |
| No Change | 4 |
| **API** | 12 |
| **Event** | 10 |
| **Batch** | 3 |
| **mS** | 1 (OCE LoanManagementMs → ILS) |
| **Complex LoE** | 2 (ILS interfaces) |
| **Difficult LoE** | 2 (ILS→BSSe-MMap, BSSe-MMap→ASPEN) |
| **Moderate LoE** | 7 |
| **Easy LoE** | 5 |
| **Test LoE** | 4 |
| **TestSupport (TSO)** | 1 |
| **Non-Development** | 3 |
| **Graph Evidence — edge_id confirmed** | 20 |
| **Graph Evidence — SI evidence only** | 5 |

---

## Key Interface Chains by Capability

```
C01 – Terminate due to Non-payment
  BSSe-ACF → ILS (Loan Lifecycle Operations API)
  BSSe-ACF → BSSe-RTB (Billing Update Event)
  BSSe-ACF → ASPEN (GL Accounting Entry API)
  CFAS-CS → ASPEN (Corporate Finance Entry API)
  ILS → BSSe-MMap (Loan Status Financial Map Event)
  BSSe-ACF → BSSe-SkyFM (Customer Notification Event)
  BSSe-RTB → BSSe-ACF (Billing Exception Notification)

C02 – Customer Death / No TOBR
  BSSe-ACF → IDP-CG (Customer Data Query API)
  BSSe-ACF → ASPEN (GL Accounting Entry API)
  OCE → SCOR (Supply Chain Notification Event)
  SCOR → ORACLE SCM (Device Return Orchestration API)
  BSSe-ACF → BSSe-SkyFM (Customer Notification Event)

C03 – Military Deployment
  BSSe-ACF → ASPEN (GL Accounting Entry API)
  BSSe-ACF → BSSe-SkyFM (Customer Notification Event)

C06 – Subscriber (CTN) Changes
  BSSe-NEO → OCE (Exception Order Initiation API)
  OCE → BSSe-OC (Order Submission API)
  OCE (LoanMgmtMs) → IDP-DTAP (CIPID/CTN Update API)
  BSSe-ACF → BSSe-RTB (Billing Update Event)
  BSSe-ACF → BSSe-SkyFM (Customer Notification Event)
  BSSe-ACF → IDP-BUPS (Billing Validation API)

C07 – Subscriber (CTN) Service Cancellation
  BSSe-ACF → OCE (Loan Modification Orchestration API)
  OCE → BSSe-OC (Order Submission API)
  OCE (ExternalEventHandlerMs) → IDP-OMNI-ODS (Cancel-Order Event)
  BSSe-ACF → CFM (Customer Financial Update API)
  BSSe-ACF → BSSe-RTB (Billing Update Event)
  BSSe-ACF → BSSe-SkyFM (Customer Notification Event)

C08 – Forced Acceleration
  BSSe-ACF → ILS (Loan Lifecycle Operations API)
  BSSe-ACF → ASPEN (GL Accounting Entry API)
  BSSe-ACF → CAPM (Payment Plan Management API)
  ILS → BSSe-MMap (Loan Status Financial Map Event)
  ILS → CorpFin-Integration (GL Journalization Feed)

C09 – Reinstate Installment Loans
  BSSe-ACF → ILS (Loan Lifecycle Operations API)
  OCE (LoanMgmtMs) → IDP-DTAP (CIPID/CTN Update API)
  BSSe-ACF → CAPM (Payment Plan Management API)
  BSSe-ACF → IDP-BUPS (Billing Validation API)

C10 – Device Returns due to Rate/Feature Changes
  OCE → SCOR (Supply Chain Notification Event)
  SCOR → ORACLE SCM (Device Return Orchestration API)
  ORACLE SCM → DPG-Orders&SC (Supply Chain Data Product Feed)

C18 – Reporting and Audit
  ILS → RECON PLUS (ILS CIPID Transaction Detail Feed)
  ILS → DPG-C&A (Loan Exception Data Product Feed)
  CFM → DPG-Finance (Finance Data Product Feed)
  BSSe-MMap → RECON PLUS (Reconciliation Summary Feed)
  ILS → CorpFin-Integration (GL Journalization Feed)
```

---

## Notes

1. **Interface LoE** reflects the effort for the *interface change*, not the full system LoE. ILS system LoE is Complex; individual ILS interfaces may vary.
2. **Edge IDs** are from `dependency_graph_cleaned.json`. Where multiple edges exist between the same source/target pair, the first confirmed edge_id is cited.
3. **SI evidence** notation means the interface was identified via the past SI document app tables (`si_dependency_graph.json` or past SIs in `past_solution_intents/`) rather than directly confirmed by a graph edge between the two systems.
4. **OCE LoanManagementMs → ILS**: Confirmed via OCE-Bsse-Platform-Summary.md microservice catalog. The OCE→ILS graph path exists via the BSSe-ACF→ILS chain; no direct OCE→ILS edge in the cleaned graph, but the interface is architecturally confirmed.
5. **notifyNow excluded**: Per Step 6 exclusion rule. BSSe-SkyFM is the customer-facing notification interface surface; notifyNow is downstream infrastructure with No Change scope.
