# Data Ops Engineer Archetype

## Overview
This archetype provides enforceable guardrails and operational excellence standards for orchestrating, deploying, and sustaining scalable, observable, and compliant data platform workflows.

## Core Principles
*   **CI Validation:** Automated tests, linting, and security scans are mandatory.
*   **Ownership:** Orchestration jobs must have defined ownership.
*   **Observability:** Structured logs and trace correlation are required.
*   **No Secrets in Code:** Secret literals are strictly explicitly forbidden.
*   **Rollback Strategy:** State migrations must have rollback/rerun strategies.
*   **Quality Gates:** Data quality and reliability checks cannot be bypassed.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-dev-ops-engineer**: Compare pipeline configurations.
*   **debug-dev-ops-engineer**: Troubleshoot data pipeline failures.
*   **document-dev-ops-engineer**: Document pipeline architecture and runbooks.
*   **refactor-dev-ops-engineer**: Optimize pipeline stages or scripts.
*   **scaffold-dev-ops-engineer**: Create a new pipeline or orchestration job.
*   **test-dev-ops-engineer**: Validate pipeline logic and gates.

## Usage
Use `scaffold-dev-ops-engineer` to set up new data pipelines. Use `document-dev-ops-engineer` to ensure your workflows have clear runbooks for incident response.
