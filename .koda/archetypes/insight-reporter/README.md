# Insight Reporter Archetype

## Overview
This archetype delivers transparent, stakeholder-ready performance narratives tying model behavior to business KPIs with trusted visualizations and accessible reporting. It ensures that insights are verifiable, accessible, and governed through Bronze, Silver, and Gold maturity stages.

## Core Principles
*   **Data Verification:** reconcile metrics against authoritative stores and business KPIs.
*   **Transparent Methodology:** Clearly define metrics, cohort filters, and segmentation details.
*   **Privacy First:** Never include raw identifiers or PII in visuals or exports.
*   **Accessibility:** Charts must be WCAG-compliant (color contrast, alt text).
*   **Honest Visualization:** Avoid manipulated axes or misleading visuals.
*   **Balanced Reporting:** Present both successes and deficits relative to SLOs.
*   **Governance:** Enforce RBAC and approvals before distribution.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-insight-reporter**: Compare report versions or metric definitions.
*   **debug-insight-reporter**: Troubleshoot data discrepancies or rendering issues.
*   **document-insight-reporter**: Generate narrative reports and documentation.
*   **refactor-insight-reporter**: Improve report clarity, accessibility, or code structure.
*   **scaffold-insight-reporter**: Create new report templates or dashboards.
*   **test-insight-reporter**: Validate data accuracy and accessibility compliance.

## Usage
Use `scaffold-insight-reporter` to start a new report draft (Bronze). Use `test-insight-reporter` to verify data sources and accessibility before promotion to Silver or Gold.
