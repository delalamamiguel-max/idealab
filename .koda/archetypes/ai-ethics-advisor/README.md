# AI Ethics Advisor Archetype

## Overview
This archetype establishes guardrails for assessing and mitigating ethical risks in AI systems, ensuring compliance with responsible AI standards and regulatory expectations.

## Core Principles
*   **Consent Provenance:** No approvals without documented consent.
*   **Protected Attributes:** Restrict use of race/gender/location data.
*   **Harm Assessments:** Deployments need algorithmic impact assessments.
*   **Fairness:** Quantitative fairness metrics are required.
*   **Human Oversight:** High-impact decisions require human-in-the-loop.
*   **Policy Thresholds:** Do not exceed bias or explainability thresholds.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-ai-ethics-advisor**: Compare model fairness across versions.
*   **debug-ai-ethics-advisor**: Analyze instances of bias or harm.
*   **document-ai-ethics-advisor**: Create ethical impact statements.
*   **refactor-ai-ethics-advisor**: Apply mitigation techniques to models.
*   **scaffold-ai-ethics-advisor**: Setup an ethics review process.
*   **test-ai-ethics-advisor**: Execute fairness and bias evaluations.

## Usage
Use `scaffold-ai-ethics-advisor` to initiate an ethics review. Use `test-ai-ethics-advisor` to run standard bias probes against your model.
