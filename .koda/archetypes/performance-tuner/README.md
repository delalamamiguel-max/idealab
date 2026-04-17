# Performance Tuner Archetype

## Overview
This archetype defines the foundational principles and hard-stop rules for performance tuning. It ensures that optimizations are data-driven, tested, and safe.

## Core Principles
*   **Authorized Scaling:** Do not scale clusters beyond approved node counts.
*   **Smart Collection:** No broad `collect()` calls without sampling.
*   **Performance Tests:** Mandatory before/after metrics comparison.
*   **Dynamic Partitioning:** Avoid hard-coded shuffle partitions.
*   **Idempotency:** Maintain idempotent write semantics.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-performance-tuner**: Compare performance metrics (pre vs post).
*   **debug-performance-tuner**: Analyze performance bottlenecks.
*   **document-performance-tuner**: Record tuning results and configuration changes.
*   **refactor-performance-tuner**: Apply optimizations to code or config.
*   **scaffold-performance-tuner**: Create a performance test plan.
*   **test-performance-tuner**: Run benchmarks and validate stability.

## Usage
Use `scaffold-performance-tuner` to setup a benchmarking environment. Use `compare-performance-tuner` to validate that your changes actually improved performance without regression.
