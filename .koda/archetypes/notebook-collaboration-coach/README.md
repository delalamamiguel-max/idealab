# Notebook Collaboration Coach Archetype

## Overview
This archetype promotes collaborative, version-controlled notebook workflows across Databricks and VS Code. It aims to preserve reproducibility, security, and review discipline in notebook-based development.

## Core Principles
*   **Source Control:** Notebooks must be in git-backed repos.
*   **Review Workflow:** Assignments and comments must be resolved before merge.
*   **Reproducibility:** No hidden state; notebooks must run top-to-bottom.
*   **Jupytext Sync:** Maintain paired `.py` or `.R` scripts.
*   **Security:** No secrets embedded in notebooks.
*   **Execution Verification:** Notebooks must run cleanly in automated pipelines (Papermill).

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-notebook-collaboration-coach**: Compare notebook cells and outputs efficiently.
*   **debug-notebook-collaboration-coach**: Fix execution errors or state issues.
*   **document-notebook-collaboration-coach**: Add documentation cells and summaries.
*   **refactor-notebook-collaboration-coach**: Clean up code and apply formatting rules.
*   **scaffold-notebook-collaboration-coach**: Create a new notebook with the standard template.
*   **test-notebook-collaboration-coach**: Verify notebook execution and linting.

## Usage
Use `scaffold-notebook-collaboration-coach` to start a new analysis. Use `refactor-notebook-collaboration-coach` to prepare a notebook for peer review.
