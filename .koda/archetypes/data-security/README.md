# Data Security Architect Archetype

## Overview
This archetype safeguards data assets across their lifecycle by enforcing encryption, minimizing exposure of sensitive information, and establishing proactive detection of insecure patterns.

## Core Principles
*   **Encryption:** Regulated SPI must be encrypted/tokenized at rest.
*   **Transport Security:** TLS 1.2+ required.
*   **Key Rotation:** Adhere to defined key rotation SLAs.
*   **Audit Logging:** No truncation of security event logs.
*   **Secrets:** No secrets in source control.
*   **Retention:** Enforce retention windows and legal holds.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-data-security**: Compare security configurations.
*   **debug-data-security**: Investigate potential vulnerabilities.
*   **document-data-security**: Generate security architecture documentation.
*   **refactor-data-security**: Implement encryption or tokenization patterns.
*   **scaffold-data-security**: Setup security controls for a new system.
*   **test-data-security**: Run SAST/DAST checks on data components.

## Usage
Use `scaffold-data-security` to design the security layer for a new data product. Use `test-data-security` to validate that encryption compliance is met.
