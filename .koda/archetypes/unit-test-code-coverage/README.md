# Unit Test Code Coverage Archetype

## Overview
This archetype ensures every line of code in the Java project is covered by meaningful unit tests. It governs the creation, execution, and validation of unit tests to maintain high code coverage.

## Core Principles
*   **No Uncovered Paths:** No uncovered methods, branches, or exception paths.
*   **Testable Code:** No untestable code (static blocks, hidden dependencies).
*   **Assertions:** Tests must have assertions.
*   **No Skipped Tests:** No ignored or skipped tests in CI/CD.
*   **No Manual Reliance:** Do not rely on manual testing for core logic.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-unit-test-code-coverage**: Compare coverage reports between builds.
*   **debug-unit-test-code-coverage**: Identify why tests are failing or coverage is low.
*   **document-unit-test-code-coverage**: Generate coverage reports.
*   **refactor-unit-test-code-coverage**: Improve existing tests or make code more testable.
*   **scaffold-unit-test-code-coverage**: Generate test skeletons for classes.
*   **test-unit-test-code-coverage**: Run the unit tests and check coverage rules.

## Usage
Run `scaffold-unit-test-code-coverage` for new classes. Use `debug-unit-test-code-coverage` to troubleshoot gaps in coverage reports.
