# Documentation Evangelist Archetype

## Overview
This archetype defines the foundational principles and hard-stop rules for creating, maintaining, and auditing project documentation. It ensures clarity, consistency, and adherence to company standards.

## Core Principles
*   **Line Length Limit:** Lines must not exceed 100 characters to ensure readability.
*   **Metadata Requirement:** All documentation must include a metadata block (version, author, last updated).
*   **Valid Diagrams:** Diagrams must use valid Mermaid syntax or be standard image formats.
*   **No Hard-Coded Links:** External references should be parameterized.
*   **Required Sections:** Documentation must include Overview, Data Flow, Schema Definitions, and Metrics Glossary.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-documentation**: Compare documentation versions or standards.
*   **debug-documentation**: Identify and fix issues in existing documentation or rendering.
*   **document-documentation**: Generate new documentation based on the constitution.
*   **refactor-documentation**: Update documentation structure to meet new standards.
*   **scaffold-documentation**: Create a skeleton structure for new documentation.
*   **test-documentation**: Validate documentation against quality rules and schema.

## Usage
Select the appropriate workflow for your task. For example, use `scaffold-documentation` when starting a new document, or `test-documentation` to verify compliance with the constitution.
