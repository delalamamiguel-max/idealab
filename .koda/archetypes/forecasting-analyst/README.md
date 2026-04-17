# Forecasting Analyst Archetype

## Overview
This archetype governs time series forecasting workflows that turn temporal telemetry into trustworthy business signals with reproducible backtesting and calibrated uncertainty.

## Core Principles
The following hard-stop rules must be strictly followed:
- **Ignores temporal integrity**: Reject any pipeline with time leakage.
- **Skips out-of-sample validation**: Rolling backtests are mandatory.
- **Omits uncertainty disclosures**: Provide prediction intervals and scenario bands.
- **Disregards business calendars**: Reconcile fiscal calendars and holidays.
- **Deploys without monitoring**: Require drift detection and retraining triggers.
- **Masks demand deficits**: Do not suppress negative variance versus plan.
- **Bypasses governance**: Azure DevOps review and MLflow registration are required.
- **Uses ambiguous naming**: Follow the domain-timeseries-signal-granularity convention.

## Standard Pattern
Implementations must demonstrate:
- **Documented forecasting charter**: Horizon, granularity, seasonality, exogenous drivers.
- **Time-aware feature pipelines**: Point-in-time correctness and late-arriving handling.
- **Rolling backtesting**: Sliding/expanding windows aligned to rolling_window_days.
- **Baseline benchmarking**: Naive and seasonal benchmarks with variance attribution.
- **Uncertainty quantification**: Intervals, scenario bands, and risk classifications.
- **Model risk reporting**: Coverage gaps, drift indicators, and mitigation playbooks.
- **Automated CI/CD hooks**: MLflow, Databricks jobs, and Azure DevOps approvals.
