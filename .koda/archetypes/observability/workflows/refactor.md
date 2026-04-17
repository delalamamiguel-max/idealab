---
description: Refactor observability implementation for better signal quality, reduced cost, and governance compliance (Observability)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Set ARCHETYPES_BASEDIR [⋯]
 
**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory
 
**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set (workflow will halt if this variable is not present in the environment)
 
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

###  1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json ` and parse for OTEL_COLLECTOR_ENDPOINT, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/observability/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: code location, refactoring goals (cost reduction, signal quality, compliance, performance), specific issues (high cardinality, PII exposure, missing correlation). Request clarification if incomplete.

### 4. Analyze Current State

Assess observability: signal quality (trace coverage, metric completeness, log correlation), cost efficiency (cardinality optimization, sampling effectiveness, retention policies), compliance (PII redaction, required metadata, audit requirements), performance (instrumentation overhead, telemetry pipeline efficiency), maintainability (code organization, reusable patterns, documentation).

Identify optimization opportunities.

### 5. Generate Refactoring Plan

Create improvements: Signal Quality (add missing instrumentation points, improve span semantics, enhance metric naming, fix log correlation), Cost Optimization (reduce high-cardinality labels, optimize sampling strategy, implement tail-based sampling, adjust retention policies), Compliance Enhancement (implement PII redaction, add required resource attributes, ensure audit trail completeness, validate structured format), Performance Improvements (reduce instrumentation overhead, optimize export batching, implement adaptive sampling, cache telemetry metadata), Code Quality (modular instrumentation design, reusable telemetry utilities, comprehensive testing, clear documentation).

### 6. Implement Refactorings

Generate refactored code: updated instrumentation with best practices, optimized telemetry configuration, enhanced compliance controls, performance improvements, updated documentation.

Include migration guide with testing strategy.

### 7. Validate and Report


Generate refactoring report with cost savings, signal quality improvements, compliance gains. Report completion.

## Error Handling

**Breaking Changes**: Provide backward-compatible migration with feature flags.

**Sampling Changes**: Validate impact on observability before rollout.

**Performance Regression**: Benchmark and optimize instrumentation overhead.

## Examples

**Example 1**: `/refactor-observability Reduce cardinality and optimize costs for order-service` - Output: Optimized telemetry with 40% cost reduction

**Example 2**: `/refactor-observability Add PII redaction to payment-api observability` - Output: Compliant instrumentation with PII safeguards

**Example 3**: `/refactor-observability Improve trace correlation for microservices` - Output: Enhanced context propagation with better correlation

## References

