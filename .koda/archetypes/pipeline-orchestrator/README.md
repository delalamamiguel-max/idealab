# Pipeline Orchestrator Archetype

## Overview
This archetype defines the foundational principles and hard-stop rules for orchestrating data pipelines (e.g., in Airflow or TWS). It ensures reliable, auditable, and resilient job scheduling.

## Core Principles
*   **No Hard-Coded Credentials:** Connection IDs and secrets must use environment variables or Key Vault.
*   **Retries Required:** Jobs must have retry logic with backoff.
*   **Callbacks:** `on_failure_callback` and `on_success_callback` are mandatory.
*   **Structured Logging:** Logs must include structured metadata.
*   **Explicit Dependencies:** Upstream/downstream dependencies must be explicit.
*   **Idempotency:** Operations within job streams must be idempotent.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-pipeline-orchestrator**: Compare DAGs or job definitions.
*   **debug-pipeline-orchestrator**: Analyze DAG parsing errors or runtime failures.
*   **document-pipeline-orchestrator**: Generate DAG documentation and graphs.
*   **refactor-pipeline-orchestrator**: Optimize DAG structure or update operators.
*   **scaffold-pipeline-orchestrator**: Create a new DAG or job schedule.
*   **test-pipeline-orchestrator**: Run integrity tests on DAG files.

## Usage
Use `scaffold-pipeline-orchestrator` to generate a compliant DAG structure. Use `test-pipeline-orchestrator` to verify that your DAGs meet the retry and callback requirements.
