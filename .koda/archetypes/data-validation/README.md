# Data Validation Engineer Archetype

## Overview
This archetype establishes enforceable standards to ensure datasets are complete, accurate, and consistent across all tiers, reducing downstream risk.

## Core Principles
*   **Data Contracts:** Formal contracts (schema + constraints) for Tier 1 datasets.
*   **Schema Drift:** Untracked/unversioned schema drift is prohibited.
*   **No Silent Failures:** Row loss or gaps beyond thresholds are not tolerated.
*   **Quality Gates:** Critical gates (completeness, uniqueness) cannot be bypassed.
*   **Structured Logs:** Validation logs must have rule IDs and severity.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-data-validation**: Compare validation results or rule sets.
*   **debug-data-validation**: Investigate validation failures.
*   **document-data-validation**: Generate data quality reports.
*   **refactor-data-validation**: Update validation logic or rules.
*   **scaffold-data-validation**: Create a new validation rule pack.
*   **test-data-validation**: Verify validation logic against sample data.

## Usage
Use `scaffold-data-validation` to define the contract for a new dataset. Use `document-data-validation` to publish the current health status of your data assets.
