# Responsible Prompting Archetype

## Overview
This archetype safeguards prompt engineering practices, ensuring that language model interactions are safe, inclusive, policy-aligned, and auditable while enabling high-quality performance.

## Core Principles
*   **Safety Classification:** Every prompt/agent must have a mapped risk profile.
*   **Policy Alignment:** Must align with privacy, copyright, and safety policies.
*   **Content Safety:** No hate, harassment, self-harm, or violent content.
*   **Data Privacy:** No user data collection without declared purpose and consent.
*   **Transparency:** Opaque prompt-chaining is prohibited.

## Available Workflows
The following workflows are available in the `workflows/` directory:

*   **compare-responsible-prompting**: Compare prompt versions for safety deviations.
*   **debug-responsible-prompting**: Analyze prompt failures or safety triggers.
*   **document-responsible-prompting**: Create safety case documentation.
*   **refactor-responsible-prompting**: Update prompts to meet better safety standards.
*   **scaffold-responsible-prompting**: Create a new safe prompt template.
*   **test-responsible-prompting**: Run adversarial testing on prompts.

## Usage
Use `scaffold-responsible-prompting` to design new prompts with built-in safety checks. Use `test-responsible-prompting` to validate your prompts against jailbreak attempts.
