# Graph Pattern Detective Archetype

## Overview
This archetype detects meaningful patterns, anomalies, and dependency chains in knowledge graphs. It covers fraud detection via subgraph matching, dependency impact analysis for vulnerability management, real-time pattern alerting, and risk scoring across graph structures.

## Core Principles
*   **Bounded Traversals:** Every graph traversal must have explicit depth limits to prevent resource exhaustion.
*   **Baseline-Driven:** Anomaly detection requires documented baselines of normal behaviour.
*   **Risk Quantification:** Detected patterns must carry numerical risk scores, not just boolean flags.
*   **Temporal Awareness:** All patterns must be evaluated in their temporal context.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **scaffold-graph-pattern-detective**: Scaffold workflow for Graph Pattern Detective.
*   **debug-graph-pattern-detective**: Debug workflow for Graph Pattern Detective.
*   **refactor-graph-pattern-detective**: Refactor workflow for Graph Pattern Detective.
*   **test-graph-pattern-detective**: Test workflow for Graph Pattern Detective.
*   **compare-graph-pattern-detective**: Compare workflow for Graph Pattern Detective.
*   **document-graph-pattern-detective**: Document workflow for Graph Pattern Detective.

## Usage
Start with `scaffold-graph-pattern-detective` to set up your environment. Use `test-graph-pattern-detective` to validate your implementation.
