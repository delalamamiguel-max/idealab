# Integration Specialist Archetype

## Overview
This archetype defines the foundational principles and hard-stop rules for defining, building, and maintaining API integrations. It covers API specifications, authentication, and client stub generation.

## Core Principles
*   **Security:** No plaintext credentials; explicit authentication schemes (OAuth2, API Key) required.
*   **Validation:** All specs must be validated (OpenAPI/GraphQL).
*   **No Hard-Coding:** Hostnames, ports, and versions must be parameterized.
*   **Resilience:** Client stubs must include retry and backoff logic.
*   **Contract Tests:** Include tests for both success and failure scenarios.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-integration-specialist**: Compare API specs or integration patterns.
*   **debug-integration-specialist**: Troubleshoot integration failures or spec issues.
*   **document-integration-specialist**: Generate API documentation or integration guides.
*   **refactor-integration-specialist**: Update API specs or client libraries.
*   **scaffold-integration-specialist**: detailed API spec generation.
*   **test-integration-specialist**: Run contract tests against the API.

## Usage
Use `scaffold-integration-specialist` to generate an OpenAPI spec. Use `test-integration-specialist` to verify that the implementation matches the contract.
