---
description: Test archetype functionality and discovery (Archetype Architect)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Archetype to Test

Extract from $ARGUMENTS:
- Archetype slug
- Category
- Test scope (full validation or specific aspect)

### 1.5 Run Automated Quality Analysis (RECOMMENDED FIRST STEP)

**Purpose:** Use the `analyze-archetypes.py` script to quickly assess archetype quality and identify issues before detailed manual testing.

**Execute Quality Analysis:**

```bash
# Analyze specific archetype with verbose output
python ${ARCHETYPES_BASEDIR}/archetype-architect/scripts/analyze-archetypes.py \
  --archetype {archetype-slug} --verbose

# Or get JSON output for programmatic use
python ${ARCHETYPES_BASEDIR}/archetype-architect/scripts/analyze-archetypes.py \
  --archetype {archetype-slug} --json
```

**Quality Gates Checked Automatically:**

| Gate | Requirement | Threshold |
|------|-------------|-----------|
| **Structural Pass** | All required files exist | manifest.yaml, constitution, 6 workflows |
| **Constitution Pass** | Minimum rule counts | 3 hard-stop, 5 mandatory, 2 preferred |
| **Workflow Pass** | Required sections present | Execution Steps, Error Handling, Examples |
| **Discovery Pass** | Primary keywords route correctly | Score ≥30 |
| **Analysis Pass** | Priority rating | P3 (passing) |

**Priority Levels:**

| Priority | Severity | Action Required |
|----------|----------|-----------------|
| **P0** | Critical | Missing required files - immediate fix needed |
| **P1** | High | Constitution/workflow deficiencies - fix before use |
| **P2** | Medium | Platform/keyword issues - fix when possible |
| **P3** | Low | Passing - minor improvements optional |

**Expected Output (Passing Archetype):**

```
═══════════════════════════════════════════════════════════════
ARCHETYPE QUALITY REPORT: {archetype-slug}
═══════════════════════════════════════════════════════════════

Priority: P3
Score: EXCELLENT
Total Issues: 0

MANIFEST: ✅
  Keywords: 6 (min 5)
  Workflows: 6

CONSTITUTION: ✅
  Hard-Stop Rules: 5 (min 3)
  Mandatory Patterns: 8 (min 5)
  Preferred Patterns: 4 (min 2)

WORKFLOWS:
  scaffold: ✅
  debug: ✅
  refactor: ✅
  test: ✅
  compare: ✅
  document: ✅

PLATFORM COMPATIBILITY: ✅

QUALITY GATES:
  1. Structural Pass: ✅ All required files exist
  2. Constitution Pass: ✅ Meets minimum rule counts (3/5/2)
  3. Workflow Pass: ✅ All required sections present
  4. Discovery Pass: ⏳ Run discover-archetype.py to verify score ≥30
  5. Analysis Pass: ✅ Priority is P3
```

**If Analysis Shows Issues:**

Based on priority, route to appropriate remediation:

| Priority | Remediation Approach |
|----------|---------------------|
| **P0** | `/scaffold-archetype-architect` to generate missing files |
| **P1** | `/refactor-archetype-architect` to fix constitution/workflow structure |
| **P2** | Update manifest.yaml keywords or add platform wrappers |
| **P3** | Proceed with detailed testing below |

**Batch Analysis (All Archetypes):**

```bash
# Analyze all archetypes and generate reports
python ${ARCHETYPES_BASEDIR}/archetype-architect/scripts/analyze-archetypes.py \
  --output results --verbose

# Reports generated:
# - results/structural-scan-summary.csv
```

### 2. Run File Structure Test

Check all required files exist:
- 6 workflow files (scaffold, debug, refactor, test, compare, document)
- Constitution file
- Environment config file
- Metadata entry

### 3. Run Constitution Quality Test

Validate constitution has:
- Minimum 3 hard-stop rules
- Minimum 5 mandatory patterns
- Minimum 2 preferred patterns
- Proper section structure

### 4. Run Discovery Performance Test

Test archetype discovery with primary keywords:
- Extract primary keywords from metadata
- Run discover-archetype.py
- Verify confidence score ≥80%
- Verify correct archetype detected

### 5. Run Workflow Syntax Test

For each workflow file, check:
- Valid YAML frontmatter
- Has description field
- Uses $ARGUMENTS placeholder
- Has Execution Steps section
- Has Error Handling section
- Has Examples section

### 6. Run Configuration Test

Validate env-config.yaml:
- Valid YAML syntax
- Has performance section
- Has variables section
- Has validation section

### 7. Run Index Updates Test

Check archetype is listed in:
- Category INDEX.md
- Main workflows INDEX.md
- Constitution INDEX.md
- Templates INDEX.md

### 8. Run Cross-Platform Compatibility Test (CRITICAL ENHANCEMENT)

**Purpose:** Validate archetype works on Windows, Mac, and Linux

#### 8.1 Check for Platform-Specific Code

Scan all workflow files for platform-specific patterns:

**Hard-Stop Violations:**
- ❌ Hardcoded bash scripts (`.sh`) without Python wrappers
- ❌ `python` commands (should use platform-agnostic wrapper)
- ❌ Hardcoded path separators (`/` or `\`)
- ❌ Bash-specific syntax (`[[`, `$OSTYPE`, etc.)

**Scan Commands:**
```bash
# Check for bash script references
grep -r "\.sh " .windsurf/workflows/{category}/{archetype-slug}/

# Check for python usage (should be platform-agnostic)
grep -r "python " .windsurf/workflows/{category}/{archetype-slug}/

# Check for hardcoded separators
grep -r "['\"].*/" .windsurf/workflows/{category}/{archetype-slug}/
```

#### 8.2 Validate Script Wrappers

For each referenced script, verify cross-platform support:

**Preferred (✓):** Python wrapper exists
- Check: `${ARCHETYPES_BASEDIR}/scripts/python/{script_name}.py`

**Acceptable (⚠️):** Both platform scripts exist
- Check: `${ARCHETYPES_BASEDIR}/scripts/bash/{script_name}.sh`
- Check: `${ARCHETYPES_BASEDIR}/scripts/powershell/{script_name}.ps1`

**Violation (❌):** Only bash script exists
- Missing: PowerShell or Python equivalent

#### 8.3 Test Virtual Environment Detection

Verify workflows use correct Python path for each OS:

**Windows:**
```
Expected: .venv\Scripts\python.exe
Check: Workflow uses PlatformUtils.get_python_executable()
```

**Unix/Mac:**
```
Expected: .venv/bin/python
Check: Workflow uses PlatformUtils.get_python_executable()
```

#### 8.4 Validate Path Handling

Check that all file paths use cross-platform patterns:

**✓ Correct:**
```python
from pathlib import Path
config_path = Path(".cdo-aifc") / "memory" / "archetypes"

# OR
import os
config_path = os.path.join(".cdo-aifc", "memory", "archetypes")
```

**❌ Incorrect:**
```python
config_path = "${ARCHETYPES_BASEDIR}/memory/archetypes"  # Unix-only
config_path = ".cdo-aifc\\memory\\archetypes"  # Windows-only
```

#### 8.5 Generate Platform Compatibility Report

```
PLATFORM COMPATIBILITY REPORT
─────────────────────────────────────────────────────
Archetype: {archetype-slug}
Test Date: {timestamp}

SCRIPT REFERENCES:
✓ 3 Python wrappers found
✓ 0 bash-only scripts
✓ All scripts cross-platform compatible

PYTHON EXECUTABLE:
✓ Uses PlatformUtils.get_python_executable()
✓ No hardcoded python commands

PATH HANDLING:
✓ All paths use pathlib.Path or os.path.join()
✓ No hardcoded separators found

PLATFORM-SPECIFIC SYNTAX:
✓ No bash-specific syntax detected
✓ No PowerShell-specific syntax detected

VERDICT: PASS
Archetype is fully cross-platform compatible.
```

### 8.6 Archetype Architect's Testing Responsibility (CRITICAL)

**What archetype-architect OWNS during testing:**

| Responsibility | Description |
|----------------|-------------|
| **Structural Validation** | File existence, manifest schema, constitution format |
| **Logical Consistency** | Cross-references, naming conventions, BASEDIR usage |
| **Discovery Performance** | Routing accuracy, confidence thresholds |
| **Workflow Structure** | Standard sections, YAML frontmatter, examples |
| **Integration Points** | Delegation language accuracy, ecosystem compatibility |

**What archetype-architect DELEGATES during testing:**

| Test Type | Delegate To | Delegation Command |
|-----------|-------------|-------------------|
| Script unit tests | unit-test-code-coverage | `/test-unit-test-code-coverage "{archetype}/scripts/"` |
| Script regression tests | regression-test-coverage | `/test-regression-test-coverage "{archetype}/scripts/"` |
| Documentation validation | documentation-evangelist | `/test-documentation "{archetype}/README.md"` |
| CI/CD pipeline tests | microservice-cicd-architect | `/test-microservice-cicd "{pipeline}"` |

**Multi-Layer Testing Strategy:**

```
archetype-architect testing:
  Layer 1: STRUCTURAL (archetype-architect owns)
    → File existence, manifest schema, naming consistency
    
  Layer 2: LOGICAL (archetype-architect owns)
    → Cross-references valid, dependencies accurate
    
  Layer 3: DISCOVERY (archetype-architect owns)
    → Routing works, confidence meets threshold
    
  Layer 4: SCRIPT QUALITY (delegate to testing archetypes)
    → /test-unit-test-code-coverage for script unit tests
    → /test-regression-test-coverage for regression tests
    
  Layer 5: INTEGRATION (delegate to solution-test)
    → /solution-test for end-to-end archetype integration
```

**Execute Delegated Tests:**

```bash
# Delegate script testing to unit-test-code-coverage
/scaffold-unit-test-code-coverage "
Create test suite for {archetype-slug} scripts:
- Test all functions in scripts/ directory
- Coverage target: 80%
- Output: {archetype-slug}/tests/test_scripts.py
"

# Run the generated tests
pytest {archetype-slug}/tests/test_scripts.py -v --cov
```

### 9. Run Simulation Testing (CRITICAL ENHANCEMENT - Phase 2)

**Purpose:** Validate archetype effectiveness, not just structure. This catches workflow clarity issues that structural validation misses.

**Steps:**

#### 9.1 Design Representative Task

Extract primary use case from archetype's constitution and metadata:
- The constitution rules are already loaded in context above.
- Identify the most common use case from "Use Cases" section
- Create sample task that exercises key capabilities

Example tasks by archetype type:
- **Code generators:** "Create {artifact} with {key_features}"
- **Infrastructure:** "Deploy {resource} with {configuration}"
- **Data engineering:** "Build {pipeline} processing {data_type}"
- **Documentation:** "Generate {doc_type} for {target}"

#### 9.2 Execute Target Archetype Workflow

Run the scaffold workflow as Cascade would:
```
/{workflow-type}-{archetype-slug} "{sample_task}"
```

**During execution, track:**
- Each step taken
- Decisions made at ambiguous points
- Missing information or assumptions
- Constitutional rules applied
- Mandatory patterns enforced
- Output quality

#### 9.3 Evaluate Simulation Results

Check the following criteria:

**Output Quality:**
- ✓ Did workflow produce expected output?
- ✓ Is output complete and functional?
- ✓ Does output follow constitutional rules?

**Workflow Clarity:**
- ✓ Were all steps clear and unambiguous?
- ✓ Could a typical user follow without confusion?
- ✓ Were examples helpful and accurate?

**Constitutional Enforcement:**
- ✓ Did hard-stop rules prevent anti-patterns?
- ✓ Were mandatory patterns applied correctly?
- ✓ Were preferred patterns suggested appropriately?

**Issues to Flag:**
- ❌ Ambiguous steps requiring interpretation
- ❌ Missing context or assumptions
- ❌ Unclear instructions
- ❌ Missing validation steps
- ❌ Inadequate error handling

#### 9.4 Generate Reasoning Trace

Document the simulation execution:

```
SIMULATION TRACE

Task: {sample_task}
Archetype: {archetype-slug}
Workflow: scaffold-{archetype-slug}
Timestamp: {timestamp}

EXECUTION LOG:
─────────────────────────────────────────────────────
Step 1: {step_description}
  → Action taken: {action}
  → Clarity: {clear/ambiguous}
  → Ambiguity: {if any, describe}
  → Decision made: {if required}

Step 2: {step_description}
  → Action taken: {action}
  → Clarity: {clear/ambiguous}
  → Constitutional rule applied: {rule_name}
  
Step 3: {step_description}
  → Action taken: {action}
  → Clarity: {clear/ambiguous}
  → Issue: ❌ Step says "Generate {artifact}" but doesn't specify:
    • Which {tool/library} to use?
    • What {configuration} options?
    • How to handle {edge_case}?
  → Workaround: Made assumption based on best practices

[... continue for all steps ...]

FINAL OUTPUT:
─────────────────────────────────────────────────────
{generated_artifact_summary}

QUALITY ASSESSMENT:
─────────────────────────────────────────────────────
✓ Output is complete
✓ Output follows constitutional rules
✓ Mandatory patterns applied
⚠️ Some preferred patterns missing

ISSUES FOUND:
─────────────────────────────────────────────────────
1. Step 3: Ambiguous tool selection
   Severity: MEDIUM
   Impact: User may choose wrong tool
   
2. Step 5: Missing validation checkpoint
   Severity: HIGH
   Impact: Invalid output may proceed undetected
   
3. Step 7: Unclear error handling
   Severity: LOW
   Impact: Users may not know how to recover from errors

RECOMMENDATIONS:
─────────────────────────────────────────────────────
1. Step 3: Add explicit tool selection with rationale
   Before: "Generate {artifact}"
   After: "Generate {artifact} using {tool} because {reason}"
   
2. Step 5: Add validation checkpoint
   Add: "// turbo
         Run `${ARCHETYPES_BASEDIR}/scripts/bash/validate-{artifact}.sh --file {output}`"
   
3. Step 7: Expand error handling section
   Add: Common error patterns and recovery steps

SIMULATION VERDICT:
─────────────────────────────────────────────────────
Status: PASS WITH WARNINGS
Workflow is functional but has clarity issues that could confuse users.
Recommend addressing 3 issues before production use.
```

#### 9.5 Update Test Scope

If test scope is "full", run simulation for multiple workflows:
- scaffold-{archetype-slug} (primary)
- debug-{archetype-slug} (with sample error)
- refactor-{archetype-slug} (with sample code)

### 10. Routing Validation Tests (CRITICAL ENHANCEMENT)

**Purpose:** Validate that the target archetype routes correctly via core and solution workflows, using realistic user prompts.

#### 10.1 Positive Routing Tests

For the archetype being tested, verify discovery correctly routes to it:

**Extract Test Prompts from Archetype:**
1. Read manifest.yaml keywords
2. Read constitution use cases
3. Generate realistic user prompts

**Execute Routing Tests:**

```bash
# Test 1: Primary keyword routing
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
  --query "scaffold a new {archetype_keyword_1} solution" --json

# Expected: archetype matches with score ≥30

# Test 2: Use case routing  
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
  --query "{use_case_from_constitution}" --json

# Expected: archetype matches with score ≥30

# Test 3: Display name routing
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
  --query "create {display_name} implementation" --json

# Expected: archetype matches with score ≥30
```

**Validation Criteria:**
- ✓ Score ≥30 for primary keywords
- ✓ Correct archetype name in result
- ✓ Correct workflow name in result

#### 10.2 Negative Routing Tests

Verify prompts intended for OTHER archetypes don't incorrectly route to this archetype:

**Generate Negative Test Cases:**
1. Select 3 unrelated archetypes from different categories
2. Use their primary keywords as test prompts
3. Verify this archetype does NOT match with high confidence

```bash
# Test: Unrelated domain should not match
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
  --query "debug SQL query syntax error" --json --top 3

# Expected: archetype-architect should NOT be in top 3 results
# (unless the archetype being tested IS sql-query-crafter)
```

**Validation Criteria:**
- ✓ Archetype does NOT appear in top 3 for unrelated prompts
- ✓ If it appears, score is <15 (low confidence)

#### 10.3 Core Workflow Routing Tests

Verify the archetype routes correctly through each of the 6 core workflows:

```bash
# Test each action type
for ACTION in scaffold refactor compare test debug document; do
  python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
    --query "${ACTION} {archetype_primary_keyword}" \
    --action ${ACTION} --json
done
```

**Validation Criteria:**
- ✓ Each action returns correct workflow name
- ✓ Workflow name matches manifest.yaml entry

#### 10.4 Solution vs Core Routing Tests

Validate when routing should go to core (1:1) vs solution (1:many):

**Single Archetype Prompt (should route to core):**
```bash
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
  --query "scaffold {specific_archetype_use_case}" --json

# Expected: Single high-confidence match (score ≥30)
# Action: Route to /scaffold-{archetype}
```

**Multi-Archetype Prompt (should route to solution):**
```bash
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/discover-archetype.py \
  --query "scaffold complete data platform with ML and reporting" --json --top 5

# Expected: Multiple matches with distributed confidence
# Action: Route to /solution-scaffold
```

#### 10.5 Generate Routing Validation Report

```
ROUTING VALIDATION REPORT
─────────────────────────────────────────────────────
Archetype: {archetype-slug}
Test Date: {timestamp}

POSITIVE ROUTING TESTS:
─────────────────────────────────────────────────────
Test 1 (Primary Keyword): {PASS/FAIL}
  Query: "scaffold a new {keyword} solution"
  Expected: {archetype-slug} with score ≥30
  Actual: {archetype} with score {score}

Test 2 (Use Case): {PASS/FAIL}
  Query: "{use_case}"
  Expected: {archetype-slug} with score ≥30
  Actual: {archetype} with score {score}

Test 3 (Display Name): {PASS/FAIL}
  Query: "create {display_name}"
  Expected: {archetype-slug} with score ≥30
  Actual: {archetype} with score {score}

NEGATIVE ROUTING TESTS:
─────────────────────────────────────────────────────
Test 4 (Unrelated Domain 1): {PASS/FAIL}
  Query: "{unrelated_query_1}"
  Expected: {archetype-slug} NOT in top 3 or score <15
  Actual: {result}

Test 5 (Unrelated Domain 2): {PASS/FAIL}
  Query: "{unrelated_query_2}"
  Expected: {archetype-slug} NOT in top 3 or score <15
  Actual: {result}

CORE WORKFLOW ROUTING:
─────────────────────────────────────────────────────
scaffold:  {PASS/FAIL} → {workflow_name}
refactor:  {PASS/FAIL} → {workflow_name}
compare:   {PASS/FAIL} → {workflow_name}
test:      {PASS/FAIL} → {workflow_name}
debug:     {PASS/FAIL} → {workflow_name}
document:  {PASS/FAIL} → {workflow_name}

ROUTING VERDICT:
─────────────────────────────────────────────────────
Status: {PASS/PASS WITH WARNINGS/FAIL}
Positive Tests: {n}/{total} passed
Negative Tests: {n}/{total} passed
Core Workflows: {n}/6 mapped correctly
```

### 11. Generate Comprehensive Test Report

```
═══════════════════════════════════════════════════════════════
ARCHETYPE VALIDATION REPORT
═══════════════════════════════════════════════════════════════

Archetype: {archetype-slug}
Category: {category}
Test Date: {timestamp}
Test Scope: {full/structural/simulation}

PHASE 1: STRUCTURAL VALIDATION
─────────────────────────────────────────────────────
1. FILE STRUCTURE: {PASS/FAIL}
   ✓ 6 workflow files present
   ✓ Constitution file present
   ✓ Environment config present
   ✓ Metadata entry present

2. CONSTITUTION: {PASS/WARN/FAIL}
   ✓ {n} hard-stop rules (minimum 3)
   ✓ {n} mandatory patterns (minimum 5)
   ✓ {n} preferred patterns (minimum 2)
   {warnings if any}

3. DISCOVERY: {PASS/WARN/FAIL}
   ✓ Confidence score: {percentage}% (target ≥80%)
   ✓ Correct archetype detected
   {warnings if any}

4. WORKFLOWS: {PASS/WARN}
   ✓ Valid YAML frontmatter
   ✓ All required sections present
   {warnings if any}

5. CONFIGURATION: {PASS/FAIL}
   ✓ Valid YAML syntax
   ✓ All required sections present

6. INDEX UPDATES: {PASS/WARN}
   ✓ Listed in all 4 INDEX.md files
   {warnings if any}

7. PLATFORM COMPATIBILITY: {PASS/WARN/FAIL}
   ✓ Script references: {n} Python wrappers, {n} bash-only
   ✓ Python executable: Uses platform-agnostic wrapper
   ✓ Path handling: {n} paths use pathlib/os.path.join
   ⚠️ {warnings if any}
   ❌ {failures if any}

PHASE 2: SIMULATION TESTING
─────────────────────────────────────────────────────
8. SAMPLE TASK: {task_description}

9. EXECUTION: {PASS/FAIL}
   ✓ Workflow completed successfully
   ✓ Output generated
   {failures if any}

10. OUTPUT QUALITY: {PASS/WARN/FAIL}
    ✓ Output is complete
    ✓ Constitutional rules followed
    ⚠️ {warnings if any}

11. WORKFLOW CLARITY: {PASS/WARN/FAIL}
    ✓ {n} steps clear and unambiguous
    ⚠️ {n} steps with ambiguities
    ❌ {n} steps with critical issues

12. REASONING TRACE: See detailed trace below

13. ISSUES FOUND: {count}
    - {count} HIGH severity
    - {count} MEDIUM severity
    - {count} LOW severity

14. RECOMMENDATIONS: {count}
    See detailed recommendations below

OVERALL VERDICT
─────────────────────────────────────────────────────
Status: {PASS/PASS WITH WARNINGS/FAIL}

{summary_statement}

DETAILED SIMULATION TRACE
─────────────────────────────────────────────────────
{paste_full_trace_from_step_8.4}

RECOMMENDED IMPROVEMENTS
─────────────────────────────────────────────────────
{list_all_recommendations_with_priority}

NEXT STEPS
─────────────────────────────────────────────────────
{if PASS}: Archetype ready for production use
{if PASS WITH WARNINGS}: Address {n} warnings before production
{if FAIL}: Fix {n} critical issues and re-test

═══════════════════════════════════════════════════════════════
```

## Error Handling

**Test Failures**: List failed tests and required actions

**Partial Pass**: List warnings and recommendations

## Examples

### Example 1: Full Validation
```
/test-archetype-architect "
Archetype: kubernetes-operator-builder
Category: 05-infrastructure-devops
Scope: full
"
```

### Example 2: Discovery Test Only
```
/test-archetype-architect "
Archetype: api-doc-generator
Scope: discovery
"
```

## References

- **System Quick Start**: ../QUICK_START.md
- **Discovery Script**: ${ARCHETYPES_BASEDIR}/scripts/python/discover-archetype.py
