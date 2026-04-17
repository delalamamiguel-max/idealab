# Java Library Upgrade Archetype

## Overview
This archetype governs the detection, analysis, and upgrade of outdated Java libraries to ensure they are current, secure, and compatible with the codebase.

## Core Principles
*   **No Deprecated Libraries:** Avoid using deprecated or unsupported libraries.
*   **No Known Vulnerabilities:** Dependencies must be free of known CVEs.
*   **Pinned Versions:** Production builds must use pinned versions.
*   **Mitigation Plans:** No breaking changes without a mitigation plan.
*   **Regression Testing:** No upgrade is complete without regression testing.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-java-library-upgrade**: Compare dependency trees and versions.
*   **debug-java-library-upgrade**: Troubleshoot upgrade conflicts or failures.
*   **document-java-library-upgrade**: Generate upgrade reports and changelogs.
*   **refactor-java-library-upgrade**: Update code to support new library versions.
*   **scaffold-java-library-upgrade**: Create upgrade tasks or branches.
*   **test-java-library-upgrade**: Verify that the application works with upgrades.

## Usage
Use `scaffold-java-library-upgrade` to identify available updates. Then use `refactor-java-library-upgrade` to help with the code changes required for the upgrade.
