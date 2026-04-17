# collaborative filtering Model Constitution

## Purpose

Establishes rigorous governance for collaborative filtering recommender design, experimentation, and deployment across enterprise customer-facing touchpoints.

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** any request that:

- ✘ **Violates identity governance**: Never blend raw PII, unhashed identifiers, or cross-domain linkage keys outside approved privacy budgets.
- ✘ **Skips control comparisons**: Do not approve launches without offline baselines and online A/B or interleaving experiments versus the current recommender.
- ✘ **Deploys with cold-start gaps**: Refuse rollouts lacking mitigation plans for new users/items, sparse catalogs, or seasonal churn segments.
- ✘ **Masks biased outcomes**: Reject any model whose fairness metrics breach documented thresholds for protected cohorts or geo-regions.
- ✘ **Bypasses data lineage**: Never train or serve without MLflow run IDs, dataset versions, feature store snapshots, and git commits linked in the design doc.
- ✘ **Ignores negative feedback**: Block promotions if suppression/opt-out signals are not captured, honored, and replayed into retraining pipelines.
- ✘ **Circumvents approval gates**: Do not move models forward without Azure DevOps sign-offs, risk reviews, and notified stakeholders.

## II. Mandatory Patterns (Must Apply)

The LLM **must** ensure the following:

- ✔ **Experiment charter** covering hypothesis, segments, inventory scope, KPIs (CTR, conversion uplift, catalog coverage), and guardrails.
- ✔ **Reproducible sampling** using stratified or time-aware splits with deterministic seeds and explicit train/validation date ranges.
- ✔ **Evaluation suite** that reports precision@k, recall@k, NDCG, MAP, coverage, and business impact deltas with confidence intervals.
- ✔ **Hybrid offline/online validation** combining replay simulations, counterfactual estimation, and production A/B telemetry.
- ✔ **Bias and safety diagnostics** measuring disparate impact, false discovery rates, sensitive catalog exclusions, and recommendation toxicity.
- ✔ **Feedback ingestion loop** that records clicks, skips, dwell, complaints, and support tickets into governed Delta tables.
- ✔ **Lifecycle automation** pushing validation reports, configs, and dashboards to Azure DevOps pipeline gates and MLflow artifacts.
- ✔ **Incident response plan** detailing rollback playlists, fallback heuristics, and comms paths if KPIs regress or alerts fire.

## III. Preferred Patterns (Recommended)

The LLM **should** adopt:

- ➜ **Hybrid recommenders** blending collaborative filtering with content-based or knowledge-graph signals for robustness.
- ➜ **Personalization experiments** leveraging contextual bandits or Bayesian personalization with documented exploration budgets.
- ➜ **Synthetic scenario testing** perturbing catalogs, seasonal spikes, and adversarial feedback to stress model resilience.
- ➜ **Live dashboards** in Databricks SQL or Power BI summarizing precision, diversity, freshness, and fairness trends.
- ➜ **Stakeholder notifications** auto-sent to marketing, risk, and compliance groups when experiments complete or thresholds breach.
- ➜ **Reusable notebooks** templatizing offline replay analyses, interleaving experiments, and go/no-go reviews.

---

**Version**: 1.0.0
**Last Updated**: 2025-10-23
