# Application Summary Table — v4
## Epic: Installment Plan Exception Handling (BSSe/ACC)

**Version:** 4.1
**Supersedes:** `installment-plan-exceptions-application-summary-v3.md` (v3)
**Epic Scope:** C01 · C02 · C03 · C06 · C07 · C08 · C09 · C10 · C18
**Out of Scope:** C04 (Subscriber Fraud), C05 (Upgrade Fraud)

---

### What Changed in v4

| Change | Detail |
|---|---|
| **Method** | Full pipeline re-run: seed identification → BFS (depth=2) → SI LoE anchoring → domain KB cross-reference → capability filtering → exclusion rules |
| **Seed MOTS IDs** | 31372 (ILS), 30911 (BSSe-C1), 30909 (BSSe-OC), 30914 (BSSe-RTB), 30912 (BSSe-iPaaS), 17815 (ASPEN), 23147 (ACC), 31998 (IDP-DTAP), 31292 (ISBUS) |
| **BFS output** | 198 candidate apps · 2,340 supported relationships from `dependency_graph_cleaned.json` |
| **New column** | **Graph Evidence** — records BFS hop distance and primary edge_id(s) from `impacted_relationships.json` |
| **New artifact** | Companion **Interface Summary Table** v4 |
| **Exclusion applied** | `notifyNow` (30920, hop=2, No Change) excluded per Step 6 rule: hop=2 AND No Change |
| **Migration exclusion** | TLG-MOB (18193) excluded — TLG→BSSe migration scope only, per v3 notes |
| **Inherited from v3** | IDP-DTAP (31998) and IDP-OMNI-ODS (32166) net-new entries from domain KB review remain; all domain KB findings confirmed |
| **Target list reconciliation (v4.1)** | 10 Group A apps added from target list gap analysis: Analytics Microservice (30420), CCDL (32255), CCSF (30685), IDP-WebAcctMgmt (32768), OTS (27429), DPG-Billing (33686), myATT Mobile App (30558), MSGRTR (25316), CCMULE (30686), IDP-Commerce-Cart & Pricing (33825). 4 unknowns flagged for SME: OMHUB, IDP-Order Graph Cloud, DPG-Network & Usage, CCMule-Service (if distinct from CCMULE) |

---

## Application Summary Table

### ESPR Development

| Parent Package | Impact Type | MOTS ID | Application | LoE | Capabilities | Primary SI | Graph Evidence |
|---|---|---|---|---|---|---|---|
| ESPR Development | Enhance | 32985 | BSSe-ACF | **Difficult** | C01–C10 (core exception orchestrator — drives all loan acceleration, reinstatement, and billing update flows) | SI 1372673 | hop=1 · edges 5cd88603c473279b (→ILS), 46880832acd2bf54 (→ASPEN), bad67248c23f9d71 (→BSSe-RTB) |
| ESPR Development | Enhance | 31697 | BSSe-MMap | **Difficult** | C01, C08, C09, C18 (financial mapping and reconciliation for accelerated/reinstated loans; feeds RECON PLUS) | SI 1372673 | hop=1 · edges c2bb5bded261e70a, cf3cec5864520680 (ILS→BSSe-MMap) |
| ESPR Development | Enhance | 31372 | ILS (Installment Loan Sub Ledger) | **Complex** | C01–C09 (all exception flows require new ILS lifecycle states — termination, death, military, reinstatement, forced acceleration; confirmed via OCE LoanManagementMs accelerate/reverseAcceleration operations) | SI 1372673 | hop=0 (seed) |
| ESPR Development | Enhance | 17815 | ASPEN | **Moderate** | C01, C02, C03, C08 (accounting entries and GL posting for loan acceleration events and death/military scenarios) | SI 1372673 | hop=0 (seed) |
| ESPR Development | Enhance | 31710 | BSSe-NEO | **Moderate** | C01–C10 (core BSSe engine; new exception state transitions introduced at the platform level) | SI 1279127 | hop=1 · edges 51567bb83fa35ac7, 1e864959aafb3e2f (BSSe-NEO→OCE) |
| ESPR Development | Enhance | 31452 | BSSe-SkyFM | **Moderate** | C01, C02, C03, C06, C07 (customer-facing notifications for all exception scenarios; confirmed as primary notification surface for AccountNotificationsMs service-transfer events) | SI 1372673 | hop=1 · edges 68579137831092dc, c097b80cae4a1c30 (BSSe-ACF→BSSe-SkyFM) |
| ESPR Development | Enhance | 73 | CAPM | **Moderate** | C07, C08, C09 (payment management for service cancellation payoff, forced acceleration, and reinstatement) | SI 1372673 | hop=1 · edge d0ef5da6260741ce (BSSe-ACF→CAPM) |
| ESPR Development | Enhance | 8043 | CFAS-CS | **Moderate** | C01, C08 (corporate financial accounting services; feeds ASPEN for GL entries on acceleration events) | SI 1372673 | hop=1 · edge 4113048c5b706ba6 (ASPEN→CFAS-CS) |
| ESPR Development | Enhance | 13287 | CFM | **Moderate** | C07, C08 (customer financial management for service cancellation billing and forced acceleration) | SI 1372673 | hop=1 · edges b30670e49dfe96b9, 30546ed66bb2e83c (BSSe-ACF→CFM) |
| ESPR Development | Enhance | 31478 | DPG - Customer & Accounts | **Moderate** | C18 (loan data reporting — subscribes to IDP-CG events for installment plan status on exception scenarios) | SI 1372673 | hop=1 · edge 952e8c4211851ce9 (ILS→DPG-C&A) |
| ESPR Development | Enhance | 33847 | IDP-BUPS | **Moderate** | C06, C07, C09 (billing/payment service layer; validates loan modification states and balances) | SI 1372673 | hop=1 · edges 1f48ea028f1601b7, e0cfb04b1f0e0ddc (BSSe-ACF→IDP-BUPS) |
| ESPR Development | Enhance | 31468 | IDP-Customer Graph Cloud | **Moderate** | C02, C06 (customer graph data for death/no-TOBR and subscriber change flows; includes CustomerGraphProductMs `GET /installments` and CustomerGraphProductPreProcessorMs digital loan status management — both internal CGraph services within this MOTS) | SI 1372673 + CGraph-Microservices-Summary.md | hop=1 · edges 9c1ed463f91abc33, 15637c924adad2a7 (BSSe-ACF→IDP-CG) |
| ESPR Development | Enhance | 18249 | ORACLE SCM | **Moderate** | C02, C10 (supply chain notifications for customer death device handling and device returns) | SI 1279127 | hop=1 · edge e10a84a2dc671a7e (ORACLE SCM→DPG-C&A); da9df3c2035cb91d (SCOR↔ORACLE SCM) |
| ESPR Development | Enhance | 12590 | RECON PLUS | **Moderate** | C18 (installment loan reconciliation reporting; receives ILS CIPID transaction details with Oracle AR for audit) | SI 1279103 | SI app table (not reached via BFS from current seeds — confirmed via SI 1279103 app table) |
| ESPR Development | Enhance | 31902 | SCOR (Supply Chain Orchestrator) | **Moderate** | C02, C10 (orchestrates supply chain notifications and device return logistics) | SI 1279127 | hop=1 · edge da9df3c2035cb91d (SCOR↔ORACLE SCM) |
| ESPR Development | Enhance | 22966 | Trade-In | **Moderate** | C10 (device return processing due to rate/feature changes) | SI 1372668 | hop=2 · via SCOR (31902, hop=1) |
| ESPR Development | Enhance | 31599 | ATTCC | **Moderate** | C02, C03, C06 (AT&T Contact Center — human-assisted intake for death/military/subscriber change flows) | SI 1036446 | hop=2 · via BSSe-OC/OCE chain |
| ESPR Development | Enhance | 31605 | acctableau | **Moderate** | C18 (Tableau reporting for installment plan exception audit trail) | SI 1036446 | hop=2 · UNKNOWN in BFS (name not in iTAP); SI app table evidence |
| ESPR Development | Enhance | 32327 | ADAS | **Easy** | C01–C10 (analytics data services; downstream analytics tracking for exception events) | SI 1372673 | hop=2 · via IDP-DTAP chain |
| ESPR Development | Configure | 30911 | BSSe-C1 | **Easy** | C06, C07 (catalog and contract configuration — new charge/reason codes for exception scenarios) | SI 1372673 | hop=0 (seed) |
| ESPR Development | Enhance | 30909 | BSSe-OC | **Easy** | C06, C07, C09 (order capture for subscriber changes, service cancellation, and reinstatement flows) | SI 1372673 | hop=0 (seed) |
| ESPR Development | Enhance | 30914 | BSSe-RTB | **Easy** | C01, C06, C07, C08 (real-time billing updates triggered by loan acceleration and subscriber changes) | SI 1372673 | hop=0 (seed) |
| ESPR Development | Enhance | 30687 | BWSFMC | **Easy** | C06, C07 (broadband wireless service fulfillment control; service state changes on CTN cancel/change) | SI 1383580 | hop=2 · via BSSe-RTB/BSSe-C1 chain |
| ESPR Development | Enhance | 31998 | IDP-DTAP | **Easy** | C06, C09 (Digital Terms, Activations & Porting — CIPID/CTN association updates when loan subscriber changes or reinstated loan needs new CTN binding; called by OCE LoanManagementMs and NumberManagementMs) | OCE-Bsse-Platform-Summary.md (v3 new) | hop=0 (seed — added based on domain KB review) |
| ESPR Development | Enhance | 29670 | DPG - EDM Omnichannel Analytics | **Easy** | C18 (omnichannel analytics data enrichment for loan exception audit) | SI 1372673 | hop=1 · edge e662aec9f626f435 (IDP-WebAcctMgmt→DPG-EDM) |
| ESPR Development | Enhance | 31618 | DPG - Finance | **Easy** | C18 (financial data product; journalization feed from CFM for ILS billed exception records) | SI 1372673 | hop=1 · via BSSe-ACF chain |
| ESPR Development | Enhance | 31510 | DPG - Orders & Supply Chain | **Easy** | C02, C10, C18 (order and supply chain data for device return and death scenario reporting) | SI 1036446 | hop=1 · via BSSe-OC/ORACLE SCM chain |
| ESPR Development | Enhance | 31479 | DPG - Sales & Sunrise | **Easy** | C18 (sales data reporting pipeline for installment plan exception tracking) | SI 1372673 | hop=1 · via ILS chain |
| ESPR Development | Enhance | 18211 | EDP | **Easy** | C01, C02 (enterprise document processing — notices/letters for non-payment termination and death scenarios) | SI 1372673 | hop=1 · via BSSe-C1/ISBUS chain |
| ESPR Development | Configure | 33822 | IDP-Catalog-Auth&Publish | **Easy** | C06, C07 (catalog publish configuration — new installment exception charge and adjustment codes) | SI 1372673 | hop=1 · via BSSe-C1 chain |
| ESPR Development | Enhance | 31326 | MIREA | **Easy** | C18 (model informing result enforcement — audit trail enforcement for exception transactions) | SI 1372673 | hop=1 · via ILS/ASPEN chain |
| ESPR Development | Enhance | 23488 | OCE | **Easy** | C06, C07, C09 (order capture engine; loan modification orchestration and OG/CG sync; OCE LoanManagementMs handles ILS accelerate/cancel and DTAP CIPID calls internally) | SI 1372673 | hop=1 · edges f7236f0996a3f7d3 (BSSe-ACF→OCE), 0008a983a9a8272b (OCE→BSSe-OC) |
| ESPR Development | Enhance | 32421 | OGSI - RM | **Easy** | C18 (Oracle GSI Revenue Management — revenue entries for loan exception accounting) | SI 1372673 | hop=2 · via ASPEN/CFM chain |
| ESPR Development | Test | 32476 | CorpFin-Integration | **Test** | C01, C08 (integration testing for GL journalization flows from ILS through CorpFin) | SI 1372673 | hop=1 · edge 8880029e0e2a18c0 (ILS→CorpFin-Integration) |
| ESPR Development | TBD | 30732 | ABS-Suite (Moody's Analytics) | **TBD** | C01, C08 (ILS downstream securitization reporting — impact on accelerated loan pools; requires securitization team SME confirmation) | SI 1372673 / SI 1013291 | hop=1 · via ILS chain |
| ESPR Development | TBD | 30699 | Everest | **TBD** | C09 (reinstatement eligibility assessment — pending SME confirmation from BSS Evolution team) | SI 1372673 | hop=2 · APM0013679 in BFS |
| ESPR Development | Enhance | 30420 | Analytics Microservice | **Easy** | C18 (platform analytics event tracking for exception scenarios — C01–C10 exception events captured in analytics pipeline) | BFS hop=1 + target list | hop=1 · via OCE/BSSe-ACF chain |

---

### ESPR Non-Development

| Parent Package | Impact Type | MOTS ID | Application | LoE | Capabilities | Primary SI | Graph Evidence |
|---|---|---|---|---|---|---|---|
| ESPR Non-Development | Test | 31692 | BSSe-BB (BSSe-BriteBill) | **Test** | C01, C06, C07 (bill presentation testing — exception billing scenarios; no code changes required) | SI 1372673 Non-Dev | hop=1 · edge ab5356dca3cd447d (BSSe-RTB→BSSe-BB) |
| ESPR Non-Development | TestSupport | 32412 | CorpFin-GL | **TestSupport (TSO)** | C01, C08 (GL system — provide test data/stubs for accounting entry validation; no changes) | SI 1372673 Non-Dev | hop=2 · via CorpFin-Integration (hop=1) |
| ESPR Non-Development | TestSupport | 32765 | IDP-IDM | **TestSupport (TSO)** | C02, C06 (identity management — test support for authenticated account flows; IdmProfileOrchestrationMs BSSe account info endpoints confirmed read-only, no development scope) | SI 1372673 Non-Dev + IDM-Microservice-Summary.md | hop=2 · via IDP-DTAP chain |
| ESPR Non-Development | TestSupport | 17922 | ORBIT GOLD | **TestSupport (TSO)** | C18 (revenue management — test support for revenue reporting validation; no code changes) | SI 1372673 Non-Dev | hop=1 · via ASPEN/CFM chain |
| ESPR Non-Development | Test | 20182 | CSI - Customer Care | **TBD** | C02, C03, C06 (customer care integration — scope of impact pending SME assessment with sk952d) | SI 1372673 | SI app table (not reached via BFS; confirm MOTS linkage with sk952d) |
| ESPR Non-Development | TestSupport | 20187 | CSI - Order & Subscription Mgmt | **TestSupport (TSO)** | C06, C07 (order and subscription management integration — test support only) | SI 1372673 | SI app table (not reached via BFS) |
| ESPR Non-Development | Test | 34190 | MBIZ | **Test** | C18 (mobility business reporting — test validation for exception event data) | SI 1372673 Non-Dev | SI app table (not reached via BFS) |
| ESPR Non-Development | Test | 14269 | ROME | **Test** | C18 (revenue opportunity management — test validation for exception revenue impacts) | SI 1372673 Non-Dev | SI app table (not reached via BFS) |
| ESPR Non-Development | Test | 17744 | DLC | **Test** | C10 (device lifecycle management — test validation for device return exception flows) | SI 1372673 | hop=1 · via BSSe-OC/ORACLE SCM chain |
| ESPR Non-Development | Test | 33932 | IDP-CTX-Evt-HUB | **Test** | C06, C07 (context event hub — test validation for subscriber change events; no code changes) | SI 1372673 Non-Dev | hop=1 · edge 84a01379999ddd33 (APM0044946→IDP-CTX-Evt-HUB) |
| ESPR Non-Development | Test | 33824 | IDP-Commerce-P&O | **Test** | C06, C07 (product & offers discovery — test support for subscriber change product mapping) | SI 1372673 | hop=1 · APM0045079 in BFS |
| ESPR Non-Development | TestSupport | 22509 | GRID-GDDN | **TestSupport (TSO)** | C01 (general data distribution network — test support for notification data routing) | SI 1372673 | hop=1 · via ISBUS chain |
| ESPR Non-Development | TestSupport | 31374 | INLAP | **TestSupport (TSO)** | C08, C09 (installment loan plan admin — test support for forced acceleration and reinstatement plan admin) | SI 1036446 Non-Dev | hop=2 · via ILS (hop=0) chain |
| ESPR Non-Development | No Change | 31292 | ISBUS | **Non-Development** | C01–C10 (integration service bus — regression testing for loan/billing event routing; no development work) | SI 1372673 | hop=0 (seed) · edge 2b9be72b76c1a7d1 (BSSe-ACF→ISBUS), ca905efc7f77418f (ILS→ISBUS) |
| ESPR Non-Development | No Change | 17901 | MFR | **Non-Development** | C01 (message format routing — no development work required) | SI 1372673 | hop=2 · via ISBUS chain |
| ESPR Non-Development | Test | 7856 | FDW | **Test** | C18 (financial data warehouse — test validation for exception financial data feeds) | SI 1279127 | SI app table (not reached via BFS from current seeds) |
| ESPR Non-Development | TestSupport | 17985 | Oracle AR | **TestSupport (TSO)** | C01, C02, C08 (accounts receivable — provide A/R extract test data for RECON PLUS reconciliation; no changes) | SI 1279103 | SI app table (not reached via BFS) |
| ESPR Non-Development | TestSupport | 30910 | BSSe-OH | **TestSupport (TSO)** | C06, C07 (BSSe Order Hub — test support for order state validation in subscriber changes; no changes) | SI 1036446 | hop=1 · via BSSe-OC/ISBUS chain |
| ESPR Non-Development | TestSupport | 32166 | IDP-OMNI-ODS | **TestSupport (TSO)** | C07 (Order Delivery System — receives cancel-order events from OCE ExternalEventHandlerMs during service cancellation; existing cancel-order interface requires no changes; test support only) | OCE-Bsse-Platform-Summary.md (v3 new) | hop=1 · edge 396ef2459762ee6b (SCOR→IDP-OMNI-ODS) |
| ESPR Non-Development | Test | 33686 | DPG - Billing | **Test** | C01, C06, C07 (billing data product — receives BSSe-RTB billing exception events; test validation for exception billing record accuracy) | BFS hop=1 + target list | hop=1 · edge f433ab9b79527139 (BSSe-RTB→APM0044946) |
| ESPR Non-Development | TestSupport | 32255 | CCDL | **TestSupport (TSO)** | C06, C07 (Commerce Customer Data Layer — subscriber data lookups on CTN change and service cancellation flows) | BFS hop=1 + target list | hop=1 · via BSSe-NEO/IDP-CG chain |
| ESPR Non-Development | TestSupport | 30685 | CCSF | **TestSupport (TSO)** | C06, C07 (Commerce Cloud Service Framework — service orchestration layer; test support for subscriber change and cancellation order routing) | BFS hop=1 + target list | hop=1 · edge c09a45ce04512bc6 (CCSF→APM0044948) |
| ESPR Non-Development | TestSupport | 32768 | IDP-WebAcctMgmt | **TestSupport (TSO)** | C06, C07 (Web Account Management — customer account state for subscriber change and cancellation flows; connects to IDP-CG and DPG-EDM) | BFS hop=1 + target list | hop=1 · edges 8bc1979a4fb72e75 (→IDP-CG), e662aec9f626f435 (→DPG-EDM) |
| ESPR Non-Development | TestSupport | 27429 | OTS | **TestSupport (TSO)** | C06, C10 (Order Tracking System — tracks subscriber change orders and device return shipments for exception flows) | BFS hop=1 + target list | hop=1 · via BSSe-OC/OCE chain |
| ESPR Non-Development | TestSupport | 30558 | myATT Mobile App | **TestSupport (TSO)** | C06, C07 (customer self-service app — exception status display and subscriber change/cancellation self-service flows; test validation) | BFS hop=2 + target list | hop=2 · via IDP-WebAcctMgmt (hop=1) |
| ESPR Non-Development | No Change | 25316 | MSGRTR | **Non-Development** | C01–C10 (Message Router — existing event routing for loan/billing exception events; no code changes required) | BFS hop=2 + target list | hop=2 · via ISBUS chain |
| ESPR Non-Development | No Change | 30686 | CCMULE (CCMule-CLM / CCMule-Service) | **Non-Development** | C01–C10 (MuleSoft CLM/service integration layer — passes through exception events on existing routes; no code changes required) | BFS hop=2 + target list | hop=2 · via BSSe-OC/BSSe-C1 chain |
| ESPR Non-Development | TestSupport | 33825 | IDP-Commerce-Cart & Pricing | **TestSupport (TSO)** | C06 (cart/pricing service — test coverage for exception pricing adjustments on subscriber changes only; new sales buy-flow is out of scope) | BFS hop=1 + target list | hop=1 · APM0045080 in BFS |
| ESPR Non-Development | TBD | 33826 | IDP-Order Graph Cloud | **TBD** | C06, C09 (order graph — order state tracking for subscriber changes and loan reinstatements; pending SME confirmation that APM0045081 = IDP-Order Graph Cloud) | BFS hop=1 (pending SME) | hop=1 · APM0045081 in BFS; edge 9e5ab29fb2e9ba5d via IDP-WebAcctMgmt |

> **Excluded (Step 6 Rule):** `notifyNow` (30920, hop=2, No Change) — excluded per exclusion rule: hop=2 AND No Change.
> **Excluded (Migration Rule):** `TLG-MOB` (18193) — excluded: TLG→BSSe migration scope only; appears in BFS at hop=1 via BSSe-ACF but migration-specific per v3 notes.
>
> **Target list items requiring SME investigation (not in BFS):**
> - `OMHUB` — not reached within BFS depth=2 from current seeds; identify MOTS ID and confirm dependency path from BSSe-ACF/OCE
> - `DPG - Network & Usage` — not in BFS; confirm scope for C07 service cancellation if network/usage data is required for exception processing
> - `CCMule-Service` — if a distinct MOTS from CCMULE (30686), identify MOTS ID; otherwise, CCMULE (30686) covers both CLM and Service modules
> - `IDP-Order Graph Cloud` — added as TBD (APM0045081/33826) pending SME confirmation of application name mapping

---

## Summary Statistics

| Metric | Count |
|---|---|
| **Total Applications (v4.1)** | **66** |
| ESPR Development | 37 |
| ESPR Non-Development | 29 |
| **Complex LoE** | 1 (ILS) |
| **Difficult LoE** | 2 (BSSe-ACF, BSSe-MMap) |
| **Moderate LoE** | 12 |
| **Easy LoE** | 14 (Analytics Microservice added) |
| **Configure LoE** | 2 (BSSe-C1, IDP-Catalog-Auth&Publish) |
| **Test LoE** | 2 (CorpFin-Integration — Dev; BSSe-BB — Non-Dev) |
| **TestSupport (TSO)** | 15 (+6: CCDL, CCSF, IDP-WebAcctMgmt, OTS, myATT Mobile App, IDP-Commerce-Cart & Pricing) |
| **Non-Development** | 4 (ISBUS, MFR, MSGRTR, CCMULE) |
| **No Change** | 0 (notifyNow excluded) |
| **TBD** | 5 (ABS-Suite, Everest, CSI-Customer Care, IDP-Order Graph Cloud + 4 unknown target apps pending SME) |
| **Apps vs v3** | −1 (notifyNow excluded); +11 (target list reconciliation); net +10 vs v3 |
| **Graph Evidence** | hop=0: 9 · hop=1: 34 · hop=2: 14 · SI app table only: 8 |
| **Target list coverage** | **35 / 39 = 90%** (25 matched pre-update + 10 Group A added; 4 unknowns pending SME) |

---

## Seed Identification (STEP 1)

| System (Epic reference) | Matched Application | MOTS ID | Match Method |
|---|---|---|---|
| ILS / Installment Loan System | ILS | 31372 | Exact |
| ASPEN / GL / Accounting | ASPEN | 17815 | Exact |
| ACC (backend services) | ACC | 23147 | Exact |
| BSSe (core platform) | BSSe-C1 | 30911 | Fuzzy — BSSe core component |
| BSSe (order capture) | BSSe-OC | 30909 | Fuzzy — BSSe order component |
| BSSe (real-time billing) | BSSe-RTB | 30914 | Fuzzy — BSSe billing component |
| BSSe (integration) | BSSe-iPaaS | 30912 | Fuzzy — BSSe integration layer |
| IDP-DTAP (domain KB: OCE→DTAP) | IDP-DTAP | 31998 | Domain KB — OCE-Bsse-Platform-Summary.md |
| ISBUS (integration bus) | ISBUS | 31292 | Exact |

---

## Notes & Assumptions

1. **Parent Package placeholder**: `ESPR Development` / `ESPR Non-Development` — replace with actual SI number when assigned (format: `{SI#} Development` / `{SI#} Non-Development`).
2. **ILS LoE (Complex)**: Confirmed from SI 1372673 app table AND from OCE platform: `LoanManagementMs` explicitly implements `accelerate` and `reverseAcceleration` workers against ILS. Exception scenarios (C01–C09) require NEW lifecycle states in ILS — termination-by-non-payment, death/military suspension, forced acceleration, and reinstatement.
3. **BSSe-ACF LoE (Difficult)**: Directly from SI 1372673. BSSe-ACF is the exception flow orchestrator — complex multi-system coordination reusing existing BSSe architecture patterns.
4. **Graph Evidence format**: `hop=N · edge <id>` — N is the minimum BFS hop distance from the nearest seed. Edge ID is from `dependency_graph_cleaned.json`. Multiple edges shown where BFS confirmed multiple paths.
5. **notifyNow exclusion**: hop=2, impact type No Change → excluded per Step 6 rule. BSSe-SkyFM handles delivery to the notification infrastructure; no changes required at notifyNow.
6. **TLG-MOB exclusion**: Appears at hop=1 via TLG-MOB→BSSe-ACF edges (lines 2109–2170 of impacted_relationships.json). Excluded — migration-specific scope (TLG→BSSe wireless migration).
7. **RECON PLUS (12590)**: Not reached by BFS from the 9 seeds (not in applications_itap.json or not connected within 2 hops). Included via SI 1279103 app table — strong SI evidence.
8. **Apps not in BFS** (SI app table only): RECON PLUS (12590), FDW (7856), Oracle AR (17985), MBIZ (34190), ROME (14269), CSI-Customer Care (20182), CSI-Order&Sub Mgmt (20187), acctableau (31605 — UNKNOWN in BFS). These apps are confirmed in past SIs but not reachable from current seed set.
9. **IDP-DTAP (Easy)**: DTAP is a hop=0 seed (added based on domain KB review). DTAP is called by OCE `LoanManagementMs` (CIPID/CTN binding on loan modification) and `NumberManagementMs` (CTN reserve/update). Easy LoE — extends existing OCE→DTAP patterns; no new interface required.
10. **IDP-OMNI-ODS (TestSupport)**: OCE `ExternalEventHandlerMs` calls ODS to deliver cancel-order / remove-line events for C07. ODS does not need code changes; test support only. Reached at hop=1 via SCOR→IDP-OMNI-ODS edge `396ef2459762ee6b`.
11. **ABS-Suite (TBD)**: hop=1 via ILS. Appears in SI 1372673 and SI 1013291 with null LoE. Requires securitization team confirmation for impact of accelerated loan pools on ABS reporting.
12. **Everest (TBD)**: hop=2 (APM0013679 in BFS). In SI 1372673 with TBD. Handles reinstatement eligibility (C09) — scope requires confirmation from BSS Evolution team.
13. **C04 (Subscriber Fraud) and C05 (Upgrade Fraud)**: Out of scope per epic definition. Moved to Fraud VD3.

---

## Past SIs Referenced

| SI | Title | Relevance |
|---|---|---|
| **1372673** | MIGR Wireless – Migration Device Financing, Signature (QB7356) | ⭐ Primary — same financial stack; ILS lifecycle changes in BSSe; closest LoE analog to exception handling |
| **1383580** | Device Financing Back Office (QB6708) | ⭐⭐ High — back-office loan correction flows; overlapping apps (BSSe-RTB, ILS, BSSe-MMap, CorpFin) |
| **1279127** | BSSe Wireless Device Financing – Installment Loan Setup, Billing, Direct Fulfillment | ⭐ High — foundational ILS/billing setup; ILS interfaces defined here |
| **1279103** | BSSe Wireless Device Financing – Installment Loan Reporting & Recon Plus (QB6545) | ✅ Medium — C18 reporting scope; BSSe-MMap/RECON PLUS reconciliation interfaces |
| **1372668** | BST Wireless – Device Financing Promotions (QB7355) | ✅ Medium — ILS promo lifecycle (negative loan); overlapping BSSe-C1, ILS, OCE, BSSe-MMap |
| **1036446** | QB5791 Shop & Purchase – Sell Accessories and Devices | ✅ Supporting — ATTCC/Care channel, acctableau, BSSe-OC buy flow calibration |
