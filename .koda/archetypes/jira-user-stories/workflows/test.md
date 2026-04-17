---
description: Generate acceptance test scenarios for Jira user stories (Jira User Stories)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype jira-user-stories --json ` and parse for JIRA_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/jira-user-stories/templates/env-config.yaml` for test configuration

### 3. Parse Input
Extract from $ARGUMENTS: story ID or text, testing framework (Cucumber, pytest-bdd), coverage goals (acceptance criteria, edge cases), test scenarios. Request clarification if incomplete.

### 4. Analyze Code

Identify testable components: user story acceptance criteria, definition of done, edge cases and exceptions, integration points. Determine test scenarios: acceptance tests (Given/When/Then), positive scenarios, negative scenarios, edge cases, integration scenarios. Report test coverage plan.

### 5. Generate Test Suite

Create acceptance test suite with Gherkin scenarios (Given/When/Then), positive test cases, negative test cases, edge case scenarios, integration tests. Include complete test scenarios in BDD format.

### 6. Add Recommendations

Include recommendations for test execution (manual vs automated, test environments), CI/CD integration (run acceptance tests on deploy), coverage improvements (add more edge cases, test all criteria), collaboration (review with stakeholders). Provide summary.

### 7. Validate and Report


## Error Handling

**Insufficient Story Info**: Request complete story with acceptance criteria.

**No Acceptance Criteria**: Suggest creating criteria first.

**Ambiguous Scenarios**: Request clarification from stakeholders.

## Examples

**Example 1**: `/test-stories Generate acceptance tests for PROJ-123` - Output: 8 Gherkin scenarios covering all criteria

**Example 2**: `/test-stories Create edge case tests for PROJ-456` - Output: Negative and boundary scenarios

**Example 3**: `/test-stories Add integration tests for PROJ-789` - Output: End-to-end user journey tests

## References

