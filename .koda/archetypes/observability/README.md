# Observability Archetype

## Overview
This archetype provides a consistent, secure, low-overhead, end-to-end observability layer using OpenTelemetry for React/FastAPI services. It enables root-cause analysis and SLO tracking.

## Core Principles
*   **Trace Propagation:** W3C traceparent headers must be propagated.
*   **Log Correlation:** Logs must include trace_id and span_id.
*   **Privacy:** No PII or secrets in telemetry data.
*   **Standard Metrics:** Metrics must have name, unit, description, and aggregation intent.
*   **Health Probes:** Instrumentation for /healthz and /readyz is mandatory.
*   **Structured Logging:** Logs must be structured JSON.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-observability**: Compare telemetry data or configurations.
*   **debug-observability**: Troubleshoot missing traces or metric gaps.
*   **document-observability**: Document metrics dictionaries and alert rules.
*   **refactor-observability**: Update instrumentation to latest standards.
*   **scaffold-observability**: Add OpenTelemetry setup to a service.
*   **test-observability**: Verify telemetry emission and propagation.

## Usage
Use `scaffold-observability` to instrument a new service. Use `test-observability` to ensure your traces connect end-to-end across service boundaries.
