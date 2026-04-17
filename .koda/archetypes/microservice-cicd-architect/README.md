# Microservice CI/CD Architect Archetype

## Overview
This archetype codifies the non-negotiable guardrails and preferred operating model for Microservice CI/CD pipelines, ensuring secure, reliable, and auditable software delivery.

## Core Principles
*   **Supply Chain Security:** Sign container images; enforce vulnerability scanning.
*   **Deployment Safety:** No direct production deployment without staged gates.
*   **Observability:** Emit structured deploy events (timestamp, service, version).
*   **Auditability:** Retain release logs for at least 90 days.
*   **Emergency Protocol:** Never bypass approvals unless following emergency protocols.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-microservice-cicd-architect**: Compare pipeline stages or policies.
*   **debug-microservice-cicd-architect**: Resolve pipeline failures or security blocks.
*   **document-microservice-cicd-architect**: Document pipeline architecture and gates.
*   **refactor-microservice-cicd-architect**: Improve pipeline efficiency or security.
*   **scaffold-microservice-cicd-architect**: Generate a new CI/CD pipeline definition.
*   **test-microservice-cicd-architect**: Validate pipeline logic and security controls.

## Usage
Use `scaffold-microservice-cicd-architect` to build a compliant pipeline. Use `refactor-microservice-cicd-architect` to add security scanning to legacy pipelines.
