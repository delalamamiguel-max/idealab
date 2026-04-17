# Inference Orchestrator Archetype

## Overview
This archetype ensures safe, observable, and cost-aware deployment of MLflow-registered models to Azure AKS and associated serving targets for both batch and real-time inference.

## Core Principles
The following hard-stop rules must be strictly followed:
- **Bypasses MLflow registry**: Never deploy models not in 'Production' stage.
- **Disables observability**: Reject services without App Insights/Prometheus.
- **Ignores security controls**: Do not expose endpoints without TLS/Auth.
- **Omits rollback plans**: No deployments without automated rollback.
- **Skips load testing**: Refuse go-lives lacking performance tests.
- **Uses unmanaged containers**: All images must be from approved registries.
- **Forgets contract enforcement**: Do not deploy without schema validation.

## Standard Pattern
Implementations must demonstrate:
- **Infrastructure-as-code**: Definitions for AKS and ingress.
- **Traffic management strategy**: Canary or blue/green gates.
- **Batch + streaming pathways**: Documenting scheduling and retry.
- **Automated drift hooks**: Sending predictions to monitoring.
- **Security posture**: Managed identities and Key Vault.
