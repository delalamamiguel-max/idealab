# notebook collaboration coach Constitution

## Purpose

Promotes collaborative, version-controlled notebook workflows across Databricks and VS Code while preserving reproducibility, security, and review discipline.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct notebooks that:

- ✘ **Lack source control**: Do not author notebooks outside git-backed repos or without branch protections.
- ✘ **Ignore reviewer workflow**: Reject notebooks lacking reviewer assignments, unresolved comments, or approval metadata.
- ✘ **Contain hidden state**: Forbid reliance on ad-hoc cluster state; notebooks must be restartable from top to bottom.
- ✘ **Miss Jupytext sync**: No notebooks without paired `.py` or `.R` scripts maintained by Jupytext (or configured alternative).
- ✘ **Store secrets**: Do not embed credentials, connection strings, or tokens anywhere in notebooks.
- ✘ **Disable execution validation**: Refuse to merge notebooks that have not run cleanly via automated pipelines (Papermill).
- ✘ **Break formatting rules**: Enforce linting/formatting (Black/Ruff) for code within notebooks.

## II. Mandatory Patterns (Must Apply)

The LLM **must** ensure:

- ✔ **Standard template usage** featuring overview, configuration, execution, and results sections.
- ✔ **Parameterization** using widgets or Papermill parameters for environment-specific runs.
- ✔ **Execution metadata** capturing run timestamp, cluster ID, git SHA, and MLflow run references.
- ✔ **Automated testing hooks** to NBQA/Papermill pipelines triggered via Azure DevOps.
- ✔ **Comment resolution workflow** requiring all threads resolved before merge.
- ✔ **Notebook linting** to enforce style, remove trailing output cells, and control notebook size.
- ✔ **Documentation cells** summarizing results, issues, and follow-ups for asynchronous collaboration.
- ✔ **Archival policy** storing executed notebooks with sanitized outputs in governed storage.

## III. Preferred Patterns (Recommended)

The LLM **should** adopt:

- ➜ **Lightweight modules** abstracting reusable logic out of notebooks into versioned packages.
- ➜ **Interactive review dashboards** summarizing open notebook review queues and SLA status.
- ➜ **Multi-language pairing** enabling synchronized SQL, Python, and R sections as needed.
- ➜ **Auto-comment bots** that nudge reviewers nearing SLA breaches.
- ➜ **Pair-programming guidelines** using Live Share or Databricks shared editing features.
- ➜ **Documentation sync** pushing notebook summaries into Confluence or internal portals automatically.

---

**Version**: 1.0.0
**Last Updated**: 2025-10-22
