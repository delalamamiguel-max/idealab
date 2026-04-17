---
description: Remediate exposed secrets from git history and resolve GitHub Security Alerts per AT&T policy
---

User input: $ARGUMENTS

## 🔴 AT&T SECURITY POLICY - MANDATORY COMPLIANCE

This workflow remediates exposed secrets and guides you through GitHub Security Alert resolution per AT&T's Secret Remediation Policy (Effective Aug 11, 2025).

**Reference:** [AT&T DevHub - Secret Remediation Guide](https://devhub.web.att.com/docs/default/component/apm0044907-documentation-library/secrets/remediation/)

## ⚠️ CRITICAL WARNINGS

### GitHub Security Alert Resolution Required
After removing secrets from git history, you **MUST** manually resolve the GitHub Security Alert with the correct attestation. **Failure to provide the exact attestation will result in automatic rejection.**

### Commit History Policy
- **DO NOT modify commit history** for secrets already pushed to remote
- **ONLY modify local commits** that have not been pushed yet
- For pushed secrets, submit an alert dismissal request to resolve the detection
- Secrets already pushed to a remote repository or flagged during a migration **cannot be removed** from the commit history

### Three Required Attestations (Effective Aug 11, 2025)

You MUST copy and paste ONE of these attestations **EXACTLY AS WRITTEN** when dismissing the GitHub Security Alert:

**1. Revoked Attestation** (for secrets you rotated):
```
Submitter confirms the secret has been remediated per AT&T policy and poses no risk. Falsification of this attestation violates AT&T's Code of Business Conduct and may result in disciplinary action.
```

**2. False Positive Attestation** (for non-secrets flagged by scanner):
```
Submitter confirms the alert is a false positive and poses no risk. Falsification of this attestation violates AT&T's Code of Business Conduct and may result in disciplinary action.
```

**3. Secrets Not Owned by AT&T Attestation** (for third-party secrets):
```
The submitter affirms that the secret is neither owned by AT&T nor by its employees or contractors, has been removed from the default branch. Falsification of this attestation violates AT&T's Code of Business Conduct and may result in disciplinary action.
```

## Prerequisites

Before running this workflow:
- [ ] Access to GitHub repository with Security tab permissions
- [ ] Identified the secret alert in GitHub Security → Secret Scanning (if applicable)
- [ ] Determined if secret is in local-only commits or already pushed
- [ ] Access to Azure Key Vault or HashiCorp Vault for secure storage
- [ ] Contact information for your Security Liaison
- [ ] `git-filter-repo` installed (or will be installed by this workflow)

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Verify Git Repository
Verify we're in a git repository by running `git rev-parse --git-dir`. If this fails, halt and ask user to navigate to their git repository.

### 2. Check if Secret is Pushed to Remote
```bash
# Check if commits containing secret are pushed
git log origin/$(git branch --show-current)..HEAD
```

If output is **empty**, secret is already pushed → Skip to Step 15 (GitHub Alert Resolution)
If output **shows commits**, secret is local only → Continue to Step 3

### 3. Create Safety Backup
Create a backup branch with timestamp:
```bash
git branch backup-before-secret-removal-$(date +%Y%m%d-%H%M%S)
```

### 4. Parse Secret Information
Extract from $ARGUMENTS:
- **Secret pattern**: The exact string or pattern to remove (e.g., "password=MyP@ssw0rd", "API_KEY=sk-...")
- **File paths** (optional): Specific files to scan (if known)
- **Replacement text** (optional): What to replace the secret with (default: "***REMOVED***")

If secret pattern is not provided, ask user:
```
Please provide the exact secret string you want to remove from git history.
Examples:
- "password=MySecretPassword123"
- "API_KEY=sk-1234567890abcdef"
- "postgresql://user:PASSWORD@host/db"
```

### 5. Install Remediation Tool (if needed)

**Option A: git-filter-repo (Recommended for complex patterns)**

Check if `git-filter-repo` is available:
```bash
git filter-repo --version
```

If not found, install it:

**Windows (with Python):**
```bash
pip install git-filter-repo
```

**Alternative (download directly):**
```bash
curl -o git-filter-repo https://raw.githubusercontent.com/newren/git-filter-repo/main/git-filter-repo
chmod +x git-filter-repo
```

**Option B: BFG Repo-Cleaner (Faster for large repositories)**

Download from: https://rtyley.github.io/bfg-repo-cleaner/

**Requires Java.** To remove a specific file:
```bash
bfg --delete-files YOUR-FILE-WITH-SENSITIVE-DATA
```

To replace sensitive text:
```bash
bfg --replace-text passwords.txt
```

**Note:** BFG automatically protects the latest commit and replaces text with `***REMOVED***`.

### 6. Create Replacement File
Create a temporary file `secret-replacements.txt` with the secret patterns to remove:

```
# Format: literal:old_text==>new_text
literal:${SECRET_PATTERN}==>${REPLACEMENT_TEXT}
```

**Example:**
```
literal:password=MyP@ssw0rd==>password=***REMOVED***
literal:API_KEY=sk-1234567890abcdef==>API_KEY=***REMOVED***
```

### 7. Preview Changes (Dry Run)
**IMPORTANT:** Always do a dry run first to see what will be changed.

```bash
git filter-repo --replace-text secret-replacements.txt --dry-run
```

Review the output carefully. Ask user to confirm before proceeding.

### 8. Execute Secret Removal
After user confirmation, execute the actual history rewrite:

```bash
git filter-repo --replace-text secret-replacements.txt --force
```

**Note:** The `--force` flag is required because this rewrites history.

### 9. Verify Removal
Search the entire repository history to confirm the secret is gone:

```bash
# Search all commits for the secret pattern
git log --all --full-history -S"${SECRET_PATTERN}"

# Search all file contents in history
git grep "${SECRET_PATTERN}" $(git rev-list --all)
```

If any results are found, the secret was not fully removed. Investigate and repeat if necessary.

### 10. Check Current Files
Verify the secret is not in current working directory:

```bash
# Case-insensitive search in all files
grep -r -i "${SECRET_PATTERN}" .
```

### 11. Store Secret in Key Vault
**MANDATORY:** Store the secret securely before pushing:

**Option 1: Azure Key Vault**
```bash
# Add secret to Azure Key Vault
az keyvault secret set --vault-name <vault-name> --name <secret-name> --value "<secret-value>"
```

**Option 2: HashiCorp Vault**
- Follow HashiCorp onboarding: [HashiCorp Vault - Home](https://devhub.web.att.com/docs/default/component/apm0044907-documentation-library/hashicorp-vault/)
- Note: Requires client licenses ($160/client annually for Test and Production)

### 12. Update Code to Reference Key Vault
Update your application code to retrieve the secret from Key Vault instead of hardcoding it.

**Example (Python with Azure Key Vault):**
```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://<vault-name>.vault.azure.net/", credential=credential)
secret = client.get_secret("<secret-name>")
```

### 13. Update Remote Repository (if needed)
**⚠️ ONLY FOR LOCAL COMMITS - COORDINATE WITH TEAM**

If the secret was only in local commits, push the cleaned history:

```bash
# For local commits only (no force needed)
git push origin [branch_name]
```

If you need to force-push (get approval first):
1. Ensure all team members have committed and pushed their work
2. Notify team to NOT push until after the force-push completes
3. Verify you have the correct remote URL: `git remote -v`

```bash
# Force-push (ONLY if approved)
git push origin --force --all
git push origin --force --tags
```

### 14. Cleanup
Remove the temporary replacement file:
```bash
rm secret-replacements.txt
```

---

## GitHub Security Alert Resolution (MANUAL STEPS)

### 15. Navigate to GitHub Security Alert
**🔴 CRITICAL:** You must manually complete these steps in GitHub to resolve the security alert.

1. Open your repository in GitHub
2. Click the **Security** tab
3. Click **Secret scanning** under "Vulnerability alerts"
4. Select **Default** or **Generic** option
5. Click on the detected secret alert

### 16. Remove Secret from Default Branch (if not already done)
If the secret still exists in the default branch:

```bash
# Checkout the default branch
git checkout main  # or master

# Remove the secret from the file
# Replace with Key Vault reference: ${KEY_VAULT_SECRET_NAME}

# Commit the removal
git add [file_name]
git commit -m "Remove exposed secret, replace with Key Vault reference"

# Push to remote
git push origin main
```

### 17. Revoke and Rotate the Exposed Credential
**🔴 MANDATORY - IMMEDIATE ACTION REQUIRED**

The exposed credential is compromised and must be revoked:

- [ ] **Revoke** the credential immediately to prevent unauthorized access
- [ ] **Rotate** by generating a new credential
- [ ] **Secure** the new credential in Azure Key Vault or HashiCorp Vault

**Examples:**
- Database password: Change in database system
- API key: Regenerate in API provider portal
- OAuth token: Revoke and generate new token
- SSH key: Remove from authorized_keys and generate new key

### 18. Determine Correct Dismissal Reason
Choose the appropriate dismissal reason based on your situation:

| Scenario | Dismissal Reason | Attestation Required | Notes |
|----------|------------------|---------------------|-------|
| Secret revoked, AT&T owned, validity Active/Inactive/Publicly leaked | **Revoked** | Revoked Attestation | Store new credential in Key Vault |
| Secret revoked, NOT owned by AT&T, removed from default branch | **Revoked** | Non-AT&T Attestation | Must provide documentation proving AT&T doesn't own it |
| Tool misidentified value (e.g., Key Vault name, SID config parameter) | **False Positive** | False Positive Attestation | May require supporting documentation |
| Intentionally exposed for public use (e.g., Google Maps public key) | **False Positive** | False Positive Attestation | May require supporting documentation |

**❌ NEVER USE - Will Be Automatically Rejected:**
- "Used in tests" - NOT VALID, secret still exposed, exposing AT&T to significant risk
- "Won't fix" - NOT VALID, secret still exposed, exposing AT&T to significant risk

**⚠️ False Positive Clarification:**
A false positive is when the tool **misidentifies** a value as a secret. It is **NOT** a secret that exists in commit history but not in the default branch.

### 19. Submit Alert Dismissal or Bypass Request in GitHub
**🔴 CRITICAL:** Follow these steps EXACTLY or your request will be automatically rejected.

#### For Alert Dismissal (Revoked or False Positive):
In GitHub:
1. Open the secret scanning alert
2. Click **Dismiss alert** or **Close as**
3. Select the appropriate reason (**Revoked** or **False Positive**)
4. In the comment field, **copy and paste the EXACT attestation** from the Prerequisites section above
   - Do NOT modify the attestation text in any way
   - Do NOT paraphrase or summarize
   - Copy the entire statement including the Code of Business Conduct warning
5. Attach supporting documentation if required:
   - For **Revoked (AT&T owned)**: Screenshots showing Key Vault storage, proof of rotation
   - For **Revoked (Non-AT&T)**: Documentation proving AT&T doesn't own the credential
   - For **False Positive**: Evidence the value is not a secret
6. Click **Submit** or **Dismiss alert**

#### For Bypass Request (Push Protection Block):
If GitHub Push Protection blocked your push:
1. Review the blocked secret in the push protection alert
2. Verify the flagged item is NOT actually a secret
3. If it IS a secret → Stop and remediate properly
4. If it is NOT a secret (false positive) → Submit bypass request with False Positive attestation
5. Attach relevant documentation proving it's not a secret

### 20. Upload Supporting Documentation (If Required)
If your Security Liaison requests additional documentation:

1. Go to **MDP-Security Alert Response Document Tracker**
2. Upload relevant documentation:
   - Screenshots showing Key Vault storage
   - Proof of credential rotation
   - Evidence for false positive claims
   - Ownership documentation for non-AT&T secrets

### 21. Wait for Security Liaison Review
**SLA (Service Level Agreement):**
- **Standard Request:** 3 US business days
- **Escalated Request:** 1 business day (requires proper escalation)

**Escalation Criteria:**
- Deployment blocked by secret alert
- Urgent production fix needed
- Time-sensitive security issue

**To Escalate:**
1. Flag request as "Escalated" in dismissal comment
2. Contact your Security Liaison directly (email/chat)

### 22. Handle Review Decision

**If APPROVED:**
- ✅ Alert marked as "Dismissed" in GitHub
- ✅ You can proceed with pull requests and deployments
- ✅ No further action required

**If REJECTED:**
Common rejection reasons:
- Missing or incorrect attestation (most common)
- Attestation was modified or paraphrased
- Insufficient supporting documentation
- Secret still active (detected by validity tools)
- Invalid dismissal reason selected

**Next Steps if Rejected:**
1. Review rejection feedback from Security Liaison
2. Ensure attestation is copied **EXACTLY** as written (no modifications)
3. Provide additional evidence to MDP-Security Alert Response Document Tracker
4. Verify credential was actually rotated (Security Liaison uses validity tools to test)
5. Resubmit with corrections

### 23. Conduct Post-Incident Review
After remediation is complete:

- [ ] Document root cause of secret exposure
- [ ] Identify process gaps that allowed the exposure
- [ ] Implement preventive measures (see Prevention section)
- [ ] Update team training on secret management
- [ ] Review and update CI/CD pipelines for secret detection

## Error Handling

### Error: "git-filter-repo requires a fresh clone"
**Resolution:** 
```bash
# Add a temporary remote
git remote add temp-origin $(git remote get-url origin)
# Or clone fresh and re-run
```

### Error: "refusing to force push"
**Resolution:**
1. Check if branch is protected in GitHub/GitLab/Azure DevOps
2. Temporarily disable branch protection
3. Force push
4. Re-enable branch protection

### Error: "Secret still found in history"
**Resolution:**
1. The secret may have multiple variations (URL-encoded, escaped, etc.)
2. Add all variations to `secret-replacements.txt`
3. Re-run the filter-repo command
4. Use regex patterns if needed: `regex:pattern==>replacement`

### Error: "Alert Dismissal Rejected"
**Resolution:**
1. **Most Common:** Attestation was not copied exactly as written
   - Go back to Prerequisites section
   - Copy the attestation again (do not type it manually)
   - Paste it exactly as is into the GitHub comment field
2. Provide additional supporting documentation
3. Verify credential was actually rotated
4. Resubmit the dismissal request

### Error: "Cannot Access GitHub Security Tab"
**Resolution:**
1. Request "Security Manager" or "Admin" role for the repository
2. Contact repository owner or GitHub organization admin
3. Verify you're logged into correct GitHub organization (ATT-DP1, etc.)

## Advanced Options

### Remove Secret from Specific Files Only
If you know the exact files containing the secret:
```bash
git filter-repo --path path/to/file.py --replace-text secret-replacements.txt
```

### Remove Entire Files from History
If a file should never have been committed:
```bash
git filter-repo --path path/to/secret-file.env --invert-paths
```

### Use Regex Patterns
For complex patterns (e.g., any password in a connection string):
```
regex:password=[^@]+@==>password=***REMOVED***@
regex:sk-[a-zA-Z0-9]{32}==>***REMOVED_API_KEY***
```

## Orchestration: Generate Test Infrastructure

**Prerequisites:** Ensure Python dependencies are installed:
```bash
pip install pyyaml
```

**Instead of manually creating test repo generator, delegate to automation-scripter:**

```bash
python3 .cdo-aifc/scripts/python/discover-archetype.py \
  --input "Create python script to generate test git repository" \
  --json
```

✓ Detected: Automation Scripter (confidence: 92%)  
  Routing to: /scaffold-automation

Execute:
```
/scaffold-automation "Create Python class TestRepoGenerator that:
- Creates temporary git repo in /tmp/
- Initializes with git init
- Adds commits with fake secrets embedded in files
- Creates multiple branches with different secret variations
- Provides cleanup function to destroy repo
- Returns repo path for testing
- Includes validation that repo is in /tmp/ (safety check)
- Supports configurable number of commits and branches"
```

Output: `.cdo-aifc/scripts/python/test_repo_generator.py`

**Benefits:**
- ✅ Test infrastructure follows best practices
- ✅ Proper error handling and validation
- ✅ Safety checks prevent production repo damage
- ✅ Reusable across all secret remediation tests

## Examples

**Example 1: Local Secret (Not Yet Pushed)**
```
/scaffold-git-secret-remediation password=MySecretP@ssw0rd123
```
Workflow will remove secret from local commits, store in Key Vault, and push clean history.

**Example 2: Pushed Secret with GitHub Alert**
```
/scaffold-git-secret-remediation "API_KEY=sk-1234567890abcdef"
```
Workflow will guide through history cleanup AND GitHub Security Alert resolution with correct attestation.

**Example 3: Multiple Secrets**
```
/scaffold-git-secret-remediation
# Then provide multiple patterns when prompted
```

## Post-Remediation Checklist

- [ ] Secret removed from git history (verified with `git log` and `git grep`)
- [ ] Secret stored in Key Vault (Azure or HashiCorp)
- [ ] Code updated to reference Key Vault
- [ ] Credential revoked and rotated
- [ ] GitHub Security Alert dismissed with correct attestation
- [ ] Security Liaison approved dismissal (for pushed secrets)
- [ ] All team members notified and re-synced (if force-push was used)
- [ ] Security incident documented
- [ ] Post-incident review completed
- [ ] Preventive measures implemented

## Prevention: Avoid Future Secret Exposures

### 1. Enable GitHub Push Protection
In GitHub repository settings:
1. Go to **Settings** → **Security** → **Code security and analysis**
2. Enable **Push protection** for secret scanning
3. This blocks pushes containing detected secrets

### 2. Install Pre-Commit Hooks
```bash
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
EOF

# Install hooks
pre-commit install

# Create baseline
detect-secrets scan > .secrets.baseline
```

### 3. Use Visual Git Tools
Avoid catch-all commands:
- ❌ Don't use: `git add .` or `git add -A`
- ✅ Do use: Visual staging in VS Code, Windsurf, or GitHub Desktop

### 4. Add .gitignore Patterns
```gitignore
# Environment files
.env
.env.local
.env.*.local

# Configuration with secrets
config/secrets.yaml
**/appsettings.Development.json

# Key files
*.pem
*.key
*.p12
*.pfx
```

## AT&T Security Resources

### Internal Links
- **DevHub Secret Remediation Guide:** https://devhub.web.att.com/docs/default/component/apm0044907-documentation-library/secrets/remediation/
- **HashiCorp Vault Onboarding:** https://devhub.web.att.com/docs/default/component/apm0044907-documentation-library/hashicorp-vault/
- **Azure Key Vault Security:** https://learn.microsoft.com/en-us/azure/key-vault/general/security-features
- **MDP-Security Alert Response Document Tracker:** (Contact your Security Liaison for access)

### External References
- **git-filter-repo Tool:** https://github.com/newren/git-filter-repo
- **GitHub: Removing Sensitive Data:** https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
- **OWASP Secrets Management:** https://owasp.org/www-community/vulnerabilities/Use_of_hard-coded_password

### Contact Information
- **Your Security Liaison:** (Check your team's security contact list)
- **CSO Encryption Technology Team:** For HashiCorp Vault licenses and POC support

## Related Workflows

- `/debug-git-secret-remediation` - Troubleshoot failed remediations
- `/document-git-secret-remediation` - Document security incidents
- `/test-git-secret-remediation` - Validate remediation completeness

---

**Last Updated:** 2026-01-06  
**Archetype:** Git Secret Remediation  
**Policy Version:** Effective August 11, 2025  
**Estimated Time:** 
- Local secrets: 10-20 minutes
- Pushed secrets: 30-60 minutes + 3 business days for Security Liaison review  
**Risk Level:** 🔴 HIGH - Security incident, requires immediate action  
**Compliance:** Mandatory per AT&T Code of Business Conduct
