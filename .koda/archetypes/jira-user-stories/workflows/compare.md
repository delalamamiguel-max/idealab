---
description: Compare user story formats and requirement approaches (Jira User Stories)
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
Extract from $ARGUMENTS: requirement problem, comparison criteria (clarity, completeness, testability), team context, constraints. Request clarification if incomplete.

### 4. Generate Alternatives

Create 2-3 story approaches: User story format (As a/I want/So that), Job story format (When/I want to/So I can), Use case format (detailed scenarios). Each with examples, use cases, pros/cons.

### 5. Generate Comparison Matrix

Compare on: clarity, completeness, testability, stakeholder understanding, development guidance, flexibility. Provide scores and analysis.

### 6. Add Recommendations

Recommend approach with justification. Include template guidance, team training needs, tool integration, refinement process.

### 7. Validate and Report


## Error Handling

**Insufficient Context**: Request team size, project type, stakeholder involvement.

**Format Confusion**: Explain key differences with concrete examples.

**Adoption Concerns**: Address change management and training needs.

## Examples

**Example 1**: `/compare-stories Compare user story vs job story format` - Output: Format comparison with clarity analysis

**Example 2**: `/compare-stories Epic vs feature vs story granularity` - Output: Hierarchy comparison with planning implications

**Example 3**: `/compare-stories Compare acceptance criteria formats (Given/When/Then vs checklist)` - Output: Format comparison with testability analysis

## References

