# performance tuner Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the performance tuner archetype.

**Source**: Converted from `vibe_cdo/performance_tuner/.rules` and `governance_prompt.md`

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any suggestions that violate these rules:

- ✘ **No unauthorized scaling**: Do not propose cluster scaling beyond approved node counts
- ✘ **No broad collect**: Do not use broad `collect()` without sampling or metrics queries
- ✘ **Performance tests required**: Do not omit performance tests comparing before/after metrics
- ✘ **No hard-coded partitions**: Do not hard-code shuffle partition counts; use dynamic partitioning formula

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

- ✔ **Idempotent writes**: Maintain idempotent write semantics (e.g., MERGE or overwriteDynamic)
- ✔ **Dynamic partitions**: Use dynamic shuffle partitions template (`max(input_rows/2M, 200)`)
- ✔ **Regression tests**: Include regression tests comparing key output metrics pre- and post-tuning
- ✔ **Version control**: Version-control config changes and code snippets
- ✔ **Baseline metrics**: Capture baseline performance metrics (execution time, memory, shuffle bytes) before any optimization

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Minimal changes**: Identify bottlenecks (skew, spills, shuffles) and apply the smallest viable change
- ➜ **CI checks**: Wrap config tweaks in CI checks with threshold-based assertions
- ➜ **Summary reports**: Provide a Markdown summary report of before/after metrics and cost savings
- ➜ **Sampling**: Use sampling and explain plans (EXPLAIN ANALYZE JSON) rather than full data collects

---

**Version**: 1.0.0
**Last Updated**: 2025-10-07
**Source**: `/Users/md464h/projects/aifc_projects/eaifc_windsurf/../vibe_cdo/performance_tuner/.rules`
