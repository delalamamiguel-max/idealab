# Python Library Upgrade Archetype

## Overview
This archetype ensures all Python dependencies are up-to-date, secure, and compatible with the current codebase.

## Core Principles
*   **No Unsupported Libraries:** Do not use libraries that are end-of-life.
*   **No Known Vulnerabilities:** Dependencies must be clear of known security flaws.
*   **No Deprecated APIs:** Identify and replace usage of deprecated APIs.
*   **Pinned Versions:** Production environments must use pinned versions.
*   **Documentation:** Upgrades must document min/max versions and runtime compatibility.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-python-library-upgrade**: detailed comparison of package versions.
*   **debug-python-library-upgrade**: Resolve dependency conflicts (pip/poetry).
*   **document-python-library-upgrade**: Update `requirements.txt` or `pyproject.toml` docs.
*   **refactor-python-library-upgrade**: Update code to align with new library APIs.
*   **scaffold-python-library-upgrade**: Initialize an upgrade process.
*   **test-python-library-upgrade**: Run tests to confirm upgrade stability.

## Usage
Run `debug-python-library-upgrade` to resolve dependency conflicts. Use `refactor-python-library-upgrade` to modernize code after a library update.
