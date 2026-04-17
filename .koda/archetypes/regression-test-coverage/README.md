# Regression Test Coverage Archetype

## Overview
This archetype manages the automated creation, execution, and verification of regression test suites. Its primary goal is to ensure that previously validated functionality remains intact after code changes.

## Core Principles
*   **No Untested Journeys:** Critical user journeys and workflows must be covered.
*   **Deterministic Assertions:** Regenerated test code must have deterministic assertions.
*   **Automated Verification:** Do not rely on manual verification for regression scope.
*   **Flaky Tests:** No flaky tests are admitted into the suite.
*   **Version Control:** All test runs must have version-controlled logs and reports.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-regression-test-coverage**: Compare test coverage between versions.
*   **debug-regression-test-coverage**: Analyze failures and flaky tests.
*   **document-regression-test-coverage**: Generate reports on test coverage and gaps.
*   **refactor-regression-test-coverage**: Optimize existing regression suites.
*   **scaffold-regression-test-coverage**: Generate new regression test cases.
*   **test-regression-test-coverage**: Validate the regression suite itself.

## Usage
Use this archetype to maintain the health of your project's regression suite. Run `scaffold-regression-test-coverage` when adding new features, and `test-regression-test-coverage` to verify the suite's integrity.
