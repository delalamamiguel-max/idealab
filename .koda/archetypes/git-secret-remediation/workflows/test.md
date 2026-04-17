---
description: Test and validate git secret remediation completeness and GitHub alert resolution
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype git_secret_remediation` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Create Isolated Test Environment (CRITICAL SAFETY)

**Hard-Stop Rule:** Never test on production repositories

#### 2.1 Generate Disposable Test Repository

**Note:** First ensure TestRepoGenerator exists by running orchestration in scaffold workflow, or create it manually.

```python
import sys
sys.path.append('.cdo-aifc/scripts/python')
from test_repo_generator import TestRepoGenerator

# Create isolated test repo
test_repo = TestRepoGenerator(
    name="git-secret-test",
    fake_secrets=[
        "password=FAKE_SECRET_12345",
        "API_KEY=sk-FAKE_KEY_67890",
        "DATABASE_URL=postgresql://user:FAKE_PASS@localhost/db"
    ],
    num_commits=10,
    num_branches=3
)

repo_path = test_repo.create()
print(f"Test repo: {repo_path}")
```

#### 2.2 Validate Test Environment

```bash
# Verify we're in test repo
if [[ "$PWD" != *"/tmp/"* ]] && [[ "$PWD" != *"test"* ]]; then
    echo "❌ ERROR: Not in test environment!"
    echo "This workflow only runs on disposable test repositories"
    exit 1
fi

echo "✅ Confirmed: Running in isolated test environment"
```

#### 2.3 Execute Remediation in Test Environment

```bash
cd ${repo_path}
/scaffold-git-secret-remediation "password=FAKE_SECRET_12345"
```

#### 2.4 Cleanup After Tests

```python
# Destroy test repo after validation
test_repo.cleanup()
echo "✅ Test environment cleaned up"
```

### 3. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/git-secret-remediation/templates/env-config.yaml` for configuration

### 4. Parse Test Scope
Extract from $ARGUMENTS: What to test (secret removal completeness, Key Vault integration, GitHub alert status, preventive measures)

### 5. Test Secret Removal Completeness

#### Test 1: Search Git History
```bash
# Test that secret is completely removed from all commits
SECRET_PATTERN="your-secret-pattern"

# Search commit messages
git log --all --grep="${SECRET_PATTERN}"

# Search file contents in all commits
git log --all --full-history -S"${SECRET_PATTERN}"

# Search with git grep across all history
git grep "${SECRET_PATTERN}" $(git rev-list --all)
```

**Expected Result:** No matches found

#### Test 2: Check All Branches
```bash
# Test secret removal across all branches
for branch in $(git branch -r | grep -v '\->'); do
    echo "Checking $branch"
    git grep "${SECRET_PATTERN}" $branch || echo "✅ Clean"
done
```

**Expected Result:** All branches clean

#### Test 3: Check Tags
```bash
# Test secret removal in all tags
for tag in $(git tag); do
    echo "Checking $tag"
    git grep "${SECRET_PATTERN}" $tag || echo "✅ Clean"
done
```

**Expected Result:** All tags clean

#### Test 4: Verify Backup Branch
```bash
# Verify backup branch was created and contains original history
git branch | grep "backup-before-secret-removal"
```

**Expected Result:** Backup branch exists

### 6. Test Key Vault Integration

#### Test 5: Verify Secret in Key Vault
```bash
# Test that secret was stored in Key Vault
az keyvault secret show --vault-name <vault-name> --name <secret-name>
```

**Expected Result:** Secret exists in Key Vault

#### Test 6: Test Application Access
```python
# Test that application can retrieve secret from Key Vault
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://<vault-name>.vault.azure.net/", credential=credential)

try:
    secret = client.get_secret("<secret-name>")
    print(f"✅ Successfully retrieved secret: {secret.name}")
except Exception as e:
    print(f"❌ Failed to retrieve secret: {e}")
```

**Expected Result:** Secret retrieved successfully

#### Test 7: Verify Old Credential Revoked
```bash
# Test that old credential no longer works
# (Specific test depends on credential type)

# Example for database password:
# psql "postgresql://user:OLD_PASSWORD@host/db" -c "SELECT 1"
# Expected: Connection refused or authentication failed

# Example for API key:
# curl -H "Authorization: Bearer OLD_API_KEY" https://api.example.com/test
# Expected: 401 Unauthorized
```

**Expected Result:** Old credential is invalid

### 7. Test GitHub Security Alert Status

#### Test 8: Verify Alert Dismissal
**Manual Test:**
1. Navigate to GitHub repository
2. Go to **Security** → **Secret scanning**
3. Verify alert is marked as "Dismissed" or "Closed"
4. Check dismissal reason matches what was submitted:
   - **Revoked**: For AT&T owned secrets OR non-AT&T secrets
   - **False Positive**: ONLY for tool misidentification (NOT secrets in history but not in default branch)
5. Verify correct attestation is present in comments (copied exactly, not paraphrased)
6. Confirm "Used in tests" or "Won't fix" was NOT selected (auto-rejected)

**Expected Result:** Alert properly dismissed with correct attestation

#### Test 9: Verify Security Liaison Approval
**Manual Test:**
1. Check GitHub alert comments for Security Liaison response
2. Verify approval was granted (not rejected or pending)
3. Check approval date is within SLA:
   - Standard: 3 US business days
   - Escalated: 1 business day
4. If rejected, verify follow-up was completed:
   - Additional documentation uploaded to MDP-Security Alert Response Document Tracker
   - Attestation re-copied exactly from source
   - Credential rotation verified

**Expected Result:** Security Liaison approved the dismissal

#### Test 9.1: Verify Bypass Request (if applicable)
**Manual Test (for Push Protection blocks):**
1. Verify flagged item was truly NOT a secret before bypass was requested
2. Check False Positive attestation was used
3. Verify supporting documentation was provided
4. Confirm bypass was approved

**Expected Result:** Bypass approved only for legitimate false positives

### 8. Test Preventive Measures

#### Test 10: Verify Pre-Commit Hooks
```bash
# Test that pre-commit hooks are installed
pre-commit --version
ls -la .git/hooks/pre-commit

# Test hook detects secrets
echo "password=TestPassword123" > test-secret.txt
git add test-secret.txt
git commit -m "Test commit"
# Expected: Commit blocked by detect-secrets hook

# Cleanup
git reset HEAD test-secret.txt
rm test-secret.txt
```

**Expected Result:** Pre-commit hook blocks secret

#### Test 11: Verify .gitignore Coverage
```bash
# Test that secret files are ignored
touch .env
touch credentials.json
touch private.key

git status
# Expected: These files should not appear in untracked files

# Cleanup
rm .env credentials.json private.key
```

**Expected Result:** Secret files are ignored

#### Test 12: Verify GitHub Push Protection
**Manual Test:**
1. Create a test branch with a fake secret
2. Attempt to push to remote
3. Verify GitHub blocks the push with secret detection warning

**Expected Result:** Push blocked by GitHub

### 9. Test Team Coordination

#### Test 13: Verify Team Members Re-synced
```bash
# Test that team members' repositories are in sync
# (Run on each team member's machine)

git fetch origin
git status
# Expected: "Your branch is up to date with 'origin/main'"

git log --oneline -5
# Expected: Commit hashes match across all team members
```

**Expected Result:** All team members in sync

### 10. Generate Test Report

Create comprehensive test report with:
- Test execution summary (passed/failed/skipped)
- Secret removal validation results
- Key Vault integration test results
- GitHub alert status verification
- Preventive measures validation
- Recommendations for any failed tests

### 11. Validate and Report
Generate outputs and documentation. Report completion.

## Error Handling

**Common Issue**: Secret still found in history
**Resolution**: Re-run remediation with all secret variations (URL-encoded, escaped, etc.)

**Configuration Error**: Cannot access Key Vault
**Resolution**: Verify RBAC permissions and Azure credentials

## Examples

**Example 1**: `/test-git-secret-remediation "Verify database password removed from history"`
Output: Test report showing secret completely removed, Key Vault integration working, GitHub alert dismissed

**Example 2**: `/test-git-secret-remediation "Validate preventive measures"`
Output: Test results for pre-commit hooks, .gitignore, and GitHub Push Protection

## Test Checklist

- [ ] Secret not found in any commit (Test 1)
- [ ] Secret not found in any branch (Test 2)
- [ ] Secret not found in any tag (Test 3)
- [ ] Backup branch exists (Test 4)
- [ ] Secret stored in Key Vault (Test 5)
- [ ] Application can access Key Vault (Test 6)
- [ ] Old credential revoked (Test 7)
- [ ] GitHub alert dismissed with correct reason - NOT "Used in tests" or "Won't fix" (Test 8)
- [ ] Correct attestation used and copied exactly (Test 8)
- [ ] Security Liaison approved within SLA (Test 9)
- [ ] Bypass request approved (if applicable) - only for true false positives (Test 9.1)
- [ ] Pre-commit hooks installed (Test 10)
- [ ] .gitignore covers secret files (Test 11)
- [ ] GitHub Push Protection enabled (Test 12)
- [ ] Team members re-synced (Test 13)

## Phase 2: Simulation Testing

### 12. Design Reproduction Task

Task: "Remove password=FAKE_SECRET_12345 from test repository"

Expected Outcomes:
✓ Backup branch created
✓ Dry-run shows changes
✓ Secret removed from all commits
✓ Repository still functional
✓ No production repos touched

### 13. Execute Workflow

Run: `/scaffold-git-secret-remediation "password=FAKE_SECRET_12345"`

Track:
- [ ] Backup branch creation
- [ ] Dry-run execution
- [ ] Secret removal completeness
- [ ] Key Vault storage
- [ ] Verification steps
- [ ] Test isolation maintained

### 14. Evaluate Results

✓ Backup branch created?
✓ Dry-run showed changes?
✓ Secret removed from all commits?
✓ Repository still functional?
✓ No production repos touched?
✓ Key Vault integration working?

### 15. Generate Reasoning Trace

Document any unclear steps or missing validations:

```markdown
# Git Secret Remediation Simulation Results

**Date:** [YYYY-MM-DD]
**Test Scenario:** Remove fake secret from test repository
**Status:** [PASS/FAIL]

## Issues Identified

### Critical Issues
- [ ] Test isolation not enforced
- [ ] Production repo could be affected
- [ ] Backup not created before changes

### Warnings
- [ ] Unclear error messages
- [ ] Missing validation steps
- [ ] No rollback mechanism

### Observations
- [ ] Test repo generator missing
- [ ] No automated cleanup
- [ ] Manual verification required

## Recommended Fixes

1. Add explicit test environment validation
2. Create TestRepoGenerator utility
3. Add automated cleanup
4. Improve error messages

## Test Verdict

[PASS/FAIL] - [Explanation]

**Confidence in Archetype:** [0-100%]
**Readiness for Production:** [Yes/No]
```

## References

Original: `vibe_cdo/git_secret_remediation/prompts/test_prompt.md` | Constitution: (pre-loaded above)
