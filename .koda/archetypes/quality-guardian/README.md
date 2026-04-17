# Quality Guardian Archetype

## Overview
This archetype defines the foundational principles and hard-stop rules for ensuring data quality within pipelines. It enforces strict standards for error handling, logging, and threshold management.

## Core Principles
*   **Bad Records Handling:** Must include `.option("badRecordsPath", ...)` on all reads.
*   **Parameterized Thresholds:** No hard-coded thresholds; use parameters/variables.
*   **Pipeline Integrity:** Pipelines must fail on critical expectation breaches.
*   **Structured Logging:** Log comprehensive summary metrics, not just "failed".
*   **Parameterization:** Table names, routes, and sinks must be parameterized.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-quality-guardian**: Compare quality rules or threshold configurations.
*   **debug-quality-guardian**: Analyze pipeline failures due to quality checks.
*   **document-quality-guardian**: Generate documentation for quality rules.
*   **refactor-quality-guardian**: Standardize existing quality checks.
*   **scaffold-quality-guardian**: Create a new quality check suite.
*   **test-quality-guardian**: Verify quality rules against test data.

## Usage
Use `scaffold-quality-guardian` to add quality checks to your pipeline. Use `debug-quality-guardian` to investigate why a pipeline halted due to data quality issues.
