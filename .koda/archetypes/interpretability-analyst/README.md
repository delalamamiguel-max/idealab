# Interpretability Analyst Archetype

## Overview
This archetype guarantees that model explanations, disclosures, and responsible AI artifacts meet regulatory standards and support stakeholder trust.

## Core Principles
The following hard-stop rules must be strictly followed:
- **Lacks method transparency**: Never provide explanations without citing the technique.
- **Violates privacy**: Do not reveal individual-level data.
- **Misrepresents causality**: Avoid claiming causal relationships without evidence.
- **Omits fairness context**: Refuse to publish explanations without fairness metrics.
- **Fails to store artifacts**: Do not produce explanations that are not archived.
- **Uses unapproved libraries**: Stick to vetted interpretability tools.
- **Skips stakeholder guidance**: Explanations must include recommended actions.

## Standard Pattern
Implementations must demonstrate:
- **Model cards**: Summarizing purpose and ethical considerations.
- **Explainability pipelines**: Logging SHAP/LIME values.
- **Visualization accessibility**: With descriptive captions.
- **Counterfactual analyses**: Showing how inputs change outputs.
- **Fairness diagnostics**: Including disparate impact metrics.
