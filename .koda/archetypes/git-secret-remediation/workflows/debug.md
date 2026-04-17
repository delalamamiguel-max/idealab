---
description: Debug failed git secret remediation attempts and GitHub Security Alert rejections
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --json --archetype git_secret_remediation` and parse for ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/git-secret-remediation/templates/env-config.yaml` for configuration

### 3. Parse Debug Request
Extract from $ARGUMENTS:
- **Issue type**: GitHub alert rejection, git-filter-repo failure, force-push error, etc.
- **Error messages**: Exact error text from GitHub or git
- **Steps attempted**: What remediation steps were already tried

### 4. Diagnose Common Issues

#### Issue: GitHub Security Alert Dismissal Rejected
**Most Common Causes:**
1. Attestation was not copied exactly as written
2. Invalid dismissal reason selected ("Used in tests" or "Won't fix")
3. Secret still active (detected by Security Liaison validity tools)
4. Insufficient supporting documentation
5. Misunderstanding of "False Positive" - it is NOT a secret in commit history but not in default branch

**Debug Steps:**
1. Verify attestation text matches exactly (character-by-character)
2. Check for extra spaces, line breaks, or formatting
3. Ensure correct attestation type was used:
   - **Revoked Attestation**: For AT&T-owned secrets that were rotated
   - **Non-AT&T Attestation**: For secrets not owned by AT&T (use "Revoked" reason)
   - **False Positive Attestation**: ONLY for tool misidentification (e.g., Key Vault names, SID config)
4. Verify supporting documentation was provided (if required)
5. Check if credential was actually rotated (Security Liaison tests with validity tools)
6. Confirm you did NOT select "Used in tests" or "Won't fix" - these are auto-rejected

**Resolution:**
- Copy attestation again from official source (do not type manually)
- Paste without any modifications
- Upload additional documentation to MDP-Security Alert Response Document Tracker
- If rejected for active credential, verify rotation was completed
- Resubmit dismissal request

#### Issue: Bypass Request Rejected
**Common Causes:**
1. Flagged item IS actually a secret (not a false positive)
2. Attestation missing or incorrect
3. Insufficient evidence that value is not a secret

**Debug Steps:**
1. Re-verify the flagged value is truly not a secret
2. Check if it's a Key Vault name, SID, or config parameter
3. Verify False Positive attestation was used

**Resolution:**
- If it IS a secret → Stop bypass attempt, remediate properly
- If NOT a secret → Provide stronger documentation proving it's not sensitive
- Upload evidence to MDP-Security Alert Response Document Tracker

#### Issue: git-filter-repo Command Failed
**Common Causes:**
- Tool not installed
- Repository not a fresh clone
- Invalid replacement pattern syntax

**Debug Steps:**
```bash
# Check if git-filter-repo is installed
git filter-repo --version

# Check git repository status
git status

# Verify replacement file syntax
cat secret-replacements.txt
```

**Resolution:**
- Install git-filter-repo: `pip install git-filter-repo`
- Clone repository fresh if needed
- Fix replacement file syntax (use `literal:` or `regex:` prefix)

#### Issue: Secret Still Found After Remediation
**Common Causes:**
- Secret has multiple variations (URL-encoded, escaped, etc.)
- Secret in binary files or compressed archives
- Incorrect search pattern

**Debug Steps:**
```bash
# Search with different encodings
git log --all --full-history -S"${SECRET_PATTERN}"
git log --all --full-history -S"$(echo -n ${SECRET_PATTERN} | base64)"

# Check for URL-encoded versions
git grep -i "password%3D" $(git rev-list --all)
```

**Resolution:**
- Add all variations to replacement file
- Use regex patterns for flexible matching
- Consider BFG Repo-Cleaner for binary files

#### Issue: Force-Push Rejected
**Common Causes:**
- Branch protection enabled
- Insufficient permissions
- Remote repository locked

**Debug Steps:**
```bash
# Check branch protection
git remote -v
# Check GitHub/Azure DevOps branch settings

# Verify permissions
git push origin --dry-run
```

**Resolution:**
- Temporarily disable branch protection
- Request admin permissions
- Coordinate with repository owner

#### Issue: Team Members' Repositories Broken After Force-Push
**Common Causes:**
- Team members didn't re-sync properly
- Local changes conflict with rewritten history

**Debug Steps:**
```bash
# Check current branch state
git status
git log --oneline -10

# Check divergence from remote
git fetch origin
git log HEAD..origin/main
```

**Resolution:**
```bash
# Save local work
git stash

# Hard reset to remote
git fetch origin
git reset --hard origin/main
git clean -fdx

# Restore local work
git stash pop
```

### 5. Generate Debug Report
Create detailed report with:
- Issue description
- Root cause analysis
- Steps to reproduce
- Recommended resolution
- Prevention measures

### 6. Validate Fix
After applying resolution, run validation:
```bash
# Verify secret is removed
git log --all --full-history -S"${SECRET_PATTERN}"

# Check GitHub alert status
# (Manual check in GitHub Security tab)
```

## Error Handling

**Common Issue**: Attestation keeps getting rejected
**Resolution**: Contact Security Liaison directly to clarify requirements

**Configuration Error**: Missing Key Vault access
**Resolution**: Request "Key Vault Secrets User" role from Azure admin

## Examples

**Example 1**: `/debug-git-secret-remediation "GitHub alert rejected with 'Invalid attestation'"`
Output: Diagnosis showing attestation was paraphrased instead of copied exactly

**Example 2**: `/debug-git-secret-remediation "git-filter-repo says 'not a fresh clone'"`
Output: Resolution steps to clone repository fresh and re-run

## References

Original: `vibe_cdo/git_secret_remediation/prompts/debug_prompt.md` | Constitution: (pre-loaded above)
