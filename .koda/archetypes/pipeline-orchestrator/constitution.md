# pipeline orchestrator Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the pipeline orchestrator archetype.

**Source**: Converted from `vibe_cdo/pipeline_orchestrator/.rules` and `governance_prompt.md`

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code that violates these rules:

- ✘ **No hard-coded credentials**: Do not hard-code credentials or connection IDs in job definitions or scheduler configurations
- ✘ **Retries required**: Do not omit `retries` or backoff settings in task definitions
- ✘ **Callbacks required**: Do not skip `on_failure_callback` or `on_success_callback` specifications
- ✘ **Structured logging required**: Do not log only plain-text messages without structured metadata
- ✘ **Dependencies required**: Do not define jobs without explicit upstream/downstream dependencies
- ✘ **Idempotent operations**: Do not use non-idempotent operations in job streams (e.g., mutable globals without guards)

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

- ✔ **Retry with backoff**: Include `retries` with exponential backoff (retries ≥3)
- ✔ **Callbacks**: Define both `on_failure_callback` and `on_success_callback` for alerts
- ✔ **Environment variables**: Use Azure Key Vault or environment variables for connection IDs and secrets
- ✔ **Job run tagging**: Tag job runs with `job_run_id`, log `start_date`, `end_date`, and `status`
- ✔ **Parameterization**: Parameterize `schedule_interval`, `start_date`, and `catchup` settings
- ✔ **Dependency validation**: Validate task dependencies and SLA declarations

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Job factory patterns**: Use job factory patterns for modularity and reusability
- ➜ **Function size**: Keep job functions ≤75 lines of code, single responsibility
- ➜ **Naming conventions**: Name job streams and jobs in `snake_case`
- ➜ **Job visualization**: Provide a Mermaid or Graphviz job stream overview in output docs
- ➜ **Documentation**: Include docstrings and inline comments for complex logic

---

**Version**: 1.0.0
**Last Updated**: 2025-10-07
**Source**: `/Users/md464h/projects/aifc_projects/eaifc_windsurf/../vibe_cdo/pipeline_orchestrator/.rules`
