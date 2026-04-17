---
description: Debug archetype creation issues (Archetype Architect)
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Identify Issue

Extract from $ARGUMENTS:
- What went wrong (file not created, discovery failing, etc.)
- Which archetype
- Error messages (if any)

### 2. Reproduce Issue via Simulation (CRITICAL ENHANCEMENT)

**Purpose:** Systematically reproduce and diagnose issues using simulation testing

**Philosophy:** User provides context; Cascade troubleshoots and reasons through solutions

#### 2.1 Parse User-Provided Context

Extract from $ARGUMENTS:
- **Observed symptoms or errors**
- **Expected vs actual behavior**
- **Specific workflow or constitutional rule involved**
- **Sample task that exhibits the problem**

#### 2.2 Design Reproduction Task

If user provided sample task:
- Use their exact task

If no sample task provided:
- Design representative task based on symptoms
- Extract from archetype's constitution use cases
- Ensure task should trigger the reported issue

Example:
```
Issue: "scaffold-kubernetes-operator-builder generates operators without RBAC"
Reproduction Task: "Create Kubernetes operator for managing ConfigMap resources"
Expected: Operator includes RBAC manifests
Actual: Operator missing RBAC definitions
```

#### 2.3 Execute Workflow Step-by-Step

Run the problematic workflow:
```
/{workflow-type}-{archetype-slug} "{reproduction_task}"
```

**Track during execution:**
- Each step executed
- Decisions made at each point
- Where issue manifests
- Reasoning steps and assumptions
- Constitutional rules applied (or not applied)
- Output generated

#### 2.4 Observe Where Issue Manifests

Document the exact step where problem occurs:

```
ISSUE REPRODUCTION LOG

Task: {reproduction_task}
Archetype: {archetype-slug}
Workflow: {workflow-type}-{archetype-slug}

EXECUTION TRACE:
─────────────────────────────────────────────────────
Step 1: {step_description}
  → Status: ✓ Executed successfully
  → Output: {output}

Step 2: {step_description}
  → Status: ✓ Executed successfully
  → Output: {output}

Step 3: {step_description}
  → Status: ⚠️ Issue detected
  → Expected: {expected_behavior}
  → Actual: {actual_behavior}
  → Issue: ❌ {issue_description}

Step 4: {step_description}
  → Status: ⏭️ Skipped (issue in previous step)

ISSUE MANIFESTATION:
─────────────────────────────────────────────────────
Location: Step 3 - {step_name}
Symptom: {observed_symptom}
Impact: {impact_description}
```

#### 2.5 Analyze Root Cause

Investigate multiple potential causes:

**A. Validate Archetype Structure**
- Check if all required files exist
- Verify file naming conventions
- Check directory structure

**B. Check for Workflow Ambiguities**
- Review step instructions for clarity
- Identify missing context or assumptions
- Check for contradictions between steps

**C. Identify Missing/Conflicting Constitutional Rules**
- Review hard-stop rules
- Check mandatory patterns
- Verify preferred patterns
- Look for rule conflicts

**D. Review Referenced Scripts/Configs**
- Check if scripts exist
- Verify script functionality
- Test script execution

**E. Check Cross-Archetype Integration**
- Verify orchestration calls
- Check archetype discovery
- Test sub-task delegation

**F. Check Platform Compatibility (CRITICAL)**
- Scan for hardcoded bash scripts without Python wrappers
- Check for `python3` commands (should be platform-agnostic)
- Verify path handling uses `pathlib` or `os.path.join()`
- Look for hardcoded path separators (`/` or `\`)
- Check virtual environment detection logic
- Test on Windows, Mac, and Linux if possible

#### 2.6 Generate Root Cause Analysis

```
ROOT CAUSE ANALYSIS

Issue: {issue_description}
Archetype: {archetype-slug}
Workflow: {workflow-type}-{archetype-slug}

PRIMARY CAUSE:
─────────────────────────────────────────────────────
Category: {structural/workflow/constitutional/script/integration}
Location: {specific_file_and_line}
Description: {detailed_explanation}

Example:
Category: Constitutional Rule Missing
Location: ${ARCHETYPES_BASEDIR}/archetype-architect/kubernetes-operator-builder-constitution.md
Description: Constitution lacks hard-stop rule enforcing RBAC generation.
             Workflow Step 5 says "Generate operator" but doesn't mandate RBAC.
             No validation checkpoint to verify RBAC exists.

CONTRIBUTING FACTORS:
─────────────────────────────────────────────────────
1. {factor_1}
   Impact: {impact}
   
2. {factor_2}
   Impact: {impact}

Example:
1. Workflow Step 5 is ambiguous
   Impact: Doesn't specify RBAC as required component
   
2. No validation script for RBAC
   Impact: Invalid operators pass through undetected

EVIDENCE:
─────────────────────────────────────────────────────
- Reproduction: {reproduction_result}
- File inspection: {inspection_result}
- Constitutional review: {review_result}
```

#### 2.7 Reason Through Correction Plan

Evaluate multiple fix approaches:

```
CORRECTION PLAN

Issue: {issue_description}

OPTION 1: {approach_1}
─────────────────────────────────────────────────────
Changes Required:
- {change_1}
- {change_2}

Pros:
+ {benefit_1}
+ {benefit_2}

Cons:
- {cost_1}
- {cost_2}

Breaking Changes: {yes/no}
Effort: {low/medium/high}

OPTION 2: {approach_2}
─────────────────────────────────────────────────────
Changes Required:
- {change_1}
- {change_2}

Pros:
+ {benefit_1}
+ {benefit_2}

Cons:
- {cost_1}
- {cost_2}

Breaking Changes: {yes/no}
Effort: {low/medium/high}

RECOMMENDED APPROACH: {option_number}
─────────────────────────────────────────────────────
Rationale: {explanation}

Example:
OPTION 1: Add hard-stop rule + validation script
Changes:
- Add "No operators without RBAC" to constitution
- Create validate-k8s-rbac.sh script via automation-scripter
- Add validation checkpoint in workflow Step 6

Pros:
+ Prevents issue at generation time
+ Provides clear error message
+ Reusable validation script

Cons:
- Requires new script creation
- Adds execution time (~2 seconds)

Breaking Changes: No
Effort: Medium (2-3 hours)

OPTION 2: Just update workflow instructions
Changes:
- Clarify Step 5 to explicitly mention RBAC

Pros:
+ Quick fix
+ No new files needed

Cons:
- Relies on LLM interpretation
- No enforcement mechanism
- Issue could recur

Breaking Changes: No
Effort: Low (15 minutes)

RECOMMENDED: Option 1
Rationale: Enforcement via hard-stop rule + validation prevents recurrence.
           Investment of 2-3 hours prevents future issues.
```

#### 2.8 Collaborate with User on Solution

Present findings and get approval:

```
═══════════════════════════════════════════════════════════════
DIAGNOSTIC REPORT
═══════════════════════════════════════════════════════════════

Issue: {issue_description}
Archetype: {archetype-slug}

ROOT CAUSE:
{paste_root_cause_analysis}

CORRECTION OPTIONS:
{paste_correction_plan}

RECOMMENDATION: {recommended_option}
{rationale}

SIDE EFFECTS:
{list_any_side_effects}

TESTING PLAN:
1. Apply fixes
2. Re-run reproduction task
3. Verify issue resolved
4. Run full simulation test
5. Check for regressions

═══════════════════════════════════════════════════════════════

Proceed with recommended approach? [Y/n/specify-option]
```

### 2.9 Archetype Architect's Debugging Responsibility (CRITICAL)

**What archetype-architect OWNS during debugging:**

| Responsibility | Description |
|----------------|-------------|
| **Structural Issues** | Missing files, wrong paths, naming mismatches |
| **Logical Inconsistencies** | Broken cross-references, invalid dependencies |
| **Discovery Problems** | Routing failures, low confidence scores |
| **Workflow Structure** | Missing sections, invalid YAML, unclear steps |
| **Integration Failures** | Delegation language errors, ecosystem incompatibility |

**What archetype-architect DELEGATES during debugging:**

| Debug Need | Delegate To | Delegation Command |
|------------|-------------|-------------------|
| Script bugs | automation-scripter | `/debug-automation "{script_path}" "{error}"` |
| Documentation issues | documentation-evangelist | `/debug-documentation "{doc_path}"` |
| Test failures | unit-test-code-coverage | `/debug-unit-test-code-coverage "{test_path}"` |
| CI/CD pipeline issues | microservice-cicd-architect | `/debug-microservice-cicd "{pipeline}"` |

**Debugging Delegation Pattern:**
```
archetype-architect detects:
  "This archetype's validation script is failing with error X"
  → Delegates to: /debug-automation "{script_path}" "Error: {error_message}"
  → automation-scripter diagnoses and fixes script
  → archetype-architect validates script integrates correctly
  → archetype-architect updates workflow references if needed
```

**When to Delegate vs Handle Directly:**

| Scenario | Action |
|----------|--------|
| Script execution errors | DELEGATE to automation-scripter |
| Documentation broken links | DELEGATE to documentation-evangelist |
| Test assertion failures | DELEGATE to testing archetypes |
| Manifest schema invalid | HANDLE directly (structural) |
| Constitution rules missing | HANDLE directly (logical quality) |
| Workflow structure broken | HANDLE directly (consistency) |
| Discovery routing wrong | HANDLE directly (integration) |

### 2.10 Apply Fixes Systematically

Once approved:

1. **Update Workflows** (archetype-architect handles directly)
   - Clarify ambiguous steps
   - Add validation checkpoints
   - Reference new scripts/configs

2. **Modify Constitutional Rules** (archetype-architect handles directly)
   - Add missing hard-stop rules
   - Enhance mandatory patterns
   - Update preferred patterns

3. **Update Referenced Scripts/Configs/Assets** (DELEGATE to specialists)
   - Create new validation scripts: `/scaffold-automation "{script_spec}"`
   - Fix existing scripts: `/debug-automation "{script_path}" "{error}"`
   - Update configurations: Delegate based on config type

4. **Maintain Version History** (archetype-architect handles directly)
   - Update changelog.md (NOT constitution version)
   - Document breaking changes (if any)

#### 2.10 Validate Fixes via Simulation

Re-run the reproduction task:

```
VALIDATION SIMULATION

Task: {reproduction_task}
Archetype: {archetype-slug}
Workflow: {workflow-type}-{archetype-slug}

EXECUTION TRACE (After Fix):
─────────────────────────────────────────────────────
Step 1: ✓ Executed successfully
Step 2: ✓ Executed successfully
Step 3: ✓ Fixed - now includes {expected_behavior}
Step 4: ✓ Validation passed
Step 5: ✓ Output complete

ISSUE STATUS:
─────────────────────────────────────────────────────
Before: ❌ {issue_description}
After: ✅ Issue resolved

VERIFICATION:
─────────────────────────────────────────────────────
✓ Reproduction task now works correctly
✓ Expected behavior achieved
✓ No regressions detected
✓ Constitutional rules enforced
```

#### 2.11 Generate Resolution Report

```
═══════════════════════════════════════════════════════════════
ISSUE RESOLUTION REPORT
═══════════════════════════════════════════════════════════════

Issue: {issue_description}
Archetype: {archetype-slug}
Status: ✅ RESOLVED

ROOT CAUSE:
{summary}

FIXES APPLIED:
─────────────────────────────────────────────────────
1. {fix_1}
   Files Modified: {file_list}
   
2. {fix_2}
   Files Modified: {file_list}

VALIDATION RESULTS:
─────────────────────────────────────────────────────
✓ Reproduction task passes
✓ No regressions detected
✓ Full simulation test: PASS

PREVENTIVE RECOMMENDATIONS:
─────────────────────────────────────────────────────
1. {recommendation_1}
2. {recommendation_2}

NEXT STEPS:
─────────────────────────────────────────────────────
1. Test with additional use cases
2. Update documentation
3. Monitor for similar issues

═══════════════════════════════════════════════════════════════
```

### 3. Common Issues Checklist (Fallback)

If simulation approach doesn't apply, use checklist-based debugging:

#### Issue 1: Discovery Not Working
**Symptoms:** Archetype not detected by `/scaffold` or other core orchestrators

**Diagnosis:**
- Check manifest.yaml entry exists
- Verify keywords match user queries
- Test with discover-archetype.py

**Fix:**
```bash
# Test discovery
python ${ARCHETYPES_BASEDIR}/scripts/python/discover-archetype.py \
  --input "your test query" --json

# If confidence is low, add more keywords to manifest.yaml
# Focus on primary keywords that users would naturally use
```

#### Issue 2: Workflow Files Not Found
**Symptoms:** "Workflow not found" error when invoking

**Diagnosis:**
- Check file naming: `{action}-{archetype-slug}.md`
- Verify directory structure: `.windsurf/workflows/{category}/{archetype-slug}/`
- Check INDEX.md references

**Fix:**
- Ensure exact naming convention
- Verify all 6 workflow files exist
- Update category INDEX.md

#### Issue 3: Constitution Not Loading
**Symptoms:** Guardrails not enforcing, rules not applied

**Diagnosis:**
- Check file path in workflow files
- Verify constitution file exists
- Check markdown formatting

**Fix:**
```markdown
# Correct path in workflow:
- The constitution rules are already loaded in context above.

# Verify file exists:
ls ${ARCHETYPES_BASEDIR}/archetype-architect/{archetype-slug}-constitution.md
```

#### Issue 4: Environment Validation Failing
**Symptoms:** validate-env.sh returns errors

**Diagnosis:**
- Check env-config.yaml exists
- Verify required_env_vars are set
- Check tool availability

**Fix:**
```bash
# Test environment validation (cross-platform)
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype {archetype_slug}

# Or use platform-specific script:
# On Unix/Linux/Mac:
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype {archetype_slug}
# On Windows:
.cdo-aifc\scripts\powershell\validate-env.ps1 -Json -Archetype {archetype_slug}

# Set missing environment variables
export REQUIRED_VAR="value"
```

#### Issue 5: Metadata Not Recognized
**Symptoms:** Category not showing archetype, discovery fails

**Diagnosis:**
- Check YAML syntax in manifest.yaml
- Verify indentation (use spaces, not tabs)
- Check archetype-slug matches directory name

**Fix:**
```yaml
# Correct format:
{archetype-slug}:  # Must match directory name
  display_name: "Display Name"
  description: "Description"
  keywords:
    primary:
      - "keyword1"
```

#### Issue 6: Slug Naming Mismatch
**Symptoms:** Files exist but not loading

**Diagnosis:**
- Check consistency across all files
- Verify kebab-case format
- Check for typos

**Fix:**
- Rename files to match exact slug
- Update all references in workflows
- Regenerate if necessary

#### Issue 7: Platform Compatibility Failures (CRITICAL)
**Symptoms:** Archetype works on Mac/Linux but fails on Windows (or vice versa)

**Diagnosis:**
- Check for hardcoded bash scripts (`.sh`) without Python wrappers
- Look for `python3` commands (Windows uses `python`)
- Check for hardcoded path separators (`/` or `\`)
- Verify virtual environment detection

**Fix:**
```python
# Replace bash scripts with Python wrappers
# Before:
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json`

# After:
Run cross-platform validation:
python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json

# Use platform utilities for paths
from platform_utils import PlatformUtils
python_cmd = PlatformUtils.get_python_executable()
config_path = PlatformUtils.join_path(".cdo-aifc", "memory", "archetypes")

# Replace python3 with platform-agnostic wrapper
# Before: python3 script.py
# After: python script.py  # or use PlatformUtils.get_python_executable()
```

**Prevention:**
- Always use Python wrappers for validation scripts
- Use `pathlib.Path` or `os.path.join()` for all file paths
- Test on multiple platforms before release
- Add platform compatibility check to test workflow
- Archetype slug must be consistent everywhere:
  - Directory name: `{archetype-slug}/`
  - Workflow files: `{action}-{archetype-slug}.md`
  - Constitution: `{archetype-slug}-constitution.md`
  - Metadata key: `{archetype-slug}:`

#### Issue 7: Index Files Not Updated
**Symptoms:** Archetype works but not discoverable in navigation

**Diagnosis:**
- Check if archetype listed in category INDEX.md
- Check if listed in main workflows INDEX.md
- Check if listed in constitution INDEX.md

**Fix:**
- Update all 4 INDEX.md files:
  1. Category INDEX.md
  2. Main workflows INDEX.md
  3. Constitution INDEX.md
  4. Templates INDEX.md

### 3. Validate File Structure

Run validation checklist:

```bash
# Check all required files exist
ARCHETYPE_SLUG="{archetype-slug}"
CATEGORY="{category}"

echo "Checking file structure for $ARCHETYPE_SLUG..."

# Workflow files (6)
for action in scaffold debug refactor test compare document; do
  file=".windsurf/workflows/$CATEGORY/$ARCHETYPE_SLUG/${action}-${ARCHETYPE_SLUG}.md"
  [ -f "$file" ] && echo "✓ $file" || echo "✗ MISSING: $file"
done

# Constitution
file="${ARCHETYPES_BASEDIR}/archetype-architect/${ARCHETYPE_SLUG}-constitution.md"
[ -f "$file" ] && echo "✓ $file" || echo "✗ MISSING: $file"

# Env config
file="${ARCHETYPES_BASEDIR}/archetype-architect/templates/env-config.yaml"
[ -f "$file" ] && echo "✓ $file" || echo "✗ MISSING: $file"

# Metadata entry
grep -q "$ARCHETYPE_SLUG:" ".windsurf/workflows/$CATEGORY/manifest.yaml" \
  && echo "✓ Metadata entry exists" \
  || echo "✗ MISSING: Metadata entry"
```

### 4. Test Discovery

```bash
# Test with primary keywords
python ${ARCHETYPES_BASEDIR}/scripts/python/discover-archetype.py \
  --input "{primary keywords from metadata}" \
  --json

# Expected: High confidence (≥80%) for this archetype
```

### 5. Test Workflow Invocation

```bash
# Test direct invocation
/{action}-{archetype-slug} "test request"

# Expected: Workflow should load and execute
```

### 6. Generate Diagnostic Report

```
🔍 Archetype Diagnostic Report

Archetype: {archetype-slug}
Category: {category}

📁 File Structure:
{list_all_files_with_status}

📊 Discovery Test:
- Test Query: "{test_query}"
- Detected: {yes/no}
- Confidence: {score}%
- Status: {pass/fail}

⚙️ Configuration:
- Constitution: {exists/missing}
- Env Config: {exists/missing}
- Metadata Entry: {exists/missing}

📚 Index Updates:
- Category INDEX: {updated/missing}
- Main INDEX: {updated/missing}
- Constitution INDEX: {updated/missing}
- Templates INDEX: {updated/missing}

🔧 Issues Found:
{list_issues}

✅ Fixes Applied:
{list_fixes}

📝 Remaining Actions:
{list_remaining_actions}
```

## Error Handling

**Archetype Not Found**:
```
❌ Archetype "{archetype-slug}" not found

Searched in:
- .windsurf/workflows/{category}/{archetype-slug}/
- ${ARCHETYPES_BASEDIR}/archetype-architect/
- ${ARCHETYPES_BASEDIR}/archetype-architect/templates/

Did you mean:
{suggest_similar_archetypes}

Or create it with:
/scaffold-archetype-architect "..."
```

**Multiple Issues**:
```
⚠️ Multiple Issues Detected

Priority 1 (Critical):
{critical_issues}

Priority 2 (Important):
{important_issues}

Priority 3 (Optional):
{optional_issues}

Fix in order? [Y/n]
```

## Examples

### Example 1: Discovery Not Working
```
/debug-archetype-architect "
Issue: Created 'kubernetes-operator-builder' but /scaffold doesn't detect it
Category: 05-infrastructure-devops
Error: Low confidence (25%) when testing discovery
"

Output:
→ Checking manifest.yaml...
→ Found entry for kubernetes-operator-builder
→ Testing keywords...
→ Issue: Primary keywords too generic
→ Recommendation: Add more specific keywords:
  - "kubernetes operator"
  - "CRD controller"
  - "reconciliation loop"
→ Updated metadata
→ Retesting... Confidence now 85% ✓
```

### Example 2: Files Missing
```
/debug-archetype-architect "
Issue: Workflow files not loading for 'api-doc-generator'
Category: 09-documentation-requirements
"

Output:
→ Checking file structure...
✓ scaffold-api-doc-generator.md
✓ debug-api-doc-generator.md
✗ MISSING: refactor-api-doc-generator.md
✗ MISSING: test-api-doc-generator.md
✗ MISSING: compare-api-doc-generator.md
✗ MISSING: document-api-doc-generator.md

→ Creating missing workflow files...
→ All files created ✓
```

## References

- **System Quick Start**: ../QUICK_START.md
- **Discovery Script**: ${ARCHETYPES_BASEDIR}/scripts/python/discover-archetype.py
- **Validation Scripts**: ${ARCHETYPES_BASEDIR}/scripts/bash/
