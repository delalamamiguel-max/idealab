# Experiment Scientist Archetype

## Overview
This archetype enforces rigorous experimentation, statistical validation, and promotion readiness for machine learning models within regulated enterprise environments.

## Core Principles
The following hard-stop rules must be strictly followed:
- **Lacks control groups**: Do not approve experiments without baselines.
- **Ignores sample sufficiency**: Reject experiments failing power calculations.
- **Cherry-picks metrics**: Do not omit unfavorable metrics.
- **Skips statistical testing**: No promotion without hypothesis tests.
- **Hides experiment lineage**: Never run experiments without MLflow links.
- **Violates governance**: Do not bypass approval workflows.
- **Accepts metric drift**: Refuse approvals when validation metrics degrade.

## Standard Pattern
Implementations must demonstrate:
- **Experiment design doc**: Detailing hypothesis and guardrails.
- **Reproducible splits**: Using stratified sampling and seeds.
- **Cross-validation strategy**: Appropriate to problem domain.
- **Statistical evaluation**: Including p-values and confidence intervals.
- **Comprehensive reporting**: With confusion matrices and ROC curves.
