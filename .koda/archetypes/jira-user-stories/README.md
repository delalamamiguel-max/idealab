# JIRA User Stories Archetype

## Overview
This archetype governs the creation and refinement of JIRA user stories, ensuring they meet strict quality standards and follow the INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable).

## Core Principles
*   **User Story Format:** Must use "As a [persona], I want [action], so that [outcome]".
*   **Acceptance Criteria:** Must be included in the Given/When/Then format.
*   **No Vague Requirements:** Requirements must be specific and measurable.
*   **No Technical Jargon:** Avoid technical jargon in business-facing stories without explanation.
*   **Definition of Done:** Must include standard DoD elements (code complete, tests passing, etc.).

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-stories**: Compare different versions or sets of user stories.
*   **debug-stories**: Analyze and fix issues in user stories (e.g., missing criteria).
*   **document-stories**: generate documentation or summaries from user stories.
*   **refactor-stories**: Improve the quality or clarity of existing stories.
*   **scaffold-stories**: Create new user stories from raw requirements.
*   **test-stories**: Validate stories against the rules (INVEST, format, etc.).

## Usage
Use this archetype when grooming the backlog or creating new work items. Select `scaffold-stories` to generate compliant stories, or `test-stories` to validate existing ones.
