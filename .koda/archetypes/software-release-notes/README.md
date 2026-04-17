# Software Release Notes Archetype

## Overview
This archetype defines the principles and rules for generating comprehensive release notes from JIRA user stories across one or more sprints. It ensures clarity, traceability, and business relevance.

## Core Principles
*   **No Missing Stories:** All completed stories from selected sprints must be included.
*   **Clear Descriptions:** Functionality must be described clearly, avoiding vagueness.
*   **Metadata:** Must include Story ID, title, sprint, and business impact.
*   **Verified Status:** Only "Done" or "Closed" stories are eligible appropriately.
*   **Format:** Stories must follow the "As a... I want... so that..." pattern in the notes.
*   **Traceability:** Must reference git commits, PRs, or tags.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-software-release-notes**: Compare draft release notes against source stories.
*   **debug-software-release-notes**: Identify missing stories or data gaps.
*   **document-software-release-notes**: Generate the actual release notes document.
*   **refactor-software-release-notes**: Improve the clarity or formatting of existing notes.
*   **scaffold-software-release-notes**: Create the initial draft of release notes.
*   **test-software-release-notes**: Verify the release notes against the rules (e.g., no missing items).

## Usage
Use this archetype at the end of a sprint or release cycle. Run `scaffold-software-release-notes` to generate a draft from your issue tracker data, then refine it.
