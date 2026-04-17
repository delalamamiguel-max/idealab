# Automation Scripter Archetype

## Overview
This archetype defines the foundational principles and hard-stop rules for creating automation scripts. It governs all workflows, ensuring scripts are secure, reliable, and standardized.

## Core Principles
*   **Security:** Never expose credentials or secrets in code or logs.
*   **Environment Variables:** Always source credentials from environment variables or vault CLI.
*   **TLS Enforcement:** Always enforce TLS 1.2+ for HTTP calls.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-automation-scripter**: Compare script versions or logic.
*   **debug-automation-scripter**: Analyze script failures or error logs.
*   **document-automation-scripter**: Generate usage documentation for scripts.
*   **refactor-automation-scripter**: Improve script efficiency or readability.
*   **scaffold-automation-scripter**: Create a new automation script template.
*   **test-automation-scripter**: Validate script execution and error handling.

## Usage
Use `scaffold-automation-scripter` to create a new script. Always check `test-automation-scripter` to ensure your script handles secrets securely.
