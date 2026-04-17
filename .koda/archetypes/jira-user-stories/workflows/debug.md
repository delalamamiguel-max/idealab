---
description: Debug issues with Jira user stories and acceptance criteria (Jira User Stories)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype jira-user-stories --json ` and parse for JIRA_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/jira-user-stories/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: story ID or text, issue description (unclear requirements, missing acceptance criteria, blocked story), symptoms (team confusion, implementation delays, failed acceptance), context. Request clarification if incomplete.

### 4. Analyze Problem

Identify issue category: clarity issues (vague story, unclear requirements, ambiguous acceptance criteria), completeness issues (missing information, no definition of done, missing dependencies), estimation issues (story too large, unclear scope), acceptance issues (criteria not testable, missing edge cases). Analyze story text, acceptance criteria, and team feedback. Report findings with specific issues and impact.

### 5. Generate Fix

Create improved story addressing issues: clarify requirements (specific persona, clear action, measurable outcome), complete acceptance criteria (Given/When/Then, positive and negative cases, edge cases), add missing information (technical notes, dependencies, risks), break down large stories (create subtasks, define dependencies). Include complete improved story with all required elements.

### 6. Add Recommendations

Include recommendations for prevention (story templates, review process, team training), testing (acceptance test scenarios, edge case identification), collaboration (stakeholder review, team refinement). Provide summary with improvements made and clarity enhancements.

### 7. Validate and Report


## Error Handling

**Insufficient Story Information**: Request complete story text, context, and stakeholder input.

**Conflicting Requirements**: Facilitate clarification with stakeholders.

**Scope Creep**: Identify core vs additional requirements, suggest story splitting.

## Examples

**Example 1: Vague Requirements**
```
/debug-stories Team confused about PROJ-123 requirements

Issue: Story says "improve reports" without specifics
Fix: Clarified specific report, metrics, and user persona
Result: Team can now implement with confidence
```

**Example 2: Missing Acceptance Criteria**
```
/debug-stories PROJ-456 failed acceptance testing

Issue: No acceptance criteria defined, expectations unclear
Fix: Added comprehensive Given/When/Then scenarios with edge cases
Result: Clear acceptance criteria for testing
```

**Example 3: Story Too Large**
```
/debug-stories PROJ-789 taking 3 sprints, blocking other work

Issue: 20-point story covering multiple features
Fix: Broke into 5 smaller stories with clear dependencies
Result: Incremental delivery, better planning
```

## References

