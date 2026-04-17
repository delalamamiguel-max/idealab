# Streamlit Developer Archetype

## Overview
This archetype defines the foundational principles and hard-stop rules for generating production-ready data applications using the Streamlit/Python stack, while adhering to AT&T brand guidelines.

## Core Principles
*   **Security:** No hardcoded secrets (use `secrets.toml`); HTTPS required.
*   **Brand Compliance:** AT&T Blue (#009FDB) must be the dominant color in themes.
*   **Input Validation:** All user inputs must be validated.
*   **Performance:** Enforce limits on pagination and queries.
*   **Error Handling:** No silent error swallowing; structured logging is required.
*   **Secure Dependencies:** No incompatible or vulnerable packages.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-streamlit-developer**: Compare app revisions or UI layouts.
*   **debug-streamlit-developer**: Troubleshoot runtime errors or widget issues.
*   **document-streamlit-developer**: Document app functionality and setup.
*   **refactor-streamlit-developer**: Improve code organization or performance.
*   **scaffold-streamlit-developer**: Create a new Streamlit app structure.
*   **test-streamlit-developer**: Validate app logic and UI components.

## Usage
Use `scaffold-streamlit-developer` to create a compliant Streamlit app. Use `debug-streamlit-developer` to fix issues with state management or data display.
