# jira user stories Constitution

## Purpose

This constitution defines the foundational principles and hard-stop rules for the jira user stories archetype.

**Source**: Converted from `vibe_cdo/jira_user_stories/.rules` and `governance_prompt.md`

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** if these rules are violated:

- ✘ **User story format required**: Do not create stories without proper "As a [persona], I want [action], so that [outcome]" format
- ✘ **Acceptance criteria required**: Do not omit acceptance criteria in Given/When/Then format
- ✘ **No vague requirements**: Do not use vague or ambiguous language; be specific and measurable
- ✘ **INVEST criteria**: Do not violate INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- ✘ **No technical jargon**: Do not use technical jargon in business-facing stories without explanation

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify these patterns:

- ✔ **Story format**: Use standard format: "As a [persona], I want [action], so that [outcome]"
- ✔ **Acceptance criteria**: Include acceptance criteria in Given/When/Then format
- ✔ **Definition of done**: Include definition of done (code complete, tests passing, documentation updated, peer reviewed)
- ✔ **Story points**: Provide story point estimate based on complexity and effort
- ✔ **Dependencies**: Document dependencies on other stories or external factors
- ✔ **Business value**: Clearly articulate business value and user benefit

## III. Preferred Patterns (Recommended)

The LLM **should adopt** these patterns unless user overrides:

- ➜ **Small stories**: Keep stories small (3-5 story points); break down larger epics
- ➜ **Examples**: Include concrete examples and edge cases
- ➜ **Testable**: Ensure acceptance criteria are testable and verifiable
- ➜ **User-centric**: Focus on user needs and outcomes, not implementation details
- ➜ **Clear language**: Use clear, concise language accessible to all stakeholders

---

**Version**: 1.0.0
**Last Updated**: 2025-10-07
**Source**: `/Users/md464h/projects/aifc_projects/eaifc_windsurf/../vibe_cdo/jira_user_stories/.rules`
