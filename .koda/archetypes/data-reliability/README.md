# Data Reliability Engineer Archetype

## Overview
This archetype ensures trustworthy, timely, and resilient data delivery by defining enforceable standards for availability, freshness, quality, and recovery.

## Core Principles
*   **SLOs:** Clearly defined Service Level Objectives are mandatory.
*   **No Silent Loss:** Detect and alert on dropped rows or partitions.
*   **Lineage:** Lineage capture is required for critical datasets.
*   **Schema Contracts:** No breaking schema changes without migration plans.
*   **Incident Logging:** Structured logs for reliability events.
*   **Alerting:** Severity-1 failures must satisfy alerting requirements.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-data-reliability**: Compare reliability metrics (SLOs).
*   **debug-data-reliability**: Troubleshoot data delays or outages.
*   **document-data-reliability**: Create runbooks and reliability reports.
*   **refactor-data-reliability**: Improve pipeline resilience code.
*   **scaffold-data-reliability**: Setup SLO monitoring and alerting.
*   **test-data-reliability**: Run chaos engineering tests on pipelines.

## Usage
Use `scaffold-data-reliability` to define your error budgets and SLOs. Use `test-data-reliability` to verify that your alerting fires correctly during simulated failures.
