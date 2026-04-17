---
description: Generate a complete new archetype with all required files (Archetype Architect)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Parse Archetype Requirements

Extract from $ARGUMENTS:
- **Archetype name** (display name)
- **Category** (existing or new)
- **Purpose** (what problem it solves)
- **Technologies** (tools, languages, frameworks)
- **Common use cases** (3-5 examples)
- **Anti-patterns** (what to prevent)
- **Best practices** (what to enforce)

If incomplete, request clarification with template:
```
Please provide:
1. Archetype Display Name: (e.g., "Kubernetes Operator Builder")
2. Category: (01-11 or "new")
3. Purpose: (One sentence describing what it does)
4. Technologies: (e.g., Python, Kubernetes, Helm)
5. Use Cases: (3-5 common scenarios)
6. Anti-patterns: (What mistakes to prevent)
7. Best Practices: (What patterns to enforce)
```

### 1.5 Analyze Requirements and Provide Recommendations (CRITICAL ENHANCEMENT)

**Purpose:** Collaborate with user to design better archetype upfront. Investment: 15-20 minutes now saves hours later.

**Philosophy:** High user involvement during creation → Minimal user involvement during use

#### Review and Recommend:

**1. Category Placement Analysis**

Analyze technologies and use cases to recommend best category:

```
CATEGORY RECOMMENDATION

Analyzing: {archetype-name}
Technologies: {tech_list}
Use Cases: {use_case_summary}

Recommended Category: {category_number}-{category_name}

Rationale:
- {reason_1}
- {reason_2}
- {reason_3}

Alternative: {alternative_category} if {condition}

Proceed with {recommended_category}? [Y/n/specify]
```

**2. Identify Logical Pitfalls**

Review anti-patterns for completeness and suggest additions:

```
ANTI-PATTERN ANALYSIS

Provided Anti-Patterns:
✓ {anti_pattern_1}
✓ {anti_pattern_2}

Additional Anti-Patterns Identified:
⚠️ {additional_anti_pattern_1}
   Why: {explanation}
   Impact: {impact}
   
⚠️ {additional_anti_pattern_2}
   Why: {explanation}
   Impact: {impact}

Example for Kubernetes Operators:
⚠️ Hard-coded namespaces
   Why: Breaks multi-tenancy
   Impact: Operators can't be deployed to different namespaces
   
⚠️ Missing RBAC definitions
   Why: Security requirement
   Impact: Operators may fail with permission errors

Add these to anti-patterns? [Y/n/modify]
```

**3. Recommend Hard-Stop Rules**

Based on domain anti-patterns and security requirements:

```
HARD-STOP RULES RECOMMENDATION

Based on anti-patterns, recommend these hard-stop rules:

✘ {hard_stop_1}
   Rationale: {explanation}
   Severity: CRITICAL
   
✘ {hard_stop_2}
   Rationale: {explanation}
   Severity: HIGH

Example for Kubernetes Operators:
✘ No operators without health checks
   Rationale: Critical for production readiness
   Severity: CRITICAL
   
✘ No hard-coded namespaces
   Rationale: Breaks multi-tenancy
   Severity: HIGH
   
✘ No missing RBAC definitions
   Rationale: Security requirement
   Severity: CRITICAL

Approve these hard-stop rules? [Y/n/modify]
```

**4. Suggest Mandatory Patterns**

For consistency, quality, and testing:

```
MANDATORY PATTERNS RECOMMENDATION

✔ {mandatory_pattern_1}
   Why: {explanation}
   Benefit: {benefit}
   
✔ {mandatory_pattern_2}
   Why: {explanation}
   Benefit: {benefit}

Example for Kubernetes Operators:
✔ Idempotent reconciliation
   Why: Prevents state drift
   Benefit: Operators can be safely re-run
   
✔ Structured logging
   Why: Enables debugging
   Benefit: Easy troubleshooting in production
   
✔ Proper error handling
   Why: Prevents crash loops
   Benefit: Graceful degradation

Approve these mandatory patterns? [Y/n/modify]
```

**5. Flag Areas Lacking Clarity**

Identify ambiguous requirements:

```
CLARIFICATION NEEDED

⚠️ Technology Version Requirements
   Question: Which {technology} versions should be supported?
   Options: {version_options}
   Recommendation: {recommended_version} because {reason}
   
⚠️ Framework Selection
   Question: Which {framework_type} framework?
   Options: {framework_options}
   Recommendation: {recommended_framework} because {reason}
   
⚠️ Deployment Strategy
   Question: How should {artifact} be deployed?
   Options: {deployment_options}
   Recommendation: {recommended_deployment} because {reason}

Example for Kubernetes Operators:
⚠️ Kubernetes Version Support
   Question: Which Kubernetes versions to support?
   Options: 1.25+, 1.28+, 1.30+
   Recommendation: 1.28+ (current stable, good feature set)
   
⚠️ Operator Framework
   Question: Which operator framework?
   Options: kopf, operator-sdk, kubebuilder
   Recommendation: kopf (Python-native, async support, simpler)
   
⚠️ Deployment Method
   Question: How to deploy operators?
   Options: Helm, kustomize, raw manifests
   Recommendation: Helm (templating, versioning, rollback)

Please clarify: [provide answers or accept recommendations]
```

**6. Present Comprehensive Recommendations**

```
═══════════════════════════════════════════════════════════════
ARCHETYPE DESIGN RECOMMENDATIONS
═══════════════════════════════════════════════════════════════

Archetype: {archetype-name}
Category: {recommended_category} ✓
Rationale: {category_rationale}

ANTI-PATTERNS (Enhanced)
─────────────────────────────────────────────────────
Original: {count}
Added: {count}
Total: {total_count}

{list_all_anti_patterns}

HARD-STOP RULES (Recommended)
─────────────────────────────────────────────────────
✘ {hard_stop_1} (CRITICAL)
✘ {hard_stop_2} (HIGH)
✘ {hard_stop_3} (HIGH)
{...}

MANDATORY PATTERNS (Recommended)
─────────────────────────────────────────────────────
✔ {mandatory_1}
✔ {mandatory_2}
✔ {mandatory_3}
{...}

CLARIFICATIONS NEEDED
─────────────────────────────────────────────────────
1. {clarification_1}: {recommendation}
2. {clarification_2}: {recommendation}
3. {clarification_3}: {recommendation}

DESIGN QUALITY SCORE
─────────────────────────────────────────────────────
Category Fit: ✓ Excellent
Anti-Pattern Coverage: ✓ Comprehensive
Hard-Stop Rules: ✓ Strong (CRITICAL + HIGH severity)
Mandatory Patterns: ✓ Well-defined
Clarity: ⚠️ Needs {n} clarifications

NEXT STEPS
─────────────────────────────────────────────────────
1. Review and approve recommendations
2. Provide clarifications for {n} questions
3. Proceed with archetype generation

═══════════════════════════════════════════════════════════════

Proceed with these recommendations? [Y/n/modify]
```

**7. Iterate Based on User Feedback**

If user requests modifications:
- Adjust recommendations
- Re-present for approval
- Continue until user approves

**Benefits of Collaborative Design:**
- ✅ Catches design issues early
- ✅ Ensures comprehensive coverage
- ✅ Reduces rework later
- ✅ Creates better archetypes that work autonomously
- ✅ Investment: 15-20 min now → Saves hours later

### 2. Generate Archetype Slug

Convert display name to kebab-case slug:
- "Kubernetes Operator Builder" → "kubernetes-operator-builder"
- "React Component Library" → "react-component-library"

### 3. Determine Category Path

If existing category (01-11):
- Use existing category folder
- Add to existing manifest.yaml

If new category:
- Create new category folder: `{number}-{category-name}/`
- Create new manifest.yaml
- Create new INDEX.md

### 4. Generate Constitution File

Create `${ARCHETYPES_BASEDIR}/archetype-architect/{archetype-slug}-constitution.md`:

```markdown
# {Archetype Display Name} Constitution

## Purpose

Define foundational principles and hard-stop rules for {archetype-slug}.

**Domain:** {Technologies}
**Use Cases:** {Common use cases}

## I. Hard-Stop Rules (Non-Negotiable)

The LLM **must refuse** or correct any code that violates:

{Generate 5-7 hard-stop rules based on anti-patterns}
- ✘ **No {security-issue}**: {Explanation}
- ✘ **No {performance-issue}**: {Explanation}
- ✘ **No {compliance-issue}**: {Explanation}

## II. Mandatory Patterns (Must Apply)

The LLM **must insert** or verify:

{Generate 7-10 mandatory patterns based on best practices}
- ✔ **{Pattern name}**: {Description}
- ✔ **{Naming convention}**: {Description}
- ✔ **{Testing requirement}**: {Description}

## III. Preferred Patterns (Recommended)

The LLM **should adopt** unless user overrides:

{Generate 3-5 preferred patterns}
- ➜ **{Optimization}**: {Description}
- ➜ **{Best practice}**: {Description}

---
**Version**: 1.0.0
**Last Updated**: {Current Date}
**Source**: Generated by Archetype Builder
```

### 5. Generate Environment Config

Create `${ARCHETYPES_BASEDIR}/archetype-architect/templates/env-config.yaml`:

```yaml
# Environment Configuration for {Archetype Display Name}
# Generated: {Current Date}

# Tool Configuration
{primary_tool}:
  version: "{recommended_version}"
  {tool_specific_settings}

# Performance Targets
performance:
  expected_runtime_secs: 10
  max_runtime_secs: 300
  max_cost_usd: 5.0

# Variables (replaced in generated code)
variables:
  # Common parameters
  project_name: "my_project"
  environment: "dev"
  
  # Tool-specific variables
  {generate_tool_specific_vars}

# Validation Rules
validation:
  required_env_vars:
    {generate_required_env_vars}
  
  optional_env_vars:
    {generate_optional_env_vars}
  
  pre_execution_checks:
    - check: "{tool}_installed"
      description: "Verify {tool} is installed"
    - check: "connection_valid"
      description: "Verify connectivity"

# Code Quality Standards
quality:
  max_file_lines: 500
  require_comments: true
  require_tests: true
  test_coverage_threshold: 80
```

### 5.5 Generate Supporting Assets via Orchestration (CRITICAL ENHANCEMENT)

**Purpose:** Delegate sub-tasks to specialized archetypes for consistency, quality, and code reuse.

For each asset type needed by target archetype:

#### A. Validation Scripts (if archetype needs validation)

Identify if archetype requires validation scripts based on domain:
- Code generators: Yes (syntax, linting, compilation)
- Infrastructure: Yes (config validation, connectivity)
- Data engineering: Yes (schema validation, data quality)
- Documentation: Optional (link checking, spell checking)

If validation needed:

```bash
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
  --input "Create bash validation script for {domain}" \
  --json
```

Parse JSON response:
```json
{
  "primary_match": {
    "archetype": "automation-scripter",
    "archetype_display_name": "Automation Scripter",
    "category": "05-infrastructure-devops",
    "confidence": 0.95,
    "workflows": {
      "scaffold": "/scaffold-automation"
    }
  }
}
```

**Confidence-Based Routing:**

**If confidence ≥ 0.80 (Auto-route):**
```
✓ Detected: Automation Scripter (confidence: 95%)
  Routing to: /scaffold-automation
  Purpose: Generate validation script

Execute:
/scaffold-automation "Create bash script to validate {specific_requirement}
for {archetype-slug}. Script should check:
- {validation_point_1}
- {validation_point_2}
- {validation_point_3}
Output: JSON format with pass/fail status"

Output location: ${ARCHETYPES_BASEDIR}/{archetype-slug}/scripts/validate-{archetype-slug}.sh

Reference in target archetype workflows:
### 6. Validate Output
Run `${ARCHETYPES_BASEDIR}/scripts/bash/validate-{archetype-slug}.sh --file {output} --json`
```

**If confidence 0.50-0.79 (Ask user confirmation):**
```
🤔 Detected: Automation Scripter (confidence: 65%)
   Alternative: Python script generator (55%)
   
   Proceed with Automation Scripter for bash validation script? [Y/n]
   Or specify: /scaffold-{archetype-slug}
```

**If confidence < 0.50 (Generate manually):**
```
⚠️  Low confidence for sub-task detection
    Generating validation script manually within archetype-architect
    (No specialized archetype delegation)
    
Note: Consider creating automation-scripter if not available
```

#### B. Documentation (if archetype needs comprehensive docs)

```bash
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
  --input "Generate comprehensive documentation" \
  --json
```

**If confidence ≥ 0.75:**
```
✓ Detected: Documentation Evangelist (confidence: 88%)
  Routing to: /document-documentation

Execute:
/document-documentation "Create usage guide for {archetype-name}
Include:
- Purpose and overview
- Workflow examples (scaffold, debug, refactor)
- Constitutional rules summary
- Integration points with other archetypes
- Common use cases
- Troubleshooting guide"

Output: .windsurf/workflows/{category}/{archetype-slug}/README.md
```

#### C. Test Harnesses (if archetype needs test scripts)

```bash
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
  --input "Create unit tests for validation" \
  --json
```

**If confidence ≥ 0.80:**
```
✓ Detected: Unit Test Code Coverage (confidence: 85%)
  Routing to: /scaffold-unit-test-code-coverage

Execute:
/scaffold-unit-test-code-coverage "Create pytest validation for {archetype-slug}
Test:
- File structure validation
- Constitution quality checks
- Discovery performance
- Workflow syntax validation"

Output: ${ARCHETYPES_BASEDIR}/{archetype-slug}/scripts/test_{archetype-slug}.py

Reference in test-{archetype-slug} workflow:
### 9. Run Automated Tests
pytest ${ARCHETYPES_BASEDIR}/{archetype-slug}/scripts/test_{archetype-slug}.py -v
```

#### D. Configuration Templates (if archetype needs YAML/JSON configs)

Identify config type based on archetype domain:
- Infrastructure → terraform-cicd-architect
- Application → app-maker
- Pipeline → pipeline-orchestrator
- Data → data-engineering archetypes

```bash
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
  --input "Create {config_type} configuration template" \
  --json
```

**If confident match found:**
```
Route to appropriate archetype
Generate config templates
Integrate into target archetype's env-config.yaml or templates/
```

#### Orchestration Decision Matrix

| Sub-Task | Primary Archetype | Confidence Threshold | Auto-Route |
|----------|-------------------|----------------------|------------|
| Bash/PowerShell script | automation-scripter | 0.80 | Yes |
| Python utility script | automation-scripter | 0.80 | Yes |
| Markdown documentation | documentation-evangelist | 0.75 | Yes |
| Unit tests | unit-test-code-coverage | 0.80 | Yes |
| CI/CD pipeline | microservice-cicd-architect | 0.80 | Yes |
| Terraform IaC | terraform-cicd-architect | 0.85 | Yes |
| Data quality checks | quality-guardian | 0.80 | Yes |
| SQL queries | sql-query-crafter | 0.85 | Yes |
| PySpark transforms | transformation-alchemist | 0.85 | Yes |
| API endpoints | integration-specialist | 0.80 | Yes |
| PowerPoint | ppt-maker | 0.90 | Confirm |
| Observability | observability | 0.85 | Yes |
| User stories | jira-user-stories | 0.85 | Yes |
| Implementation plans | documentation-evangelist | 0.80 | Yes |
| Regression tests | regression-test-coverage | 0.85 | Yes |

#### E. User Stories (if archetype is part of a project)

When archetype creation is part of a larger project initiative:

```
/scaffold-jira-user-stories "
Create user stories for {archetype-name} archetype implementation:

Epic: Implement {archetype-display-name} Archetype

Stories:
1. Constitution Development - Define hard-stop rules and mandatory patterns
2. Workflow Implementation - Create 6 standard workflows
3. Script Development - Create validation and utility scripts  
4. Test Suite - Create comprehensive test coverage
5. Documentation - Create README and usage guides
6. Integration Testing - Validate ecosystem integration

Acceptance Criteria for each story should reference:
- Constitution compliance
- Workflow consistency with archetype standards
- Script quality (via automation-scripter patterns)
- Test coverage thresholds
"
```

#### F. Implementation Plan (for complex archetypes)

For archetypes with significant scope:

```
/solution-document "
Create implementation plan for {archetype-name} archetype:

SECTIONS:
1. Overview and Objectives
2. Technical Design
3. Phased Delivery Plan
4. Dependencies and Integration Points
5. Testing Strategy
6. Rollout Plan

OUTPUT: {archetype-slug}/docs/implementation-plan.md
"
```

#### G. Comprehensive Test Suite

Archetypes require multiple layers of testing:

**1. Script Tests (if archetype has scripts):**
```
/scaffold-unit-test-code-coverage "
Create pytest suite for {archetype-slug} scripts:
- Test each script function
- Test error handling
- Test edge cases
- Coverage target: 80%

Output: {archetype-slug}/tests/test_scripts.py
"
```

**2. Workflow Validation Tests:**
```
/scaffold-regression-test-coverage "
Create workflow validation tests for {archetype-slug}:
- Validate workflow file syntax
- Validate constitution references
- Validate ARCHETYPES_BASEDIR usage
- Test discover-archetype.py routing accuracy

Output: {archetype-slug}/tests/test_workflows.py
"
```

**3. Integration Tests:**
```
/solution-test "
Create integration test suite for {archetype-slug}:
- Test workflow execution paths
- Test ecosystem delegation
- Test error handling flows
- Validate outputs match constitution

Output: {archetype-slug}/tests/test_integration.py
"
```

### 5.6 Archetype Architect's Core Responsibility (CRITICAL)

**What archetype-architect OWNS (Structural & Logical Quality):**

| Responsibility | Description |
|----------------|-------------|
| **Manifest Structure** | Correct schema, required fields, proper keywords |
| **Constitution Quality** | Well-defined hard-stops, mandatory patterns, clear rules |
| **Workflow Consistency** | All 6 workflows follow standard structure |
| **File Organization** | Correct directory structure, naming conventions |
| **Cross-References** | Proper paths, ARCHETYPES_BASEDIR usage |
| **Ecosystem Integration** | Proper delegation language, routing hints |
| **Naming Consistency** | Slug matches across all files |
| **Dependency Declarations** | Accurate constitution.path, dependencies list |

**What archetype-architect DELEGATES (Content Quality):**

| Content Type | Delegate To | Why |
|--------------|-------------|-----|
| Scripts (bash/python) | automation-scripter | Script expertise, patterns |
| Documentation prose | documentation-evangelist | Writing quality, structure |
| Test suites | unit-test-code-coverage | Testing expertise |
| Regression tests | regression-test-coverage | Coverage analysis |
| User stories | jira-user-stories | Story format, acceptance criteria |
| CI/CD pipelines | microservice-cicd-architect | Pipeline patterns |
| Data validation | quality-guardian | Data quality rules |

**Delegation Pattern:**
```
archetype-architect says:
  "I need a validation script for this archetype"
  → Delegates to automation-scripter
  → automation-scripter creates high-quality script
  → archetype-architect integrates script into archetype structure
  → archetype-architect validates script reference in workflows
```

#### Benefits of Orchestration

✅ **Code Reuse:** Don't reinvent script generation—use automation-scripter  
✅ **Consistency:** Scripts follow automation-scripter patterns across all archetypes  
✅ **Best Practices:** Leverage domain expertise embedded in specialized archetypes  
✅ **Maintainability:** Updates to automation-scripter benefit all archetypes  
✅ **Discovery Testing:** Validates that archetype metadata is accurate  
✅ **Meta-Learning:** archetype-architect learns which archetypes work together  

#### Example: Complete Orchestration Flow

```
Creating "Kafka Stream Processor" archetype:

1. Needs bash validation script
   → discover-archetype.py "bash script validate Kafka stream"
   → Detected: automation-scripter (95%)
   → /scaffold-automation "Create bash validation for Kafka offset management..."
   → Output: ${ARCHETYPES_BASEDIR}/scripts/bash/validate-kafka-stream.sh
   → Referenced in workflow with // turbo

2. Needs Python monitoring script
   → discover-archetype.py "python monitoring script Kafka metrics"
   → Detected: automation-scripter (92%)
   → /scaffold-automation "Create python monitoring for Kafka consumer lag..."
   → Output: ${ARCHETYPES_BASEDIR}/scripts/python/monitor-kafka-metrics.py

3. Needs configuration template
   → discover-archetype.py "YAML configuration Kafka consumer"
   → Detected: pipeline-orchestrator (70% - requires confirmation)
   → User confirms
   → /scaffold-pipeline "Config template for Kafka consumer with schema registry"
   → Output: ${ARCHETYPES_BASEDIR}/archetype-architect/templates/kafka-config.yaml

4. Needs comprehensive documentation
   → discover-archetype.py "comprehensive documentation"
   → Detected: documentation-evangelist (88%)
   → /document-documentation "Kafka Stream Processor archetype usage guide"
   → Output: README.md with usage examples

Result: All supporting assets generated by specialized archetypes
        Target archetype workflows reference these assets
        Consistent quality across all generated artifacts
```

### 6. Generate Six Workflow Files

For each workflow type (scaffold, debug, refactor, test, compare, document):

Create `.windsurf/workflows/{category}/{archetype-slug}/{action}-{archetype-slug}.md`:

#### scaffold-{archetype-slug}.md
```markdown
---
description: Generate {artifact} for {Archetype Display Name}
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run cross-platform validation:
```python
# Use Python wrapper for cross-platform compatibility
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype {archetype_slug}
```

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/archetype-architect/templates/env-config.yaml`

### 3. Parse Input
Extract from $ARGUMENTS: {specific_requirements}

### 4. Validate Constraints
Check against hard-stop rules from constitution

### 5. Generate {Artifact}
{Specific generation logic based on archetype purpose}

**Note:** Use `pathlib.Path` or `os.path.join()` for all file paths to ensure cross-platform compatibility.

### 6. Validate and Report
Run cross-platform validation:
```python
# Use Python wrapper for cross-platform compatibility
```

## Error Handling

**Hard-Stop Violations**: Explain violation, suggest compliant alternative

**Incomplete Input**: List missing information, provide example

**Environment Failure**: Report missing configuration

## Examples

{Generate 3 concrete examples based on use cases}

## References

Constitution: (pre-loaded above)
```

#### debug-{archetype-slug}.md
```markdown
---
description: Debug {artifact} errors for {Archetype Display Name}
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Error Context
Extract from $ARGUMENTS:
- Error message or symptom
- File path (if applicable)
- Recent changes

### 2. Load Configuration
- Read constitution for common pitfalls
- Load env-config for validation rules

### 3. Analyze Error Pattern
Match against known error patterns:
{Generate common error patterns for this archetype}

### 4. Diagnose Root Cause
{Diagnostic steps specific to archetype}

### 5. Suggest Fix
Provide step-by-step remediation

### 6. Validate Fix
Verify fix complies with constitution

## Common Issues

{Generate 5-7 common issues and fixes}

## References

Constitution: (pre-loaded above)
```

#### refactor-{archetype-slug}.md
```markdown
---
description: Refactor {artifact} to apply best practices for {Archetype Display Name}
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Analyze Current Code
Load and parse existing code

### 2. Identify Improvements
Check against:
- Hard-stop violations
- Missing mandatory patterns
- Opportunities for preferred patterns

### 3. Generate Refactoring Plan
Prioritize improvements:
1. Fix hard-stop violations (critical)
2. Apply mandatory patterns (required)
3. Suggest preferred patterns (optional)

### 4. Apply Refactorings
{Specific refactoring logic}

### 5. Validate Changes
Ensure no regressions

## Refactoring Patterns

{Generate 5-7 common refactoring patterns}

## References

Constitution: (pre-loaded above)
```

#### test-{archetype-slug}.md
```markdown
---
description: Generate test harness for {Archetype Display Name}
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Analyze Code Under Test
Parse code structure and identify testable units

### 2. Load Test Requirements
From env-config: coverage threshold, test framework

### 3. Generate Test Scaffold
{Test generation logic specific to archetype}

### 4. Add Test Cases
- Happy path
- Edge cases
- Error conditions
- Boundary conditions

### 5. Validate Test Coverage
Ensure meets threshold from env-config

## Test Patterns

{Generate test patterns for this archetype}

## References

Constitution: (pre-loaded above)
```

#### compare-{archetype-slug}.md
```markdown
---
description: Compare approaches for {Archetype Display Name}
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Parse Comparison Request
Extract approaches to compare

### 2. Define Comparison Criteria
- Performance
- Maintainability
- Compliance with constitution
- Cost
- Complexity

### 3. Analyze Each Approach
{Comparison logic specific to archetype}

### 4. Generate Comparison Matrix
Present trade-offs in table format

### 5. Recommend Approach
Based on criteria and use case

## Comparison Dimensions

{Generate comparison dimensions for this archetype}

## References

Constitution: (pre-loaded above)
```

#### document-{archetype-slug}.md
```markdown
---
description: Generate documentation for {Archetype Display Name}
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Analyze Code
Parse code structure and extract documentation targets

### 2. Generate Documentation Structure
- Overview
- Architecture
- Usage examples
- API reference (if applicable)
- Configuration
- Troubleshooting

### 3. Add Code Examples
Extract or generate illustrative examples

### 4. Validate Documentation
- Check for completeness
- Verify examples are runnable
- Ensure constitution compliance is documented

## Documentation Patterns

{Generate documentation patterns for this archetype}

## References

Constitution: (pre-loaded above)
```

### 7. Generate Manifest File

Create `${ARCHETYPES_BASEDIR}/{archetype-slug}/manifest.yaml`:

```yaml
archetype:
  name: {archetype-slug}
  display_name: "{Archetype Display Name}"
  description: |
    {Purpose - detailed description of what this archetype does and when to use it}
  keywords:
    - {primary_keyword_1}
    - {primary_keyword_2}
    - {technology_1}
    - {technology_2}
    - {use_case_keyword}
  constitution:
    path: {archetype-slug}-constitution.md
  dependencies: []
  workflows:
    scaffold: scaffold-{archetype-slug}
    refactor: refactor-{archetype-slug}
    compare: compare-{archetype-slug}
    test: test-{archetype-slug}
    debug: debug-{archetype-slug}
    document: document-{archetype-slug}
# NOTE: No version field - version tracking belongs in changelog.md
```

### 7.5 Generate Changelog File

Create `${ARCHETYPES_BASEDIR}/{archetype-slug}/changelog.md`:

```markdown
# {Archetype Display Name} - Changelog

All notable changes to this archetype are documented in this file.

## [Unreleased]

### Added
- Initial archetype creation
- Constitution with hard-stop rules and mandatory patterns
- All 6 workflow files (scaffold, refactor, compare, test, debug, document)
- README.md with usage documentation

---

## Template for Future Entries

## [YYYY-MM-DD]

### Added
- New features

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes
```

### 7.6 Generate README File

Create `${ARCHETYPES_BASEDIR}/{archetype-slug}/README.md`:

```markdown
# {Archetype Display Name}

## Overview

{Purpose - brief description of what this archetype does}

## When to Use

- {Use case 1}
- {Use case 2}
- {Use case 3}

## Quick Start

\`\`\`bash
# Scaffold a new {domain} solution
/scaffold-{archetype-slug} "{example arguments}"
\`\`\`

## Workflows

| Workflow | Purpose |
|----------|---------|
| \`/scaffold-{archetype-slug}\` | Create new {domain} solutions |
| \`/refactor-{archetype-slug}\` | Improve existing {domain} code |
| \`/compare-{archetype-slug}\` | Evaluate {domain} design options |
| \`/test-{archetype-slug}\` | Validate {domain} implementations |
| \`/debug-{archetype-slug}\` | Diagnose {domain} issues |
| \`/document-{archetype-slug}\` | Generate {domain} documentation |

## Related Archetypes

- {Related archetype 1} - {Relationship description}
- {Related archetype 2} - {Relationship description}

## References

- [Constitution](./{archetype-slug}-constitution.md)
- [Changelog](./changelog.md)
```

### 8. Update Index Files

#### Update Category INDEX.md

Add entry:
```markdown
### {archetype-slug}

**Available Workflows:**
- `compare-{archetype-slug}.md`
- `debug-{archetype-slug}.md`
- `document-{archetype-slug}.md`
- `refactor-{archetype-slug}.md`
- `scaffold-{archetype-slug}.md`
- `test-{archetype-slug}.md`

**Description:** {Purpose}

**When to Use:** {Use cases summary}

---
```

#### Update Main Workflows INDEX.md

Add to appropriate category section

#### Update Constitution INDEX.md

Add to `${ARCHETYPES_BASEDIR}/memory/archetypes/INDEX.md`

#### Update Templates INDEX.md

Add to `${ARCHETYPES_BASEDIR}/templates/INDEX.md`

### 9. Test Discovery

Run discovery test:
```bash
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
  --input "{test query based on primary keywords}"
```

Verify archetype is detected with high confidence.

### 10. Generate Summary Report

```
✅ Archetype Created: {Archetype Display Name}

📁 Files Created:
- Constitution: ${ARCHETYPES_BASEDIR}/archetype-architect/{archetype-slug}-constitution.md
- Env Config: ${ARCHETYPES_BASEDIR}/archetype-architect/templates/env-config.yaml
- Workflows (6):
  • .windsurf/workflows/{category}/{archetype-slug}/scaffold-{archetype-slug}.md
  • .windsurf/workflows/{category}/{archetype-slug}/debug-{archetype-slug}.md
  • .windsurf/workflows/{category}/{archetype-slug}/refactor-{archetype-slug}.md
  • .windsurf/workflows/{category}/{archetype-slug}/test-{archetype-slug}.md
  • .windsurf/workflows/{category}/{archetype-slug}/compare-{archetype-slug}.md
  • .windsurf/workflows/{category}/{archetype-slug}/document-{archetype-slug}.md

📝 Metadata Updated:
- manifest.yaml
- Category INDEX.md
- Main workflows INDEX.md
- Constitution INDEX.md
- Templates INDEX.md

🧪 Discovery Test:
- Test Query: "{test_query}"
- Confidence: {confidence}%
- Status: {pass/fail}

📚 Next Steps:
1. Review generated constitution rules
2. Customize env-config variables
3. Add specific examples to workflows
4. Test with real use cases
5. Update README with archetype documentation

🔗 Quick Test:
/{workflow-type}-{archetype-slug} "Your test request"
```

## Error Handling

**Incomplete Requirements**:
```
⚠️ Missing Required Information

Please provide:
{list_missing_fields}

Example:
/scaffold-archetype-architect "
Archetype: Kubernetes Operator Builder
Category: 05-infrastructure-devops
Purpose: Generate production-ready Kubernetes operators
Technologies: Python, Kubernetes, Helm, kopf
Use Cases: CRD management, controller logic, reconciliation loops
Anti-patterns: Hard-coded namespaces, missing RBAC, no health checks
Best Practices: Operator SDK patterns, idempotent reconciliation, proper logging
"
```

**Category Conflict**:
```
⚠️ Category Decision Required

Category "05-infrastructure-devops" already has 8 archetypes.
Options:
1. Add to existing category (recommended if related)
2. Create new category: "12-{new-category-name}"

Which option? [1/2]
```

**Slug Conflict**:
```
❌ Archetype slug "{slug}" already exists in category {category}

Suggestions:
- Use more specific name: "{alternative-slug-1}"
- Add qualifier: "{alternative-slug-2}"
- Choose different category

Please provide alternative name.
```

## Examples

### Example 1: Infrastructure Archetype
```
/scaffold-archetype-architect "
Archetype: Kubernetes Operator Builder
Category: 05-infrastructure-devops
Purpose: Generate production-ready Kubernetes operators with reconciliation loops
Technologies: Python, Kubernetes, kopf, Helm
Use Cases: 
  - CRD management
  - Custom controller logic
  - Reconciliation loops
  - Operator deployment
Anti-patterns:
  - Hard-coded namespaces
  - Missing RBAC definitions
  - No health checks
  - Synchronous operations
Best Practices:
  - Idempotent reconciliation
  - Proper error handling
  - Structured logging
  - Operator SDK patterns
"
```

### Example 2: Data Science Archetype
```
/scaffold-archetype-architect "
Archetype: AutoML Pipeline Builder
Category: 01-machine-learning-models
Purpose: Generate automated machine learning pipelines with hyperparameter tuning
Technologies: Python, scikit-learn, optuna, MLflow
Use Cases:
  - Automated feature selection
  - Hyperparameter optimization
  - Model comparison
  - Pipeline deployment
Anti-patterns:
  - Data leakage in cross-validation
  - No experiment tracking
  - Hard-coded hyperparameters
Best Practices:
  - MLflow experiment tracking
  - Proper train/test splits
  - Reproducible random seeds
  - Pipeline versioning
"
```

### Example 3: Documentation Archetype
```
/scaffold-archetype-architect "
Archetype: API Documentation Generator
Category: 09-documentation-requirements
Purpose: Generate comprehensive API documentation from code
Technologies: Python, OpenAPI, Swagger, Markdown
Use Cases:
  - REST API documentation
  - GraphQL schema docs
  - SDK documentation
  - Interactive API explorers
Anti-patterns:
  - Outdated examples
  - Missing authentication docs
  - No error code documentation
Best Practices:
  - Auto-generated from code
  - Interactive examples
  - Version-specific docs
  - Authentication flows
"
```

## References

- **System Quick Start**: ../QUICK_START.md
- **Existing Archetypes**: Browse .windsurf/workflows/ for examples
- **Constitution Examples**: See ${ARCHETYPES_BASEDIR}/memory/archetypes/
- **Discovery Script**: ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py
