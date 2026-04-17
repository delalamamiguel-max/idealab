# AKS DevOps Deployment Archetype

## Overview
This archetype defines the foundational principles and hard-stop rules for deploying Java-based applications to Azure Kubernetes Service (AKS) using DevOps practices. It ensures reliability, scalability, and maintainability of cloud-native deployments.

## Core Principles
*   **Versioned Images:** No unversioned container images.
*   **Staged Deployments:** No direct deployment to production without staging validation.
*   **Secret Management:** No hardcoded secrets; use Azure Key Vault or Kubernetes Secrets.
*   **Resource Management:** Resource limits and requests are mandatory in manifests.
*   **Health Checks:** Deployments must have health checks and readiness probes.
*   **Infrastructure as Code:** No manual configuration changes in AKS clusters.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-aks-devops-deployment**: Compare deployment manifests or strategies.
*   **debug-aks-devops-deployment**: Troubleshoot deployment failures or pod crashes.
*   **document-aks-devops-deployment**: Generate deployment documentation or runbooks.
*   **refactor-aks-devops-deployment**: Optimize Helm charts or pipeline configurations.
*   **scaffold-aks-devops-deployment**: Create a new AKS deployment pipeline/manifests.
*   **test-aks-devops-deployment**: Validate manifests and run deployment tests.

## Usage
Use `scaffold-aks-devops-deployment` to generate Helm charts and pipeline configs. Use `test-aks-devops-deployment` to validate your Kubernetes manifests before applying them.
