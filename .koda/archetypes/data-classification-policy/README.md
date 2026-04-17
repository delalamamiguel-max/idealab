# Data Classification Policy Archetype

## Overview
This archetype establishes guardrails for governing Sensitive Personal Information (SPI) and Personally Identifiable Information (PII), ensuring compliance with data classification policies and zero-trust security.

## Core Principles
*   **Classification Mapping:** No processing without explicit SPI/PII inventory.
*   **Least Privilege:** Access granted only to minimum required identities.
*   **Encryption:** AES-256 at rest and TLS 1.2+ in transit are mandatory.
*   **Consent:** Data usage must have recorded consent or legal basis.
*   **Breach Response:** Incident playbooks and notification SLAs are required.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-data-classification-policy**: Compare policy definitions or tags.
*   **debug-data-classification-policy**: Investigate access denials or policy violations.
*   **document-data-classification-policy**: Generate data inventory and classification reports.
*   **refactor-data-classification-policy**: Update tags or policies to match new regulations.
*   **scaffold-data-classification-policy**: Apply classification tags to a dataset.
*   **test-data-classification-policy**: Verify reliable enforcement of access controls.

## Usage
Use `scaffold-data-classification-policy` to tag new datasets. Use `document-data-classification-policy` to prove compliance with data residency and privacy laws.
