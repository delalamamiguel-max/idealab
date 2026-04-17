# Key Vault Config Steward Archetype

## Overview
This archetype defines guardrails for producing a reusable configuration layer that sources secrets from Azure Key Vault with typed fallbacks and operational observability.

## Core Principles
*   **Key Vault First:** Do not bypass Key Vault when a managed secret exists.
*   **No Secrets in Code:** Never embed secrets in source files.
*   **Typed Configuration:** Use Pydantic models for configuration objects.
*   **Error Handling:** Surface actionable errors; do not swallow exceptions.
*   **Fallback Policy:** Respect the `Key Vault -> Env Vars -> .env` fallback order.
*   **Auditing:** Maintain diagnostic logging and access policy telemetry.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-key-vault-config-steward**: Compare config schemas or secret mappings.
*   **debug-key-vault-config-steward**: Troubleshoot secret retrieval or access issues.
*   **document-key-vault-config-steward**: Generate config documentation.
*   **refactor-key-vault-config-steward**: Update config models or secret handling logic.
*   **scaffold-key-vault-config-steward**: Create a new configuration loader.
*   **test-key-vault-config-steward**: Verify secret resolution and fallback logic.

## Usage
Use `scaffold-key-vault-config-steward` to generate a secure configuration module. Use `test-key-vault-config-steward` to verify that your application correctly falls back to environment variables when Key Vault is unreachable (in dev).
