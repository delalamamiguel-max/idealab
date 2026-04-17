#!/usr/bin/env python3
"""Generate Solution Intent document for Epic 1371759 from impact analysis data."""
import os, datetime

OUT = os.path.join(os.path.dirname(__file__), "1371759_Solution_Intent.md")

S = 'border: 1px solid black; padding: 8px;'
def tbl(headers, rows):
    h = ['<table border="1" style="border-collapse: collapse; width: 100%;">', '  <thead>', '    <tr>']
    for c in headers: h.append(f'      <th style="{S}">{c}</th>')
    h += ['    </tr>', '  </thead>']
    if rows:
        h.append('  <tbody>')
        for r in rows:
            h.append('    <tr>')
            for i,c in enumerate(r): h.append(f'      <td style="{S}">{c}</td>')
            for _ in range(len(headers)-len(r)): h.append(f'      <td style="{S}"></td>')
            h.append('    </tr>')
        h.append('  </tbody>')
    h.append('</table>')
    return '\n'.join(h)

# ── APPLICATION DATA ──
dev_seeds = [
    ("1371759 Development","Enhance","23488","OCE","","TBD/SME","BC-01, BC-02, BC-03, BC-05"),
    ("1371759 Development","Enhance","21053","YODA","","TBD/SME","BC-01, BC-02, BC-03, BC-05"),
    ("1371759 Development","Enhance","31902","SCOR","","TBD/SME","BC-03, BC-05"),
    ("1371759 Development","Enhance","30687","BWSFMC","","TBD/SME","BC-01, BC-06"),
    ("1371759 Development","Enhance","13287","CFM","","TBD/SME","BC-07"),
    ("1371759 Development","Enhance","30914","BSSe-RTB","","TBD/SME","BC-07"),
    ("1371759 Development","Enhance","31697","BSSe-MMap","","TBD/SME","BC-06, BC-07"),
    ("1371759 Development","Enhance","31543","IDP-Order Graph Cloud","","TBD/SME","BC-01, BC-02, BC-03, BC-05"),
    ("1371759 Development","Configure","18249","ORACLE SCM","","TBD/SME","BC-03"),
    ("1371759 Development","Enhance","18944","OrderTrack","","TBD/SME","BC-05, BC-06"),
    ("1371759 Development","Enhance","17815","ASPEN","","TBD/SME","BC-07"),
    ("1371759 Development","Enhance","31372","ILS","","TBD/SME","BC-07"),
]
dev_bsse = [
    ("1371759 Development","Enhance","30909","BSSe-OC","","Easy","BC-01, BC-02, BC-03, BC-05"),
    ("1371759 Development","Enhance","30911","BSSe-C1","","Easy","BC-01, BC-02"),
    ("1371759 Development","Configure","30912","BSSe-iPaaS","","Easy","BC-01, BC-02, BC-03"),
    ("1371759 Development","Enhance","31452","BSSe-SkyFM","","Easy","BC-05, BC-06"),
    ("1371759 Development","Enhance","32985","BSSe-ACF","","Easy","BC-01, BC-02, BC-07"),
    ("1371759 Development","Enhance","31692","BSSe-BB","","Easy","BC-01, BC-02, BC-07"),
    ("1371759 Development","Enhance","31710","BSSe-NEO","","Easy","BC-01, BC-07"),
]
dev_ccmule = [
    ("1371759 Development","Enhance","33686","CCMule-CLM","","Easy-Moderate","BC-03, BC-06"),
    ("1371759 Development","Enhance","33688","CCMule-Service","","Easy-Moderate","BC-01, BC-02, BC-03"),
    ("1371759 Development","Enhance","30686","CCMULE","","Easy-Moderate","BC-01, BC-02, BC-03"),
]
dev_dpg = [
    ("1371759 Development","Enhance","31204","DPG - Billing","","Easy","BC-07"),
    ("1371759 Development","Enhance","31478","DPG - Customer & Accounts","","Easy","BC-01, BC-02"),
    ("1371759 Development","Enhance","31618","DPG - Finance","","Easy","BC-07"),
    ("1371759 Development","Enhance","31510","DPG - Orders & Supply Chain","","Easy","BC-03, BC-05"),
    ("1371759 Development","Enhance","31479","DPG - Sales & Sunrise","","Easy","BC-01"),
    ("1371759 Development","Enhance","29670","DPG - EDM Omnichannel Analytics","","Easy","BC-01"),
    ("1371759 Development","Enhance","32417","DPG - Network & Usage","","Easy","BC-01"),
    ("1371759 Development","Enhance","31520","DPG - Credit and Collections","","Easy","BC-07"),
]
dev_idp = [
    ("1371759 Development","Configure","33932","IDP-CTX-Evt-HUB","","Easy","BC-01, BC-02, BC-03"),
    ("1371759 Development","Configure","33825","IDP-Commerce-Cart & Pricing","","Easy","BC-01, BC-02"),
    ("1371759 Development","Configure","33824","IDP-Commerce-P&O Discovery","","Easy","BC-01, BC-02"),
    ("1371759 Development","Configure","31468","IDP-Customer Graph Cloud","","Easy","BC-01, BC-02"),
    ("1371759 Development","Enhance","32166","IDP-OMNI-ODS","","Easy","BC-01, BC-02, BC-05"),
    ("1371759 Development","Enhance","32768","IDP-WebAcctMgmt","","Easy","BC-01, BC-02, BC-05"),
    ("1371759 Development","Configure","32470","IDP-Platform Cloud","","Easy","BC-01"),
]
dev_order = [
    ("1371759 Development","Enhance","22966","Trade-In","","Easy","BC-01, BC-02, BC-03"),
    ("1371759 Development","Configure","31292","ISBUS","","Easy","BC-01, BC-06"),
    ("1371759 Development","Configure","25316","MSGRTR","","Easy","BC-06"),
    ("1371759 Development","Enhance","25376","WMS - FDC/PDC - FedEx","","Easy","BC-03, BC-05"),
    ("1371759 Development","Configure","17989","Oracle OM","","Easy","BC-01, BC-02, BC-03"),
    ("1371759 Development","Configure","32785","STIBO","","Easy","BC-03"),
    ("1371759 Development","Configure","23135","OALC","","Easy","BC-01, BC-02"),
    ("1371759 Development","Enhance","30920","notifyNow","","Easy","BC-06"),
    ("1371759 Development","Configure","31293","IEBUS","","Easy","BC-01"),
]
dev_channel = [
    ("1371759 Development","Enhance","30558","myATT Mobile App","","Easy","BC-01, BC-02, BC-05, BC-06"),
    ("1371759 Development","Enhance","18257","OPUS - C","","Easy","BC-01, BC-02"),
    ("1371759 Development","Enhance","31599","ATTCC","","Easy","BC-01, BC-02, BC-05"),
    ("1371759 Development","Enhance","27835","OMHUB","","Easy","BC-01, BC-02, BC-05"),
]
dev_finance = [
    ("1371759 Development","Configure","73","CAPM","","Easy","BC-07"),
    ("1371759 Development","Configure","32412","CorpFin-GL","","Easy","BC-07"),
    ("1371759 Development","Configure","32476","CorpFin-Integration","","Easy","BC-07"),
    ("1371759 Development","Enhance","34345","CFMS4","","Easy","BC-07"),
    ("1371759 Development","Configure","8043","CFAS-CS","","Easy","BC-07"),
    ("1371759 Development","Configure","9783","ERP","","Easy","BC-07"),
    ("1371759 Development","Configure","17985","Oracle AR","","Easy","BC-07"),
    ("1371759 Development","Enhance","33847","BUPS Platform","","Easy","BC-07"),
]
dev_support = [
    ("1371759 Development","Configure","32255","CCDL","","Easy","BC-01"),
    ("1371759 Development","Configure","25114","AVTK","","Easy","BC-01"),
    ("1371759 Development","Configure","30732","ABS-Suite","","Easy","BC-07"),
    ("1371759 Development","Configure","18211","EDP","","Easy","BC-01"),
    ("1371759 Development","Configure","18906","EDS","","Easy","BC-03"),
    ("1371759 Development","Configure","32765","IDP-IDM","","Easy","BC-01"),
    ("1371759 Development","Configure","31998","IDP-DTAP","","Easy","BC-01, BC-03"),
    ("1371759 Development","Configure","31595","IDP - Consent","","Easy","BC-01"),
    ("1371759 Development","Configure","33944","IDGraph","","Easy","BC-01"),
    ("1371759 Development","Configure","32767","APM0039726","","Easy","BC-01"),
    ("1371759 Development","Enhance","33687","APM0044947","","Easy-Moderate","BC-01, BC-03"),
    ("1371759 Development","Configure","33826","APM0045081","","Easy","BC-01"),
    ("1371759 Development","Configure","33827","APM0045082","","Easy","BC-01"),
]

all_dev = dev_seeds + dev_bsse + dev_ccmule + dev_dpg + dev_idp + dev_order + dev_channel + dev_finance + dev_support

test_apps = [
    ("1371759 Testing","TestSupport","30910","BSSe-OH","","TestSupport (TSO)","BC-01, BC-02, BC-03"),
    ("1371759 Testing","TestSupport","34173","IDP-PLTFRM","","TestSupport (TSO)","BC-01, BC-02"),
    ("1371759 Testing","Test","22597","DATARTR","","Test","BC-01"),
    ("1371759 Testing","Test","32765","IDP-IDM","","Test","BC-01, BC-02"),
    ("1371759 Testing","Test","31998","IDP-DTAP","","Test","BC-01, BC-03"),
    ("1371759 Testing","TestSupport","31293","IEBUS","","TestSupport (TSO)","BC-01"),
    ("1371759 Testing","Test","20138","OTSM","","Test","BC-03, BC-05"),
    ("1371759 Testing","Test","27429","OTS","","Test","BC-03, BC-05"),
]

# ── INTERFACE DATA ──
interfaces = [
    ("myATT Mobile App","OCE","Trade-In Self-Service Initiation","REST API","Customer submits trade-in request via myATT; OCE receives order payload (BC-01, BC-02)","New"),
    ("OPUS - C","OCE","Agent-Assisted Trade-In Submit","REST API","Retail/care agent submits trade-in order on behalf of customer (BC-01, BC-02)","New"),
    ("OCE","Trade-In","Trade-In Eligibility & Valuation Request","REST API","OCE calls Trade-In for device eligibility check and Assurant/Hyla valuation quote (BC-01, BC-02, BC-03)","New"),
    ("Trade-In","OCE","Trade-In Valuation Response","REST API","Returns device condition tier, credit value, and promo eligibility (BC-01, BC-02)","Enhance"),
    ("OCE","YODA","Trade-In Order Handoff","REST API","OCE passes confirmed trade-in order to YODA for billing/account processing (BC-01, BC-02)","New"),
    ("YODA","BSSe-RTB","Bill Credit Application Event","Event","YODA publishes trade-in credit event for real-time billing credit (BC-07)","Enhance"),
    ("YODA","CFM","Financial Settlement Request","REST API","YODA submits trade-in financial settlement to CFM for credit accounting (BC-07)","Enhance"),
    ("YODA","ILS","Installment Ledger Credit Update","REST API","YODA updates ILS with trade-in credit applied to installment loan (BC-07)","Enhance"),
    ("YODA","ASPEN","Bill Credit Accounting Entry","REST API","YODA triggers ASPEN to record trade-in credit as accounting entry (BC-07)","Enhance"),
    ("OCE","SCOR","Trade-In RMA Order Request","REST API","OCE sends RMA request to SCOR for device return logistics (BC-03)","New"),
    ("SCOR","ORACLE SCM","RMA Work Order Create","API","SCOR creates RMA work order in Oracle SCM for device return label (BC-03)","New"),
    ("ORACLE SCM","WMS - FDC/PDC - FedEx","RMA Shipping Label Request","API","Oracle SCM requests FedEx return label via WMS integration (BC-03)","Enhance"),
    ("WMS - FDC/PDC - FedEx","OrderTrack","Shipment Tracking Event","Event","FedEx/WMS publishes shipment events; OrderTrack consumes for status (BC-05)","Enhance"),
    ("OCE","OrderTrack","Trade-In Order Status Event","Event","OCE publishes order lifecycle events for customer visibility (BC-05)","Enhance"),
    ("OCE","BSSe-OC","Trade-In Order Context","REST API","OCE passes trade-in context to BSSe-OC for order capture (BC-01)","Enhance"),
    ("BSSe-OC","BSSe-iPaaS","Trade-In Order Event","Event","BSSe-OC publishes trade-in events via iPaaS to downstream (BC-01)","Configure"),
    ("BSSe-iPaaS","IDP-CTX-Evt-HUB","Trade-In Context Event Route","Event","BSSe-iPaaS routes context events to IDP-CTX-Evt-HUB (BC-01)","Configure"),
    ("OCE","IDP-Order Graph Cloud","Trade-In Order Graph Node","Event","OCE publishes trade-in order for graph node creation (BC-01, BC-05)","Enhance"),
    ("OCE","ISBUS","Trade-In Order Event Publish","Event","OCE publishes trade-in event to ISBUS for downstream routing (BC-01, BC-06)","Enhance"),
    ("ISBUS","CCMule-CLM","Trade-In CLM Notification Trigger","Event","ISBUS routes trade-in comm events to CCMule-CLM (BC-06)","Enhance"),
    ("ISBUS","CCMule-Service","Trade-In Service Event","Event","ISBUS routes trade-in events to CCMule-Service (BC-01, BC-03)","Enhance"),
    ("CCMule-CLM","BWSFMC","RMA Communication Request","REST API","CCMule-CLM sends RMA communication request to BWSFMC (BC-06)","Enhance"),
    ("BWSFMC","MSGRTR","Customer Notification Route","Event","BWSFMC routes notification payloads to MSGRTR for SMS/email (BC-06)","Configure"),
    ("BWSFMC","notifyNow","Push Notification Dispatch","Event","BWSFMC triggers push notification via notifyNow for myATT (BC-06)","Enhance"),
    ("OCE","IDP-OMNI-ODS","Trade-In Order Data Persist","Event","OCE writes trade-in order data to ODS for persistence (BC-01, BC-05)","Enhance"),
    ("IDP-WebAcctMgmt","IDP-OMNI-ODS","Trade-In Status Read","REST API","IDP-WebAcctMgmt reads trade-in order status from ODS (BC-05)","Enhance"),
    ("myATT Mobile App","IDP-WebAcctMgmt","Trade-In Tracking Display","REST API","myATT retrieves trade-in tracking for self-serve UI (BC-05, BC-06)","Enhance"),
    ("ATTCC","OCE","Care Agent Trade-In View","REST API","ATTCC reads trade-in order context from OCE for care agent (BC-01, BC-05)","Enhance"),
    ("BSSe-RTB","DPG - Billing","Trade-In Credit Transaction","Event","BSSe-RTB publishes credit transaction to DPG-Billing (BC-07)","Enhance"),
    ("BSSe-SkyFM","OrderTrack","Fulfillment Exception Event","Event","BSSe-SkyFM raises exception events for OrderTrack status (BC-05)","Enhance"),
    ("CFM","CorpFin-GL","Trade-In GL Journal Entry","Batch","CFM generates GL journal entry for trade-in credits (BC-07)","Configure"),
    ("OCE","Trade-In","Trade-In Initiation via BSSe","REST API","New entry point for BSSe-originated trade-in vs legacy path (BC-01)","New"),
]

# ── BUILD DOCUMENT ──
lines = []
W = lines.append

W("<!-- SI Document – 1371759 BSSe Wireless: Trade-In & Buyback Solution Intent -->")
W("")
W(tbl(["","Solution Intent (SI)"],[]))
W("")
W("SI Generated: 03/13/26")
W("")
W("***ATTENTION: This Solution Intent (SI) should be validated by the Solution Architect to ensure requirements are still satisfied, if PI planning or phase 2 implementation begins after 09/13/26***")
W("")
W("*It is Strongly encouraged to be reviewed with the Solution Architect if initial SI is being targeted in a later PI/release than initially planned.*")
W("")
W("")
W("# 1371759 BSSe Wireless: Trade-In & Buyback (QB-7342) Solution Intent")
W("")
W("")
W("Revision History")
W("")
W(tbl(["Author / ATTUID","Revision Date","Version","Revision Description"],
      [["","13 Mar 2026","0.01","Initial version SI — generated from impact analysis report v4"]]))
W("")
W("")
W("# Problem Statement")
W("")
W("This epic introduces net-new unified Trade-In & Buyback capability on the BSSe Wireless platform. The current landscape lacks a cohesive BSSe-native trade-in order flow — device trade-in processing, RMA logistics, device condition assessment, bill credit application, and customer status tracking are fragmented across legacy systems.")
W("")
W("Epic 1371759 delivers a unified solution spanning order capture (OCE/YODA), supply chain logistics (SCOR/Oracle SCM/FedEx), financial settlement (CFM/ASPEN/ILS/BSSe-RTB), and customer communication (BWSFMC/CCMule/OrderTrack) to enable BSSe wireless customers to trade in devices for bill credits through self-service (myATT), retail (OPUS-C), and care (ATTCC) channels.")
W("")
W("**Epic Scope:** BC-01 (Trade-In for Bill Credit) · BC-02 (Buyback Standalone) · BC-03 (RMA) · BC-04 (Device Assessment) · BC-05 (Order Tracking) · BC-06 (Communications) · BC-07 (Financial Settlement)")
W("")
W("**PI28 Active:** BC-01, BC-03, BC-04, BC-05, BC-06")
W("")
W("**ON HOLD PI28:** BC-02 (Buyback Standalone), BC-07 (Financial Settlement)")
W("")
W("")
W("# Contributing Factors")
W("")
W("")
W("## Assumptions, Constraints and Dependencies")
W("")

acd_rows = [
    ["Assumptions",""],
    ["A1","All 12 seed applications require SME-confirmed LoE assignments during PI28 planning."],
    ["A2","Assurant/Hyla is an external partner system with no internal MOTS ID — the Trade-In system (22966) serves as the internal integration point."],
    ["A3","BSSe-Core family apps (BSSe-OC, -C1, -iPaaS, -SkyFM, -ACF, -BB, -NEO) are assessed at Easy LoE per SI 1372673 historical anchoring."],
    ["A4","DPG, IDP-Platform, CCMule, and BSSe-Core critical families are mandatory assessment — Rule A/C/D exclusions never applied."],
    ["A5","BFS depth=2 from 12 seeds produced 193 candidates; 126 excluded via Rules A/C/D."],
    ["A6","notifyNow (30920) is included as Enhance/Easy for BC-06 push notifications — not excluded (unlike exception handling epic where it was hop=2 No Change)."],
    ["Constraints",""],
    ["C1","BC-02 (Buyback Standalone) and BC-07 (Financial Settlement) are ON HOLD for PI28 — apps tagged with these capabilities may have deferred development."],
    ["C2","24 catalog gaps (APM0*/UNKNOWN) identified in iTAP — 4 included with unresolved names, 20 excluded via Rule A."],
    ["C3","BYOD trade-in without new BSSe line purchase is out of scope."],
    ["C4","Bulk/Business customer trade-in is future state (separate epic)."],
    ["C5","Legacy TLG trade-in sunset is a separate epic."],
    ["Dependencies",""],
    ["D1","SI 1383580 — Device Financing Back Office (QB6708) — OCE/YODA reference patterns"],
    ["D2","SI 1372673 — MIGR Wireless Device Financing, Signature (QB7356) — BSSe-Core LoE anchoring"],
    ["D3","SI 1279127 — BSSe Wireless Device Financing — foundational ILS/billing interfaces"],
    ["D4","SI 1372668 — BST Wireless Device Financing Promotions (QB7355) — Trade-In promo lifecycle"],
]
W(tbl(["A/C/D #","Description"], acd_rows))
W("")
W("")
W("## Applications Summary Table")
W("")

app_headers = ["Parent Package","Impact Type","MOTS ID","Application","IT App Owner","LoE"]
app_rows = []
for a in all_dev:
    app_rows.append([a[0],a[1],a[2],a[3],a[4],a[5]])
for a in test_apps:
    app_rows.append([a[0],a[1],a[2],a[3],a[4],a[5]])
W(tbl(app_headers, app_rows))
W("")
W("*Group impacts are added automatically via MDE and are not represented in the SI.")
W("")
W("")

# ── SEQUENCING ──
W("## Sequencing Summary Table")
W("")
seq_rows = [
    ["1","myATT Mobile App / OPUS-C / ATTCC","Customer/Agent Trade-In Initiation","Customer or agent submits trade-in request via channel UI"],
    ["2","OCE","Order Capture & Eligibility","OCE captures trade-in order, calls Trade-In system for eligibility/valuation"],
    ["3","Trade-In","Device Valuation","Trade-In system returns device condition tier, credit value, promo eligibility"],
    ["4","OCE","Order Confirmation & Handoff","OCE confirms trade-in order, hands off to YODA and publishes events to ISBUS/ODS/Order Graph"],
    ["5","YODA","Billing & Financial Processing","YODA processes bill credit application via BSSe-RTB, CFM, ASPEN, ILS"],
    ["6","SCOR / ORACLE SCM","RMA & Supply Chain","SCOR creates RMA work order; Oracle SCM generates FedEx return label"],
    ["7","WMS - FDC/PDC - FedEx","Device Return Shipping","FedEx generates return label and publishes shipment tracking events"],
    ["8","OrderTrack","Status Tracking","OrderTrack records trade-in lifecycle events for customer visibility"],
    ["9","BSSe-OC / BSSe-iPaaS","Order Context Distribution","BSSe-OC captures order context; iPaaS distributes to IDP-CTX-Evt-HUB"],
    ["10","ISBUS / CCMule-CLM / BWSFMC","Customer Communication","ISBUS routes comm events; CCMule/BWSFMC send SMS/email/push notifications"],
    ["11","DPG Family","Data Product Updates","DPG family members consume trade-in events for billing, order, finance, and analytics data products"],
    ["ZZZ","BSSe-Core / IDP-Platform / Supporting","Platform Support","Platform and infrastructure apps — sequence per PI planning"],
]
W(tbl(["Seq #","Application","Activity/Action","Description"], seq_rows))
W("")
W("*Sequences of \"ZZZ\" means the application was not considered in the sequencing.")
W("This sequence table understands that this sequence does not cover all acceptance criteria or requirements or all scenarios under epic but covers most common and generic flow to give high level idea.")
W("Actual development sequence should be relied on PI planning exercises.")
W("")
W("")

# ── PRODUCT TEAM ──
W("## Product Team Summary Table")
W("")
pt_rows = []
for a in all_dev + test_apps:
    pt_rows.append(["", f"{a[3]} (MOTS ID: {a[2]})", a[2], a[3], a[5]])
W(tbl(["Product Team","Notes","MOTS ID","Application","Application LoE"], pt_rows))
W("")
W("")

# ── INTERFACES ──
W("## Interfaces Summary Table")
W("")
int_headers = ["Source","Target","Name","Type","Description","Impact Type"]
int_rows = [[i[0],i[1],i[2],i[3],i[4],i[5]] for i in interfaces]
W(tbl(int_headers, int_rows))
W("")
W("*Any Non-Backward compatible api design changes should be flagged for a risk assessment/validation by the api Provider with all api Consumers and SA/AA/SyE")
W("")
W("")

# ── REQUIREMENTS ──
W("## Requirements Summary Table")
W("")
W(tbl(["NFR","Name","Notes","Apps"],[]))
W("")
W("")

# ── END TO END SOLUTION ──
W("## 1371759 End to End Solution")
W("")
W("")
W("### BC-01 — Trade-In for Bill Credit")
W("")
W("The customer initiates a device trade-in through myATT Mobile App (self-service), OPUS-C (retail agent), or ATTCC (care agent). The channel application submits the trade-in request to OCE, which captures the order and calls the Trade-In system (22966) for device eligibility verification and Assurant/Hyla valuation. The Trade-In system returns the device condition tier, estimated credit value, and promotional eligibility.")
W("")
W("Upon customer confirmation, OCE hands the trade-in order to YODA for billing and account processing. YODA publishes bill credit events to BSSe-RTB for real-time billing credit application to the customer's BSSe BAN. OCE simultaneously publishes order events to ISBUS, IDP-Order Graph Cloud, IDP-OMNI-ODS, and OrderTrack for downstream processing and status tracking.")
W("")
W("")
W("### BC-03 — RMA Request & Device Return Logistics")
W("")
W("When a trade-in is confirmed, OCE sends an RMA order request to SCOR (Supply Chain Orchestration). SCOR creates an RMA work order in ORACLE SCM, which requests a FedEx return shipping label via WMS-FDC/PDC-FedEx. The label is generated and tracking events are published back through OrderTrack for customer visibility.")
W("")
W("The device is shipped back by the customer using the pre-paid label. FedEx/WMS publishes shipment tracking events (pickup, in-transit, delivered) that OrderTrack consumes to update the trade-in order status visible to the customer.")
W("")
W("")
W("### BC-04 — Device Condition Assessment & Grading")
W("")
W("Upon device receipt at the partner facility, Assurant/Hyla performs condition assessment and grading. The Trade-In system (22966) serves as the internal integration point for receiving assessment results. Final credit value may be adjusted based on actual device condition versus the initial estimate.")
W("")
W("")
W("### BC-05 — Order Tracking & Customer Status Visibility")
W("")
W("OrderTrack (18944) serves as the central status aggregation point. It receives trade-in order events from OCE, shipment tracking from WMS-FedEx, and fulfillment exception events from BSSe-SkyFM. Customers access trade-in status through myATT Mobile App → IDP-WebAcctMgmt → IDP-OMNI-ODS. Care agents view status through ATTCC → OCE.")
W("")
W("")
W("### BC-06 — Customer Communications / Notifications")
W("")
W("Trade-in lifecycle events trigger customer notifications through the ISBUS → CCMule-CLM → BWSFMC pipeline. BWSFMC routes notifications to MSGRTR for SMS/email delivery and to notifyNow for myATT push notifications. Communication types include: trade-in confirmation, RMA label sent, device received, credit applied, and exception notifications.")
W("")
W("")
W("### BC-07 — Financial Settlement, Bill Credit & Reporting (ON HOLD PI28)")
W("")
W("YODA orchestrates financial settlement by sending requests to CFM (credit accounting and GL posting), ASPEN (accounting entries), ILS (installment loan ledger credit), and BSSe-RTB (real-time billing credit). CFM generates GL journal entries to CorpFin-GL for reconciliation. BSSe-RTB publishes credit transactions to DPG-Billing. BUPS Platform handles billing credit settlement. Financial reporting flows through DPG-Finance, DPG-Credit and Collections, and DPG-Billing data products.")
W("")
W("")
W("---")
W("")
W("")
W("##### Reporting and Audit")
W("")
W("DPG family members provide operational reporting: DPG-Billing (credit transactions), DPG-Finance (GL entries), DPG-Orders & Supply Chain (RMA tracking), DPG-Customer & Accounts (customer data), DPG-Sales & Sunrise (trade-in promo data), DPG-EDM Omnichannel Analytics (analytics), DPG-Network & Usage (network data), and DPG-Credit and Collections (credit/collections). Financial audit trails flow through CFM → CorpFin-GL/CorpFin-Integration → ASPEN.")
W("")
W("")
W("##### Future Scope Considerations (not in this EPIC)")
W("")
W("- BYOD trade-in without new BSSe line purchase")
W("- Bulk / Business customer trade-in")
W("- Legacy TLG trade-in sunset (separate epic)")
W("- Assurant payment processing (partner-owned)")
W("")
W("")

# ── CONTEXT DIAGRAM ──
W("### Context - 1371759 BSSe Wireless: Trade-In & Buyback")
W("")
W("```mermaid")
W('%%{init: {"theme": "base", "themeVariables": {"fontSize": "11px"}, "flowchart": {"nodeSpacing": 25, "rankSpacing": 40}}}%%')
W("")
W("flowchart TB")
W("")
W('    subgraph LEGEND["Impact Legend"]')
W("        direction LR")
W('        L_NEW["◼ New"]:::impactNew')
W('        L_ENH["◼ Enhance"]:::impactEnhance')
W('        L_CFG["◼ Configure"]:::impactConfigure')
W('        L_TST["◼ Test"]:::impactTest')
W('        L_NC["◼ No Change"]:::impactNoChange')
W("    end")
W("")
W('    subgraph LINE_LEGEND["Line Legend"]')
W("        direction LR")
W('        LL1["── Enhance/New"]')
W('        LL2["-·- Test"]')
W('        LL3["··· Configure"]')
W("    end")
W("")
W('    subgraph ACTORS["Actors"]')
W("        direction LR")
W('        CUSTOMER(["🧑 Customer"])')
W('        AGENT(["🧑 Agent"])')
W("    end")
W("")
W('    subgraph CHANNEL["Channel Layer"]')
W("        direction LR")
W('        MYATT["myATT Mobile App<br/><small>30558 · Enhance · Easy</small>"]:::impactEnhance')
W('        OPUSC["OPUS-C<br/><small>18257 · Enhance · Easy</small>"]:::impactEnhance')
W('        ATTCC_N["ATTCC<br/><small>31599 · Enhance · Easy</small>"]:::impactEnhance')
W('        OMHUB_N["OMHUB<br/><small>27835 · Enhance · Easy</small>"]:::impactEnhance')
W("    end")
W("")
W('    subgraph ORDER["Order Orchestration"]')
W("        direction LR")
W('        OCE_N["OCE<br/><small>23488 · Enhance · TBD/SME</small>"]:::impactEnhance')
W('        YODA_N["YODA<br/><small>21053 · Enhance · TBD/SME</small>"]:::impactEnhance')
W('        TRADEIN["Trade-In<br/><small>22966 · Enhance · Easy</small>"]:::impactEnhance')
W("    end")
W("")
W('    subgraph BSSE["BSSe Core"]')
W("        direction LR")
W('        BSSEOC["BSSe-OC<br/><small>30909 · Enhance · Easy</small>"]:::impactEnhance')
W('        BSSEIP["BSSe-iPaaS<br/><small>30912 · Configure · Easy</small>"]:::impactConfigure')
W('        BSSESKY["BSSe-SkyFM<br/><small>31452 · Enhance · Easy</small>"]:::impactEnhance')
W('        BSSEACF["BSSe-ACF<br/><small>32985 · Enhance · Easy</small>"]:::impactEnhance')
W('        BSSERTB["BSSe-RTB<br/><small>30914 · Enhance · TBD/SME</small>"]:::impactEnhance')
W('        BSSEC1["BSSe-C1<br/><small>30911 · Enhance · Easy</small>"]:::impactEnhance')
W('        BSSEBB["BSSe-BB<br/><small>31692 · Enhance · Easy</small>"]:::impactEnhance')
W('        BSSENEO["BSSe-NEO<br/><small>31710 · Enhance · Easy</small>"]:::impactEnhance')
W("    end")
W("")
W('    subgraph SUPPLY["Supply Chain"]')
W("        direction LR")
W('        SCOR_N["SCOR<br/><small>31902 · Enhance · TBD/SME</small>"]:::impactEnhance')
W('        OSCM["ORACLE SCM<br/><small>18249 · Configure · TBD/SME</small>"]:::impactConfigure')
W('        WMS["WMS-FedEx<br/><small>25376 · Enhance · Easy</small>"]:::impactEnhance')
W('        ORDTRK["OrderTrack<br/><small>18944 · Enhance · TBD/SME</small>"]:::impactEnhance')
W("    end")
W("")
W('    subgraph COMMS["Communications"]')
W("        direction LR")
W('        ISBUS_N["ISBUS<br/><small>31292 · Configure · Easy</small>"]:::impactConfigure')
W('        CCCLM["CCMule-CLM<br/><small>33686 · Enhance · Easy-Mod</small>"]:::impactEnhance')
W('        CCSVC["CCMule-Service<br/><small>33688 · Enhance · Easy-Mod</small>"]:::impactEnhance')
W('        BWSFMC_N["BWSFMC<br/><small>30687 · Enhance · TBD/SME</small>"]:::impactEnhance')
W('        MSGRTR_N["MSGRTR<br/><small>25316 · Configure · Easy</small>"]:::impactConfigure')
W('        NOTIFY["notifyNow<br/><small>30920 · Enhance · Easy</small>"]:::impactEnhance')
W("    end")
W("")
W('    subgraph FINANCE["Financial Layer"]')
W("        direction LR")
W('        CFM_N["CFM<br/><small>13287 · Enhance · TBD/SME</small>"]:::impactEnhance')
W('        ASPEN_N["ASPEN<br/><small>17815 · Enhance · TBD/SME</small>"]:::impactEnhance')
W('        ILS_N["ILS<br/><small>31372 · Enhance · TBD/SME</small>"]:::impactEnhance')
W('        BSSEMMAP["BSSe-MMap<br/><small>31697 · Enhance · TBD/SME</small>"]:::impactEnhance')
W('        CORPGL["CorpFin-GL<br/><small>32412 · Configure · Easy</small>"]:::impactConfigure')
W('        BUPS["BUPS<br/><small>33847 · Enhance · Easy</small>"]:::impactEnhance')
W("    end")
W("")
W('    subgraph IDP["IDP Platform"]')
W("        direction LR")
W('        IDPOG["IDP-Order Graph<br/><small>31543 · Enhance · TBD/SME</small>"]:::impactEnhance')
W('        IDPODS["IDP-OMNI-ODS<br/><small>32166 · Enhance · Easy</small>"]:::impactEnhance')
W('        IDPWAM["IDP-WebAcctMgmt<br/><small>32768 · Enhance · Easy</small>"]:::impactEnhance')
W('        IDPCTX["IDP-CTX-Evt-HUB<br/><small>33932 · Configure · Easy</small>"]:::impactConfigure')
W('        IDPCG["IDP-Cust Graph<br/><small>31468 · Configure · Easy</small>"]:::impactConfigure')
W("    end")
W("")
W('    subgraph DPG["Data Products"]')
W("        direction LR")
W('        DPGBILL["DPG-Billing<br/><small>31204 · Enhance · Easy</small>"]:::impactEnhance')
W('        DPGFIN["DPG-Finance<br/><small>31618 · Enhance · Easy</small>"]:::impactEnhance')
W('        DPGOSC["DPG-Orders&SC<br/><small>31510 · Enhance · Easy</small>"]:::impactEnhance')
W("    end")
W("")
W("    %% ── CONNECTIONS ──")
W('    CUSTOMER --> MYATT')
W('    AGENT --> OPUSC')
W('    AGENT --> ATTCC_N')
W('    MYATT -->|"Trade-In Initiation<br/>(REST API)"| OCE_N')
W('    OPUSC -->|"Agent Trade-In<br/>(REST API)"| OCE_N')
W('    ATTCC_N -->|"Care View<br/>(REST API)"| OCE_N')
W('    OCE_N -->|"Eligibility<br/>(REST API)"| TRADEIN')
W('    OCE_N -->|"Order Handoff<br/>(REST API)"| YODA_N')
W('    OCE_N -->|"RMA Request<br/>(REST API)"| SCOR_N')
W('    OCE_N -->|"Order Context<br/>(REST API)"| BSSEOC')
W('    OCE_N -->|"Order Graph<br/>(Event)"| IDPOG')
W('    OCE_N -->|"Event Publish<br/>(Event)"| ISBUS_N')
W('    OCE_N -->|"ODS Persist<br/>(Event)"| IDPODS')
W('    OCE_N -->|"Status Event<br/>(Event)"| ORDTRK')
W('    YODA_N -->|"Bill Credit<br/>(Event)"| BSSERTB')
W('    YODA_N -->|"Settlement<br/>(REST API)"| CFM_N')
W('    YODA_N -->|"Ledger Update<br/>(REST API)"| ILS_N')
W('    YODA_N -->|"Accounting<br/>(REST API)"| ASPEN_N')
W('    SCOR_N -->|"RMA Work Order<br/>(API)"| OSCM')
W('    OSCM -->|"Ship Label<br/>(API)"| WMS')
W('    WMS -->|"Tracking<br/>(Event)"| ORDTRK')
W('    BSSEOC -.-|"Order Event<br/>(Event)"| BSSEIP')
W('    BSSEIP -.-|"Context Route<br/>(Event)"| IDPCTX')
W('    ISBUS_N -->|"CLM Trigger<br/>(Event)"| CCCLM')
W('    ISBUS_N -->|"Service Event<br/>(Event)"| CCSVC')
W('    CCCLM -->|"RMA Comm<br/>(REST API)"| BWSFMC_N')
W('    BWSFMC_N -.-|"Notification<br/>(Event)"| MSGRTR_N')
W('    BWSFMC_N -->|"Push<br/>(Event)"| NOTIFY')
W('    BSSERTB -->|"Credit Txn<br/>(Event)"| DPGBILL')
W('    BSSESKY -->|"Exception<br/>(Event)"| ORDTRK')
W('    CFM_N -.-|"GL Entry<br/>(Batch)"| CORPGL')
W('    IDPWAM -->|"Status Read<br/>(REST API)"| IDPODS')
W('    MYATT -->|"Tracking<br/>(REST API)"| IDPWAM')
W("")
W("    classDef impactNew fill:#00b300,stroke:#006600,color:#fff,font-weight:bold")
W("    classDef impactEnhance fill:#00bcd4,stroke:#00838f,color:#fff,font-weight:bold")
W("    classDef impactConfigure fill:#ff9800,stroke:#e65100,color:#fff,font-weight:bold")
W("    classDef impactTest fill:#ffc107,stroke:#ff8f00,color:#000,font-weight:bold")
W("    classDef impactNoChange fill:#9e9e9e,stroke:#616161,color:#fff,font-weight:bold")
W("```")
W("")
W("SI Created by: Requirements Impact Analyst (AI-assisted) on 13 Mar 2026")
W("Modified: 13 Mar 2026")
W("Figure: 1")
W("")
W("")

# ── PER-APP DETAILS: DEVELOPMENT ──
W("### 1371759 Development")
W("")

def app_detail(name, mots, impact, loe, caps, ifaces):
    lines = []
    lines.append(f"#### {name} {mots}")
    lines.append("")
    lines.append(f"{name} (MOTS ID: {mots})")
    lines.append("")
    lines.append("Tagged Values")
    lines.append("")
    lines.append(tbl(["Application Name","App Lifestyle","App Lifestyle Status","Impact Type","LoE"],
                      [[name,"Operational","In Use",impact,loe]]))
    lines.append("")
    if ifaces:
        lines.append("Interfaces")
        lines.append("")
        lines.append(tbl(["Source","Target","Name","Type","Description","Impact Type"],ifaces))
        lines.append("")
    lines.append("")
    lines.append("---")
    lines.append("")
    return '\n'.join(lines)

# Build interface lookup
iface_lookup = {}
for i in interfaces:
    src, tgt = i[0], i[1]
    row = [i[0],i[1],i[2],i[3],i[4],i[5]]
    iface_lookup.setdefault(src, []).append(row)
    iface_lookup.setdefault(tgt, []).append(row)

for a in all_dev:
    name = a[3]
    mots = a[2]
    impact = a[1]
    loe = a[5]
    caps = a[6] if len(a)>6 else ""
    ifaces = iface_lookup.get(name, [])
    W(app_detail(name, mots, impact, loe, caps, ifaces))

# ── PER-APP DETAILS: TESTING ──
W("")
W("### 1371759 Non Development")
W("")

for a in test_apps:
    name = a[3]
    mots = a[2]
    impact = a[1]
    loe = a[5]
    caps = a[6] if len(a)>6 else ""
    ifaces = iface_lookup.get(name, [])
    W(app_detail(name, mots, impact, loe, caps, ifaces))

# ── TBD ──
W("")
W("### 1371759 TBD")
W("")
W("The following applications have unresolved catalog names and require iTAP/CMDB resolution:")
W("")
tbd_rows = [
    ["32767","APM0039726","Configure","Easy","Unresolved — needs CMDB/iTAP resolution"],
    ["33687","APM0044947","Enhance","Easy-Moderate","Likely CCMule-adjacent — needs resolution"],
    ["33826","APM0045081","Configure","Easy","Unresolved — needs CMDB/iTAP resolution"],
    ["33827","APM0045082","Configure","Easy","Unresolved — needs CMDB/iTAP resolution"],
]
W(tbl(["MOTS ID","Stored Name","Impact Type","LoE","SME Action Required"], tbd_rows))
W("")
W("")

# ── ISSUES LOG ──
W("## Issues Log")
W("")
W("")
W("# Log (Optional issues and information for tracking purposes)")
W("")
log_rows = [
    ["1","13 Mar 2026","SME LoE Assignment Required","12 seed applications (OCE, YODA, SCOR, BWSFMC, CFM, BSSe-RTB, BSSe-MMap, IDP-Order Graph Cloud, ORACLE SCM, OrderTrack, ASPEN, ILS) require SME-confirmed LoE during PI28 planning.","Pending PI28 planning"],
    ["2","13 Mar 2026","Catalog Gaps","24 applications with unresolved APM0*/UNKNOWN names in iTAP catalog. 4 included in Development package; 20 excluded via Rule A.","Route to CMDB/iTAP team"],
    ["3","13 Mar 2026","BC-02 / BC-07 ON HOLD","Buyback Standalone (BC-02) and Financial Settlement (BC-07) are ON HOLD for PI28. Apps tagged with these capabilities may have deferred development.","Monitor PI28 planning decisions"],
    ["4","13 Mar 2026","SCOR → ORACLE SCM Exception Interface","Interface identified but payload and contract not finalized — SME required.","Pending SME confirmation"],
]
W(tbl(["No.","Date","Log Title (Short Title)","Description (Chronologically list the activities with dates)","Notes"], log_rows))
W("")

# ── WRITE FILE ──
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"SI document generated: {OUT}")
print(f"Total lines: {len(lines)}")
