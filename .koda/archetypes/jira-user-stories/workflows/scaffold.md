---
description: Generate high-quality Jira user stories with acceptance criteria and subtasks (Jira User Stories)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype jira-user-stories --json ` and parse for JIRA_URL, PROJECT_KEY, STORY_TEMPLATE, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/jira-user-stories/templates/env-config.yaml` for project key, epic links, story point scale

### 3. Parse Input
Extract from $ARGUMENTS: feature description, user persona, business value, technical requirements, dependencies. Request clarification if incomplete.

### 4. Validate Constraints
Check against hard-stop rules:
- ✘ Refuse stories without clear acceptance criteria
- ✘ Refuse missing business value or user persona
- ✘ Refuse stories too large (>13 story points) without breakdown
- ✘ Refuse unclear or ambiguous requirements
If violated, explain clearly and suggest compliant alternative.

### 5. Generate User Story

Create INVEST-compliant user story with structure: title (concise, action-oriented), user story format (As a [persona], I want [goal], So that [benefit]), description (context, background, constraints), acceptance criteria (Given/When/Then format or checklist), technical notes (implementation hints, architecture considerations), subtasks (breakdown of implementation steps), story points (estimation using Fibonacci scale), labels and components (categorization), dependencies (blocked by, blocks).

INVEST criteria validation: Independent (can be developed standalone), Negotiable (details can be discussed), Valuable (delivers user/business value), Estimable (team can estimate effort), Small (completable in one sprint), Testable (clear acceptance criteria).

Acceptance criteria patterns: Given/When/Then (BDD style for behavior), checklist format (for multiple conditions), edge cases (error handling, boundary conditions), performance criteria (response time, throughput), security criteria (authentication, authorization), accessibility criteria (WCAG compliance).

Apply mandatory patterns: INVEST compliance check, clear acceptance criteria (≥3 criteria), business value articulation, story point estimation, subtask breakdown for >5 point stories, dependency identification, component/label tagging.

### 6. Add Recommendations

Include suggestions for: epic linkage, sprint assignment, priority setting, assignee recommendation, related stories, testing strategy.

### 7. Validate and Report


Generate optional Jira API payload for story creation. Report completion with story summary, acceptance criteria count, story points, next steps.

## Error Handling

**Hard-Stop Violations**: Explain violation (e.g., missing acceptance criteria), suggest compliant alternative with Given/When/Then examples.

**Incomplete Input**: List missing information (persona, goal, benefit, requirements), provide well-formed example.

**Environment Failure**: Report missing Jira configuration, suggest setup steps.

## Examples

**Data Pipeline Story**: `/story-create Create automated customer data pipeline: ingest from S3, transform with Spark, load to Snowflake, for data engineering team`
Output: User story with title, As a/I want/So that format, 5 acceptance criteria, 8 subtasks, 8 story points, technical notes.

**API Feature**: `/story-create Add customer search API endpoint with pagination and filtering, for mobile app team`
Output: User story with API specs, acceptance criteria for pagination/filtering/errors, 5 story points, API contract subtask.

**Dashboard Feature**: `/story-create Build executive dashboard showing KPIs with drill-down capability, for business users`
Output: User story with KPI list, acceptance criteria for visualizations/interactions, 13 story points, UI/backend subtasks.

## References

