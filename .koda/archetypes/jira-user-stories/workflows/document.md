---
description: Generate documentation for user stories and requirements (Jira User Stories)
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
Extract from $ARGUMENTS: story/epic to document, target audience (stakeholders, developers, testers), documentation scope (requirements doc, user guide, acceptance criteria). Request clarification if incomplete.

### 4. Analyze Code/System

Analyze story/epic: identify user personas and goals, document acceptance criteria, explain business value, note dependencies and constraints, identify edge cases, document testing scenarios.

### 5. Generate Documentation

Create comprehensive documentation with: feature overview and business context, user personas and journeys, detailed requirements, acceptance criteria, user guide with screenshots, testing scenarios, release notes.

Include requirements document, user guide, test scenarios, release notes.

### 6. Add Recommendations

Include recommendations for documentation maintenance, stakeholder communication, user training, feedback collection, continuous improvement.

### 7. Validate and Report


Generate documentation artifacts. Report completion.

## Error Handling

**Insufficient Context**: Request business context and user personas.

**Unclear Requirements**: Facilitate requirements gathering with stakeholders.

**Missing Acceptance Criteria**: Request testable acceptance criteria.

## Examples

**Example 1**: `/document-stories Create user guide for customer portal feature` - Output: User guide with screenshots, workflows, FAQs

**Example 2**: `/document-stories Generate requirements doc for PROJ-123` - Output: Requirements document with acceptance criteria, dependencies

**Example 3**: `/document-stories Document epic for stakeholders` - Output: Executive summary with business value, roadmap, success metrics

## References

