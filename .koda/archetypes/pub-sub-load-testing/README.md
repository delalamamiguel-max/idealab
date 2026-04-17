# Pub/Sub Load Testing Archetype

## Overview
This archetype governs the design, execution, and analysis of load testing scenarios for Pub/Sub systems to ensure they can handle expected and peak loads reliably.

## Core Principles
*   **No Unmonitored Loss:** Zero tolerance for unmonitored message loss.
*   **Bounded Latency:** Latency must remain within defined bounds under load.
*   **Failure Recovery:** Recovery scenarios must be tested.
*   **Metrics:** Load tests must collect metrics (throughput, latency, lag).
*   **Production Validation:** No production deployment without load test validation.
*   **Explicit Config:** No anonymous consumer groups or default-thread settings.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-pub-sub-load-testing**: Compare results from different load test runs.
*   **debug-pub-sub-load-testing**: Analyze bottlenecks or failures in load tests.
*   **document-pub-sub-load-testing**: Generate load test reports and analysis.
*   **refactor-pub-sub-load-testing**: Optimize load test scripts and configs.
*   **scaffold-pub-sub-load-testing**: Create new load testing scenarios/scripts.
*   **test-pub-sub-load-testing**: Verify the load testing harness itself.

## Usage
Use `scaffold-pub-sub-load-testing` to create a new load test plan. Use `debug-pub-sub-load-testing` to interpret results and find performance bottlenecks.
