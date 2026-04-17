# Constitution: Git Secret Remediation

## Purpose
Ensure the complete and compliant remediation of exposed secrets from git history, resolution of GitHub Security Alerts, and prevention of future secret exposures in accordance with AT&T's Secret Remediation Policy (Effective August 11, 2025).

---

### I. Hard-Stop Rules (Non-Negotiable)
The LLM **must refuse** or correct any action that violates these rules:

✘ No modification of commit history for secrets already pushed to remote without Security Liaison approval  
✘ No force-push without team coordination and explicit approval  
✘ No dismissal of GitHub Security Alerts without exact AT&T attestation text (verbatim copy required)  
✘ No paraphrasing or modification of attestation text (automatic rejection)  
✘ No credential rotation without storing new credential in Key Vault (Azure or HashiCorp)  
✘ No secret removal without verification across all branches, tags, and commit history  
✘ No hardcoded secrets in code after remediation (must use Key Vault references)  
✘ No deployment of code containing exposed secrets

---

### II. Mandatory Patterns (Must Apply)
The LLM **must insert** or verify these patterns:

✔ Create backup branch before any history rewriting operation  
✔ Use git-filter-repo for precise secret removal (not git filter-branch)  
✔ Verify secret removal with `git log --all --full-history -S"pattern"` and `git grep`  
✔ Store all secrets in Azure Key Vault or HashiCorp Vault (never in code)  
✔ Revoke and rotate exposed credentials immediately  
✔ Update application code to retrieve secrets from Key Vault  
✔ Copy exact AT&T attestation text when dismissing GitHub Security Alerts:
  - Revoked: "Submitter confirms the secret has been remediated per AT&T policy and poses no risk. Falsification of this attestation violates AT&T's Code of Business Conduct and may result in disciplinary action."
  - False Positive: "Submitter confirms the alert is a false positive and poses no risk. Falsification of this attestation violates AT&T's Code of Business Conduct and may result in disciplinary action."
  - Non-AT&T: "The submitter affirms that the secret is neither owned by AT&T nor by its employees or contractors, has been removed from the default branch. Falsification of this attestation violates AT&T's Code of Business Conduct and may result in disciplinary action."  
✔ Provide supporting documentation for alert dismissals (Key Vault screenshots, rotation proof)  
✔ Wait for Security Liaison approval (3 business day SLA, 1 day escalated)  
✔ Document all remediation actions for compliance and audit trail

---

### III. Preferred Patterns (Recommended)
The LLM **should adopt** these patterns unless user overrides:

➜ Install pre-commit hooks (detect-secrets) to prevent future exposures  
➜ Enable GitHub Push Protection for secret scanning  
➜ Add comprehensive .gitignore patterns for secret files (.env, *.pem, *.key, credentials.json)  
➜ Use visual Git tools instead of `git add .` or `git add -A`  
➜ Implement CI/CD pipeline secret scanning  
➜ Conduct post-incident review to identify root cause and process gaps  
➜ Update team training on secret management best practices  
➜ Use Azure Key Vault for Azure-native applications (included with subscription)  
➜ Consider HashiCorp Vault for multi-cloud environments (requires $160/client annual license)  
➜ Create incident documentation for security compliance and knowledge management  
➜ Test remediation completeness with validation scripts  
➜ Coordinate with all team members before force-pushing  
➜ Notify team members to re-sync repositories after force-push

---

### IV. AT&T Policy Compliance (Mandatory)
The LLM **must enforce** these AT&T-specific requirements:

🔴 **Attestation Requirement (Effective Aug 11, 2025)**  
- Exact attestation text must be copied verbatim (no modifications allowed)
- Failure to provide exact text results in automatic rejection
- Three attestation types: Revoked, False Positive, Non-AT&T
- Each attestation includes Code of Business Conduct warning

🔴 **Security Liaison Review**  
- All pushed secret remediations require Security Liaison approval
- Standard SLA: 3 US business days
- Escalated SLA: 1 business day (requires proper escalation)
- Rejections must be addressed and resubmitted

🔴 **Supporting Documentation**  
- Upload to MDP-Security Alert Response Document Tracker
- Include Key Vault storage screenshots for revoked secrets
- Provide proof of credential rotation
- Document ownership for non-AT&T secrets
- Evidence for false positive claims

🔴 **Credential Management**  
- Store all secrets in Azure Key Vault or HashiCorp Vault
- Never store secrets in code, config files, or environment files in git
- Rotate exposed credentials immediately
- Verify old credentials are revoked and no longer functional

---

### V. Technical Requirements
The LLM **must verify** these technical constraints:

⚙️ **Git History Rewriting**  
- Use git-filter-repo (not deprecated git filter-branch)
- Create backup branch with timestamp before rewriting
- Verify removal across all branches and tags
- Test with dry-run before executing
- Handle URL-encoded and escaped secret variations

⚙️ **GitHub Security Alert Resolution**  
- Navigate to Security → Secret scanning → Alert
- Select correct dismissal reason (Revoked or False Positive)
- Paste exact attestation in comment field
- Attach supporting documentation
- Submit and wait for Security Liaison review

⚙️ **Key Vault Integration**  
- Azure Key Vault: Use DefaultAzureCredential for authentication
- HashiCorp Vault: Follow onboarding process and obtain licenses
- Update application code to retrieve secrets at runtime
- Use caching for performance (e.g., @lru_cache)
- Handle Key Vault access errors gracefully

⚙️ **Preventive Measures**  
- Install detect-secrets pre-commit hook
- Create .secrets.baseline file
- Enable GitHub Push Protection
- Add .gitignore patterns for secret files
- Implement CI/CD secret scanning

---

### VI. Error Handling
The LLM **must handle** these common error scenarios:

🔧 **git-filter-repo Errors**  
- "requires a fresh clone": Add temporary remote or clone fresh
- "not a git repository": Verify working directory
- "invalid replacement pattern": Fix syntax (literal: or regex:)

🔧 **GitHub Alert Rejection**  
- "Invalid attestation": Copy exact text again (most common cause)
- "Insufficient documentation": Provide additional evidence
- "Secret still active": Verify credential was actually rotated
- Resubmit with corrections after addressing feedback

🔧 **Force-Push Failures**  
- "refusing to force push": Check branch protection settings
- "insufficient permissions": Request admin access
- "remote repository locked": Contact repository owner

🔧 **Key Vault Access Errors**  
- "Access denied": Request "Key Vault Secrets User" RBAC role
- "Vault not found": Verify vault name and subscription
- "Authentication failed": Check Azure credentials and identity

---

## Enhanced Archetype Patterns (v1.2.0)

### A. Test Isolation (CRITICAL SAFETY)

**Hard-Stop Rule:** Never test secret remediation on production repositories.

**Test Environment Requirements:**
1. Create disposable test repo in `/tmp/` or test directory
2. Validate environment before executing remediation
3. Use fake secrets only (e.g., `FAKE_SECRET_12345`)
4. Cleanup test repo after validation
5. Fail fast if production repo detected

**See:** `test-git-secret-remediation.md` Step 2 for full test isolation protocol.

### B. Simulation Testing

**Simulation validates remediation effectiveness:**
1. Generate test repo with fake secrets
2. Execute full remediation workflow
3. Verify secret removal completeness
4. Check Key Vault integration
5. Validate no production impact
6. Document findings and iterate

**See:** `test-git-secret-remediation.md` Phase 2 for simulation protocol.

### C. Orchestration (Test Infrastructure)

**Pattern:** Delegate test repo generation to automation-scripter.

```bash
/scaffold-automation "Create Python class TestRepoGenerator that:
- Creates temporary git repo in /tmp/
- Adds commits with fake secrets
- Provides cleanup function
- Returns repo path for testing"
```

**Benefits:**
- ✅ Test infrastructure follows best practices
- ✅ Safety checks prevent production damage
- ✅ Reusable across all tests

**See:** `scaffold-git-secret-remediation.md` Orchestration section.

---

Version: 1.1.0  
Last Updated: 2025-08-12  
Policy Effective Date: August 11, 2025  
Compliance: AT&T Code of Business Conduct
