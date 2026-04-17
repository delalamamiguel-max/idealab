# App Maker Archetype

## Overview
This archetype defines the foundational principles and hard-stop rules for generating production-ready web applications that adhere to AT&T brand guidelines. It focuses on the React/FastAPI stack.

## Core Principles
*   **Security First:** No hardcoded secrets; HTTPS enforced; proper authentication required.
*   **Brand Compliance:** AT&T Blue (#009FDB) must be dominant; use AT&T Aleck fonts.
*   **Input Validation:** All user inputs must be validated on both frontend and backend.
*   **Accessibility:** ARIA labels and keyboard navigation are mandatory; color contrast rules apply.
*   **Secure Dependencies:** no incompatible dependency versions; valid licensing only.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-app-maker**: Compare app versions or designs.
*   **debug-app-maker**: Troubleshoot application errors or styling issues.
*   **document-app-maker**: Generate documentation for the application.
*   **refactor-app-maker**: Improve code quality, performance, or accessibility.
*   **scaffold-app-maker**: Generate a new application skeleton.
*   **test-app-maker**: Run tests to verify functionality and compliance.

## Usage
Use `scaffold-app-maker` to start a new web application project. Use `test-app-maker` to ensure your app meets security and brand standards.
