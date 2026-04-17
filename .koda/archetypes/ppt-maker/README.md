# PPT-Maker Archetype

## Overview
This archetype automates the generation of professional, AT&T-branded PowerPoint presentations using YAML specifications and programmatic or image-based diagrams.

## Core Principles
*   **Character Limits:** Adhere to field limits defined in the configuration.
*   **Template Conformance:** Use the YAML + library approach; do not create ad-hoc scripts.
*   **Aspect Ratio Tolerance:** Images must not be distorted by more than 10%.
*   **No Placeholder Text:** All content must be final; no "Lorem ipsum" allowed.
*   **Mandatory Slides:** Must include a Title slide and a Final slide.
*   **Asset Management:** YAML specs and images must reside in the designated assets folder.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-ppt**: Compare presentation updates or specifications.
*   **debug-ppt**: Troubleshoot issues in the YAML spec or generation process.
*   **document-ppt**: Document the structure or content of the presentation.
*   **refactor-ppt**: Update YAML specs to improve flow or meet new requirements.
*   **scaffold-ppt**: Create a basic YAML structure for a new presentation.
*   **test-ppt**: Validate the YAML spec and assets against the constitution rules.

## Usage
Define your presentation content in a YAML file following the schema, then use `scaffold-ppt` or `refactor-ppt` to manage the lifecycle of your slide deck generation.
