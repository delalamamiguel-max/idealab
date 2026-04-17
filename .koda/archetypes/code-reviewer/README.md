# Code Reviewer Archetype

## Mission Statement
Establish a AI assisted, consistent code and peer review practice that improves correctness, security, performance, and maintainability—so every change is understandable, testable, and safe to operate in production.

The **Code Reviewer** is the gatekeeper of architectural standards in this repo. It ensures that every line of Snowflake SQL, Python, or Shell script adheres to the core rules of security, performance, and reliability.

## Quick Start
To invoke the reviewer manually:
`@code-reviewer /compare --target path/to/files`

## Features
- **Loud Alerts**: Hard-stop violations (secrets, data corruption) are highlighted immediately.
- **Subtle Guidance**: Quality improvements are grouped to maintain workflow flow without clutter.
- **Fix-it Snippets**: Every violation comes with a logic-based fix suggestion.
- **No-Git Tracking**: Uses session metadata and file timestamps to identify what needs review.

## Integration
This archetype is mandated to run after any modification by the **Core Orchestrator**. 
It will always prompt for a `Code_Review.md` location before finishing.

## Constitution
See [code-reviewer-constitution.md](code-reviewer-constitution.md) for the full list of rules.
