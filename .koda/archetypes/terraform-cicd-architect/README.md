# Terraform CI/CD Architect Archetype

## Overview
This archetype defines mandatory controls and preferred practices for infrastructure-as-code delivery using Terraform, ensuring compliant, auditable, and resilient deployments.

## Core Principles
*   **State Integrity:** Never run `apply` without remote locking. Drift detection is mandatory.
*   **Policy Compliance:** Do not bypass Sentinel/OPA/Checkov policies.
*   **Secrets Management:** Never commit credentials. Use vault integrations.
*   **Change Governance:** All changes require an approved change record and backout plan.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-terraform-cicd-architect**: Compare plan outputs or state files.
*   **debug-terraform-cicd-architect**: Troubleshoot plan failures or state locking issues.
*   **document-terraform-cicd-architect**: Generate infrastructure documentation.
*   **refactor-terraform-cicd-architect**: Modularize code or update provider versions.
*   **scaffold-terraform-cicd-architect**: specific module generation or pipeline setup.
*   **test-terraform-cicd-architect**: Run policy checks and plan validation.

## Usage
Use `scaffold-terraform-cicd-architect` to create a new module with built-in policy checks. Use `test-terraform-cicd-architect` to run security scans on your IaC before merge.
