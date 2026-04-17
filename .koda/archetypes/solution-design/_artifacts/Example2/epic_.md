# Executive Summary
This Epic defines the processes and system behaviors for handling installment plan exceptions and account status changes for BSSe customers within ACC. Scenarios include termination due to non-payment, customer death, military deployment, subscriber changes, service cancellation and foundational payoff, forced acceleration, reinstatement of installment loans, and device returns due to rate/feature changes. The scope focuses on backend orchestration, billing integration, accounting entries, and customer communications, with select human-assisted actions through Care/Retail.

# Objective
- Ensure accurate, compliant handling of installment plan updates across key exception scenarios.
- Integrate with loan systems (ILS), biller, A/R, and accounting (Aspen/GL) for real-time, auditable updates.
- Provide clear customer-facing notifications and guidance where UI is in scope; avoid ACC UI where explicitly out of scope.

# Benefits
- Reduce customer friction and disputes by systematizing exception handling.
- Improve operational efficiency and compliance through automated notifications, accounting entries, and audit trails.
- Ensure billing accuracy and proper financial reconciliation across systems.

# Channels & Products
Channels: Care (human-assisted), Retail (escalation to Care), ACC backend services.
Products: Device installment plans (smartphone, tablet, watch); accessory/account installment plans noted where excluded.

# Devices
Smartphones, tablets, wearables; accessory plans excluded where specified.
    
# Customer Type
BSSe customers with authenticated accounts.

# Assumptions
Includes TOBR exclusions, installment plan status handling, loan system updates, BSSe account status rules, and accounting/biller considerations as previously documented.

# Out of Scope
• Reverse acceleration when account is resumed (C1AC20).
• Transfer installment plan responsibility to another person (C2AC70).
• Subscriber Fraud and Upgrade Fraud moved to Fraud VD3.
• TOBR not covered under ESPR.
• No ACC UI for Capability 1.

# UX Flows
• Non-payment: Systematic trigger on account cancellation; backend acceleration, bill updates, accounting; customer notification (no ACC UI).
• Customer death & Military deployment: Human-assisted intake; backend loan updates, A/R, GL entries; supply chain notifications; customer-facing guidance.
• Subscriber changes & service cancellation/payoff: Agent initiates updates; loan acceleration or reinstatement; biller/GL integration; customer-facing payment options.
Mural Link: [Insert Mural link here]

# Capability Overview
C01 – Terminate due to Non-payment
C02 – Customer Death with no TOBR
C03 – Military Deployment ***
C04 – Subscriber Fraud (Out of Scope)
C05 – Upgrade Fraud (Out of Scope)
C06 – Subscriber (CTN) Changes
C07 – Subscriber (CTN) Service Cancellation  
C08 – Forced Acceleration
C09 – Reinstate Installment Loans
C10 – Device Returns due to Rate/Feature Changes
C18 – Reporting and Audit