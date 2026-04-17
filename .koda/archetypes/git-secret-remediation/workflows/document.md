---
description: Document git secret remediation incident for compliance and post-mortem analysis
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

### 3. Parse Incident Information
Extract from $ARGUMENTS:
- **Secret type**: Database password, API key, OAuth token, etc.
- **Discovery method**: GitHub Security Alert, manual review, automated scan
- **Exposure duration**: When secret was committed vs when discovered
- **Remediation actions**: Steps taken to resolve
- **GitHub alert status**: Dismissed, approved, rejected

### 4. Generate Incident Report

Create comprehensive documentation including:

#### Executive Summary
- **Incident ID**: GIT-SECRET-[YYYY-MM-DD]-[REPO]
- **Severity**: Critical (exposed credential)
- **Status**: Resolved / Pending Review
- **Discovery Date**: [Date]
- **Resolution Date**: [Date]

#### Incident Details
- **Repository**: [Org/Repo Name]
- **Branch**: [Branch Name]
- **Commit Hash**: [Hash where secret was introduced]
- **Secret Type**: [Database password / API key / etc.]
- **Exposure Scope**: [Local only / Pushed to remote / Public]

#### Timeline
1. **[Date/Time]**: Secret committed to repository
2. **[Date/Time]**: Secret pushed to remote (if applicable)
3. **[Date/Time]**: GitHub Security Alert triggered
4. **[Date/Time]**: Incident discovered by [Person/System]
5. **[Date/Time]**: Remediation initiated
6. **[Date/Time]**: Secret removed from history
7. **[Date/Time]**: Credential revoked and rotated
8. **[Date/Time]**: GitHub alert dismissed
9. **[Date/Time]**: Security Liaison approved (if applicable)
10. **[Date/Time]**: Incident closed

#### Remediation Actions Taken
- [ ] Secret removed from git history using git-filter-repo
- [ ] Backup branch created: [Branch Name]
- [ ] Exposed credential revoked
- [ ] New credential generated and stored in Key Vault
- [ ] Application code updated to use Key Vault reference
- [ ] GitHub Security Alert dismissed with attestation
- [ ] Security Liaison approval received (if required)
- [ ] Team members notified and repositories re-synced
- [ ] Force-push completed (if applicable)

#### Root Cause Analysis
**Primary Cause**: [e.g., Hardcoded credential in configuration file]

**Contributing Factors**:
- Lack of pre-commit hooks for secret detection
- No code review before commit
- Developer unfamiliar with Key Vault usage
- Insufficient security training

**Why it wasn't caught earlier**:
- Pre-commit hooks not installed
- GitHub Push Protection not enabled
- Manual code review didn't catch it

#### Impact Assessment
- **Credential Exposure**: [Duration exposed]
- **Access Risk**: [High/Medium/Low - based on credential privileges]
- **Data at Risk**: [What systems/data the credential could access]
- **Actual Unauthorized Access**: [None detected / Under investigation]
- **Business Impact**: [Deployment delay / No impact / etc.]

#### Attestation Used
[Copy the exact attestation that was submitted to GitHub]

**Attestation Type**: 
- [ ] Revoked (AT&T owned secret, rotated and stored in Key Vault)
- [ ] Revoked with Non-AT&T Attestation (secret not owned by AT&T)
- [ ] False Positive (tool misidentified value - NOT a secret in history but not in default branch)

**Request Type**:
- [ ] Alert Dismissal (secret scanning alert)
- [ ] Bypass Request (push protection block)

**Supporting Documentation Provided**:
- Key Vault storage screenshot
- Credential rotation proof
- Ownership documentation (for Non-AT&T secrets)
- Evidence of false positive (for misidentified values)
- [Other documentation]

#### Security Liaison Review
- **Liaison Name**: [Name]
- **Review Date**: [Date]
- **Decision**: Approved / Rejected / Pending
- **SLA Met**: Yes / No (Standard: 3 business days, Escalated: 1 business day)
- **Feedback**: [Any comments from Security Liaison]

#### If Rejected - Follow-up Actions
**Rejection Reason**: [From Security Liaison feedback]

**Common Rejection Reasons:**
- [ ] Attestation missing or modified
- [ ] Invalid dismissal reason ("Used in tests" or "Won't fix")
- [ ] Secret still active (validity tools detected it works)
- [ ] Insufficient supporting documentation
- [ ] Misused False Positive (secret exists in history, not a tool misidentification)

**Follow-up Actions Taken:**
- [ ] Uploaded additional documentation to MDP-Security Alert Response Document Tracker
- [ ] Verified credential was actually rotated
- [ ] Copied attestation exactly (not paraphrased)
- [ ] Resubmitted dismissal request
- [ ] Contacted Security Liaison directly for clarification

### 5. Document Preventive Measures

#### Immediate Actions (Completed)
- [ ] Pre-commit hooks installed (detect-secrets)
- [ ] GitHub Push Protection enabled
- [ ] .gitignore updated with secret file patterns
- [ ] Team training scheduled

#### Long-term Improvements
- [ ] Mandatory Key Vault usage for all credentials
- [ ] Automated secret scanning in CI/CD pipeline
- [ ] Quarterly security training for developers
- [ ] Code review checklist updated with secret detection
- [ ] Incident response playbook updated

### 6. Generate Compliance Artifacts

Create required documentation for:
- **Security Liaison**: Incident summary and resolution proof
- **Audit Trail**: Complete timeline and actions taken
- **Team Knowledge Base**: Lessons learned and prevention guide
- **Management Report**: Executive summary and business impact

### 7. Add Recommendations

Include best practices for future prevention:
- Use Azure Key Vault or HashiCorp Vault for all secrets
- Enable GitHub Push Protection
- Install pre-commit hooks on all developer machines
- Conduct regular security training
- Implement automated secret scanning in CI/CD
- Use visual Git tools instead of `git add .`
- Review code before committing

### 8. Validate and Report
Generate outputs and documentation. Report completion.

## Error Handling

**Common Issue**: Incomplete incident information
**Resolution**: Interview team members, review GitHub history, check Security Liaison communications

**Configuration Error**: Missing access to MDP-Security Alert Response Document Tracker
**Resolution**: Contact Security Liaison for access

## Examples

**Example 1**: `/document-git-secret-remediation "Database password exposed in config.py"`
Output: Complete incident report with timeline, remediation actions, and preventive measures

**Example 2**: `/document-git-secret-remediation "API key in commit history, GitHub alert dismissed"`
Output: Compliance documentation package for Security Liaison review

## References

Original: `vibe_cdo/git_secret_remediation/prompts/document_prompt.md` | Constitution: (pre-loaded above)
