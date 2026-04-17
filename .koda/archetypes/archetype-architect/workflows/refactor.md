---
description: Refactor existing archetype to apply best practices (Archetype Architect)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Archetype to Refactor

Extract from $ARGUMENTS:
- Archetype slug
- What to improve (discovery, constitution, workflows, etc.)
- Specific issues or goals

### 2. Analyze Current Implementation (ENHANCED)

Load and review:
- Constitution rules
- Workflow files
- Metadata keywords
- Environment config
- Discovery performance

**NEW: Identify ALL Referenced Assets**

Parse all 6 workflow files for references to:
- **Bash scripts:** `${ARCHETYPES_BASEDIR}/scripts/bash/*.sh`
- **Python scripts:** `${ARCHETYPES_BASEDIR}/scripts/python/*.py`
- **Configuration files:** `${ARCHETYPES_BASEDIR}/archetype-architect/templates/*.yaml`
- **Documentation:** README.md, guides, examples
- **Test scripts:** pytest, unittest files
- **Validation scripts:** check-guardrails.sh, validate-env.sh

For each referenced asset:

#### 2.1 Check Asset Existence
```bash
# Example: Check if validation script exists
ls ${ARCHETYPES_BASEDIR}/scripts/bash/validate-{archetype-slug}.sh

# Check if config exists
ls ${ARCHETYPES_BASEDIR}/archetype-architect/templates/env-config.yaml
```

#### 2.2 Identify Asset Type
- Bash script (.sh)
- Python script (.py)
- YAML configuration (.yaml)
- Markdown documentation (.md)
- Test script (test_*.py, *_test.py)

#### 2.3 Determine Refactoring Need

For each asset, check:
- **Functionality:** Does it work correctly?
- **Best Practices:** Does it follow domain standards?
- **Maintainability:** Is code clear and documented?
- **Performance:** Any optimization opportunities?
- **Security:** Any vulnerabilities?

#### 2.4 Run Discovery for Asset Refactoring

For each asset needing refactoring:

```bash
python ${ARCHETYPES_BASEDIR}/scripts/python/discover-archetype.py \
  --input "refactor {asset_type} {asset_purpose}" \
  --json
```

**Example for bash script:**
```bash
# Found reference in scaffold-kafka-stream-processor.md:
# Run `${ARCHETYPES_BASEDIR}/scripts/bash/validate-kafka-stream.sh`

# Check asset exists
ls ${ARCHETYPES_BASEDIR}/scripts/bash/validate-kafka-stream.sh

# Identify type: bash script
# Run discovery
python ${ARCHETYPES_BASEDIR}/scripts/python/discover-archetype.py \
  --input "refactor bash validation script" \
  --json

# Response:
{
  "primary_match": {
    "archetype": "automation-scripter",
    "confidence": 0.92,
    "workflows": {
      "refactor": "/refactor-automation"
    }
  }
}

# If confidence ≥ 0.80:
# → Route to: /refactor-automation validate-kafka-stream.sh
# → Apply automation-scripter best practices
# → Update script in place
```

#### Asset Refactoring Matrix

| Asset Type | Archetype | Confidence Threshold | Action |
|------------|-----------|----------------------|--------|
| Bash script | automation-scripter | 0.80 | /refactor-automation {script_path} |
| Python script | automation-scripter | 0.80 | /refactor-automation {script_path} |
| YAML config | pipeline-orchestrator | 0.70 | /refactor-pipeline {config_path} |
| Markdown docs | documentation-evangelist | 0.75 | /refactor-documentation {doc_path} |
| Test scripts | unit-test-code-coverage | 0.80 | /refactor-unit-test-code-coverage {test_path} |
| SQL queries | sql-query-crafter | 0.85 | /refactor-sql {query_file} |
| Terraform | terraform-cicd-architect | 0.85 | /refactor-terraform {tf_file} |
| User stories | jira-user-stories | 0.85 | /refactor-jira-user-stories {story_file} |

### 2.5 Archetype Architect's Refactoring Responsibility (CRITICAL)

**What archetype-architect OWNS during refactoring:**

| Responsibility | Description |
|----------------|-------------|
| **Structural Consistency** | Manifest schema, file organization, naming conventions |
| **Constitution Integrity** | Hard-stop rules are well-formed, mandatory patterns are clear |
| **Workflow Structure** | All 6 workflows follow standard structure |
| **Cross-References** | All paths valid, ARCHETYPES_BASEDIR usage correct |
| **Ecosystem Integration** | Delegation language updated, routing hints accurate |
| **Dependency Accuracy** | constitution.path, dependencies list current |

**What archetype-architect DELEGATES during refactoring:**

| Refactoring Need | Delegate To | Delegation Command |
|------------------|-------------|-------------------|
| Script quality issues | automation-scripter | `/refactor-automation "{script_path}"` |
| Documentation prose | documentation-evangelist | `/refactor-documentation "{doc_path}"` |
| Test coverage gaps | unit-test-code-coverage | `/refactor-unit-test-code-coverage "{test_path}"` |
| Regression test issues | regression-test-coverage | `/refactor-regression-test-coverage "{test_path}"` |
| CI/CD pipeline issues | microservice-cicd-architect | `/refactor-microservice-cicd "{pipeline}"` |

**Refactoring Delegation Pattern:**
```
archetype-architect detects:
  "This archetype's validation script has poor error handling"
  → Delegates to: /refactor-automation "{script_path}" "Improve error handling, add logging"
  → automation-scripter refactors script with best practices
  → archetype-architect validates script still integrates correctly
  → archetype-architect updates any workflow references if needed
```

**When to Delegate vs Handle Directly:**

| Scenario | Action |
|----------|--------|
| Script has bugs or poor patterns | DELEGATE to automation-scripter |
| Documentation is unclear | DELEGATE to documentation-evangelist |
| Tests are missing or weak | DELEGATE to testing archetypes |
| Manifest has wrong schema | HANDLE directly (structural) |
| Constitution rules are incomplete | HANDLE directly (logical quality) |
| Workflow structure is non-standard | HANDLE directly (consistency) |
| Cross-references are broken | HANDLE directly (integration) |

#### 2.6 Check Cross-Archetype Integration

Verify integration with other archetypes:
- Check if archetype is referenced by other archetypes
- Verify orchestration calls work correctly
- Test discovery confidence for this archetype
- Check for naming conflicts

### 3. Identify Improvements

Check for:

#### Constitution Improvements
- Missing hard-stop rules
- Weak mandatory patterns
- Outdated preferred patterns
- Security gaps
- Performance issues

#### Workflow Improvements
- Missing validation steps
- Unclear instructions
- Missing examples
- No error handling
- Missing turbo annotations

#### Discovery Improvements
- Low confidence scores
- Missing keywords
- Wrong category
- File pattern gaps
- Error pattern gaps

#### Configuration Improvements
- Missing variables
- Outdated tool versions
- Missing validation rules
- No performance targets

### 4. Generate Refactoring Plan

Prioritize improvements:

**Priority 1: Critical (Security/Compliance)**
- Add missing hard-stop rules
- Fix security vulnerabilities
- Add compliance checks

**Priority 2: Important (Functionality)**
- Add missing mandatory patterns
- Improve workflow logic
- Fix discovery issues

**Priority 3: Nice-to-Have (Quality)**
- Add preferred patterns
- Improve examples
- Enhance documentation

### 5. Apply Refactorings

For each improvement:

#### Refactor Constitution
```markdown
# Before
## I. Hard-Stop Rules
- ✘ No hard-coded credentials

# After
## I. Hard-Stop Rules
- ✘ **No hard-coded credentials**: Never embed API keys, passwords, or tokens in code
- ✘ **No unencrypted secrets**: Always use secret management (Key Vault, etc.)
- ✘ **No secrets in logs**: Never log sensitive information
```

#### Refactor Workflows
```markdown
# Before
### 3. Generate Code
Create the artifact

# After
### 3. Parse Input Requirements
Extract from $ARGUMENTS:
- Required parameters
- Optional parameters
- Validation criteria

### 4. Validate Against Constitution
Check hard-stop rules before generation

### 5. Generate Code
Apply mandatory patterns:
- Pattern 1
- Pattern 2

### 6. Validate Output
```

#### Refactor Metadata
```yaml
# Before
keywords:
  primary:
    - "API"
    - "documentation"

# After
keywords:
  primary:
    - "API documentation"
    - "OpenAPI"
    - "Swagger"
    - "REST API docs"
  secondary:
    - "API reference"
    - "endpoint documentation"
    - "API explorer"
    - "GraphQL schema"
```

#### Refactor Environment Config
```yaml
# Before
variables:
  output_dir: "docs"

# After
# Performance Targets
performance:
  expected_runtime_secs: 5
  max_runtime_secs: 60

# Variables
variables:
  output_dir: "{{var.project_root}}/docs"
  api_version: "v1"
  format: "openapi-3.0"
  
# Validation Rules
validation:
  required_env_vars:
    - PROJECT_ROOT
  pre_execution_checks:
    - check: "openapi_validator_installed"
      description: "Verify OpenAPI validator is available"
```

### 6. Test Improvements

#### Test Discovery
```bash
# Test with various queries
python ${ARCHETYPES_BASEDIR}/scripts/python/discover-archetype.py \
  --input "generate API documentation" \
  --json

# Expected: High confidence (≥80%)
```

#### Test Workflows
```bash
# Test each workflow type
/scaffold-{archetype-slug} "test request"
/debug-{archetype-slug} "test error"
/refactor-{archetype-slug} "test code"
```

#### Test Constitution
```bash
# Verify guardrails enforce rules
  --file test_output.py \
  --json \
  --archetype {archetype-slug}
```

### 7. Update Documentation

Update:
- Category INDEX.md (if description changed)
- README examples (if usage changed)
- Constitution version number
- Env-config last updated date

### 8. Generate Refactoring Report

```
✅ Archetype Refactored: {archetype-slug}

📊 Improvements Applied:

Constitution:
- Added {n} hard-stop rules
- Enhanced {n} mandatory patterns
- Updated {n} preferred patterns

Workflows:
- Improved {n} workflow files
- Added {n} validation steps
- Added {n} examples

Discovery:
- Added {n} primary keywords
- Added {n} secondary keywords
- Improved confidence: {old}% → {new}%

Configuration:
- Updated tool versions
- Added {n} variables
- Added {n} validation rules

📈 Before/After Metrics:

Discovery Confidence:
- Before: {old_confidence}%
- After: {new_confidence}%
- Improvement: +{delta}%

Constitution Coverage:
- Hard-Stop Rules: {old_count} → {new_count}
- Mandatory Patterns: {old_count} → {new_count}

Workflow Quality:
- Validation Steps: {old_count} → {new_count}
- Examples: {old_count} → {new_count}
- Error Handlers: {old_count} → {new_count}

🧪 Test Results:
✓ Discovery test passed
✓ All workflows load correctly
✓ Constitution validates
✓ Environment config valid

📝 Next Steps:
1. Test with real use cases
2. Gather user feedback
3. Monitor discovery performance
4. Iterate on patterns
```

## Refactoring Patterns

### Pattern 1: Enhance Discovery Keywords

**When:** Archetype has low discovery confidence

**How:**
1. Analyze failed discovery attempts
2. Extract common terms users use
3. Add to primary keywords (if definitive)
4. Add to secondary keywords (if supporting)
5. Add high-confidence phrases

### Pattern 2: Strengthen Constitution

**When:** Generated code has quality issues

**How:**
1. Identify common mistakes
2. Add hard-stop rules for critical issues
3. Add mandatory patterns for required practices
4. Document rationale for each rule

### Pattern 3: Improve Workflow Clarity

**When:** Users struggle to use workflows

**How:**
1. Break down complex steps
2. Add concrete examples
3. Improve error messages
4. Add validation checkpoints

### Pattern 4: Modernize Tool Versions

**When:** Using outdated tools

**How:**
1. Research current best practices
2. Update tool versions in env-config
3. Update patterns for new features
4. Add migration notes if breaking changes

### Pattern 5: Add Missing Workflows

**When:** Some workflow types are incomplete

**How:**
1. Review similar archetypes for patterns
2. Adapt to current archetype's domain
3. Add domain-specific examples
4. Test thoroughly

## Examples

### Example 1: Improve Discovery
```
/refactor-archetype-architect "
Archetype: api-doc-generator
Issue: Only 45% confidence when users say 'generate swagger docs'
Goal: Improve discovery to 80%+
"

Output:
→ Analyzing current keywords...
→ Current primary: ["API", "documentation"]
→ Adding specific keywords:
  - "swagger"
  - "OpenAPI"
  - "API documentation"
→ Adding high-confidence phrases:
  - "swagger documentation"
  - "OpenAPI spec"
→ Testing discovery...
→ New confidence: 88% ✓
```

### Example 2: Strengthen Constitution
```
/refactor-archetype-architect "
Archetype: kubernetes-operator-builder
Issue: Generated operators missing RBAC definitions
Goal: Add hard-stop rule for RBAC
"

Output:
→ Adding to constitution...
✘ **No missing RBAC**: All operators must include RBAC manifests
✔ **RBAC validation**: Validate RBAC rules before deployment
→ Updating scaffold workflow to enforce...
→ Testing with sample generation...
→ RBAC check now enforced ✓
```

### Example 3: Modernize Configuration
```
/refactor-archetype-architect "
Archetype: python-package-builder
Issue: Using Python 3.7, now EOL
Goal: Update to Python 3.11+
"

Output:
→ Updating env-config.yaml...
→ Python version: 3.7 → 3.11
→ Updating patterns for new features:
  - Type hints with | operator
  - Match statements
  - Improved error messages
→ Updating constitution patterns...
→ Testing with Python 3.11... ✓
```

## Error Handling

**Archetype Not Found**:
```
❌ Cannot refactor: Archetype "{archetype-slug}" not found

Available archetypes in category {category}:
{list_archetypes}

Did you mean: {closest_match}?
```

**Breaking Changes**:
```
⚠️ Warning: Proposed changes may break existing usage

Breaking changes:
- {change_1}
- {change_2}

This will affect:
- Existing workflows using this archetype
- Generated code from previous versions

Proceed with breaking changes? [y/N]
```

## References

- **Archetype Patterns**: Browse .windsurf/workflows/ for examples
- **Constitution Best Practices**: See ${ARCHETYPES_BASEDIR}/memory/archetypes/
- **Discovery Optimization**: ${ARCHETYPES_BASEDIR}/scripts/python/discover-archetype.py
