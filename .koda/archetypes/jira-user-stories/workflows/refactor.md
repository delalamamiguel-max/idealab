---
description: Refactor Jira user stories to improve clarity, completeness, and acceptance criteria (Jira User Stories)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype jira-user-stories --json ` and parse for JIRA_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/jira-user-stories/templates/env-config.yaml` for story templates, acceptance criteria patterns

### 3. Parse Input
Extract from $ARGUMENTS: existing story ID or text, refactoring goals (improve clarity, add acceptance criteria, break down epic, add subtasks), constraints. Request clarification if incomplete.

### 4. Analyze Existing Story
Load and analyze existing user story: identify issues (vague user story, missing acceptance criteria, no definition of done, unclear business value, missing edge cases, no test scenarios, large story needing breakdown), identify missing elements (clear user persona, specific action, measurable outcome, INVEST criteria compliance, testable acceptance criteria), identify improvement opportunities (add examples, clarify edge cases, add technical notes, link dependencies).

Report findings with specific improvement recommendations.

### 5. Generate Refactored Story

Create refactored user story applying improvements: rewrite user story in clear format (As a [persona], I want [action], so that [outcome]), add comprehensive acceptance criteria (Given/When/Then format, positive and negative scenarios, edge cases), add definition of done (code complete, tests passing, documentation updated, peer reviewed), break down large stories (create subtasks, define dependencies, estimate story points), add technical notes and examples.

Include complete story template with all required fields.

### 6. Add Recommendations

Include suggestions for story points estimation, sprint planning considerations, dependency management, risk identification, and testing strategy.

Provide summary of improvements with clarity enhancements and completeness metrics.

### 7. Validate and Report


Generate optional story breakdown and dependency map. Report completion with story improvements, next steps.

## Error Handling

**Vague Story**: Explain issues, show specific improvements with clear persona, action, and outcome.

**Incomplete Input**: List missing information, provide well-formed example.

**Environment Failure**: Report missing Jira configuration, suggest setup steps.

## Examples

**Example 1: Clarify Vague Story**
```
/refactor-stories Improve clarity of PROJ-123 user story

Input: "Users need better reports"
Output: Refactored with specific persona, action, outcome, acceptance criteria
```

**Example 2: Add Acceptance Criteria**
```
/refactor-stories Add comprehensive acceptance criteria to PROJ-456

Input: Story with no acceptance criteria
Output: Refactored with Given/When/Then scenarios, edge cases, DoD
```

**Example 3: Break Down Epic**
```
/refactor-stories Break down large story PROJ-789 into manageable subtasks

Input: 20-point story covering multiple features
Output: Refactored into 5 smaller stories with dependencies and estimates
```

## References

