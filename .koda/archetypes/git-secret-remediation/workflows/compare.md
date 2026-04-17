---
description: Compare different approaches for git secret remediation and GitHub alert resolution
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

### 3. Parse Comparison Request
Extract from $ARGUMENTS: Approaches to compare (e.g., git-filter-repo vs BFG Repo-Cleaner, local remediation vs GitHub alert dismissal)

### 4. Compare Remediation Approaches

#### Approach 1: git-filter-repo (Recommended)
**Pros:**
- Fine-grained control over history rewriting
- Supports complex regex patterns
- Active maintenance and community support
- Python-based, easy to install

**Cons:**
- Requires fresh clone for some operations
- Steeper learning curve than BFG
- Slower for very large repositories

**Best For:** Precise secret removal, complex patterns, standard repositories

#### Approach 2: BFG Repo-Cleaner
**Pros:**
- Faster for large repositories
- Simpler syntax
- Automatically protects latest commit
- Java-based, cross-platform

**Cons:**
- Less flexible than git-filter-repo
- Requires Java installation
- Cannot modify latest commit

**Best For:** Large repositories, simple secret removal, batch operations

#### Approach 3: Interactive Rebase (Local Only)
**Pros:**
- No additional tools required
- Complete control over each commit
- Can modify commit messages

**Cons:**
- Only works for local commits
- Time-consuming for many commits
- Risk of conflicts

**Best For:** Local commits only, small number of commits, learning purposes

#### Approach 4: GitHub Alert Dismissal (No History Rewrite)
**Pros:**
- Follows AT&T policy for pushed secrets
- No force-push required
- Simpler process
- Security Liaison oversight

**Cons:**
- Secret remains in git history
- Requires attestation and approval
- 3-day SLA for review
- Credential must be rotated

**Best For:** Secrets already pushed to remote, compliance with AT&T policy

### 5. Compare Attestation Types

#### Revoked Attestation (AT&T Owned)
**When to Use:** Secret was owned by AT&T and has been rotated
**Dismissal Reason:** Select "Revoked"
**Requirements:** 
- Proof of credential rotation
- Key Vault storage screenshot
- Secret removed from default branch
- Applies when validity is Active, Inactive, or Publicly leaked

**Approval Rate:** High (if properly documented)

#### Revoked Attestation (Non-AT&T Owned)
**When to Use:** Secret not owned by AT&T or its employees/contractors
**Dismissal Reason:** Select "Revoked" (NOT False Positive)
**Requirements:**
- Documentation proving AT&T doesn't own the credential
- Secret removed from default branch

**Approval Rate:** Medium (requires ownership proof)

#### False Positive Attestation
**When to Use:** Tool **misidentified** a value as a secret
**Dismissal Reason:** Select "False Positive"
**Valid Examples:**
- Key Vault names flagged as secrets
- System ID (SID) configuration parameters
- Intentionally public values (e.g., Google Maps public API keys)

**⚠️ NOT a False Positive:**
- A secret that exists in commit history but not in the default branch
- A secret used only in tests (still exposed!)

**Requirements:**
- Evidence it's not a secret
- Explanation of why scanner flagged it
- May require supporting documentation

**Approval Rate:** Medium (requires strong evidence)

### 5.1 Compare Request Types

#### Alert Dismissal
**When to Use:** Secret scanning alert needs to be closed
**Process:** Submit through GitHub Security tab
**SLA:** 3 business days (standard), 1 business day (escalated)

#### Bypass Request
**When to Use:** Push Protection blocked your push
**Process:** Submit through push protection alert
**Requirement:** Must verify flagged item is NOT a secret before requesting bypass

### 6. Compare Key Vault Options

#### Azure Key Vault
**Pros:**
- Integrated with Azure ecosystem
- Included with Azure subscription
- RBAC integration
- Managed service

**Cons:**
- Azure-specific
- Learning curve for non-Azure users

**Cost:** Included with Azure subscription

#### HashiCorp Vault
**Pros:**
- Multi-cloud support
- Advanced secret management features
- Industry standard

**Cons:**
- Requires licenses ($160/client annually)
- More complex setup
- Self-managed or enterprise version

**Cost:** $160/client/year (Test + Production)

### 7. Generate Comparison Report
Create detailed comparison with:
- Feature matrix
- Performance benchmarks
- Cost analysis
- Compliance considerations
- Recommendations based on scenario

### 8. Add Recommendations
Provide specific recommendations based on:
- Repository size
- Secret type
- Exposure scope (local vs pushed)
- Team size and coordination needs
- Compliance requirements

### 9. Validate and Report
Generate outputs and documentation. Report completion.

## Error Handling

**Common Issue**: Unclear comparison criteria
**Resolution**: Ask user to specify what aspects to compare (speed, ease of use, compliance, cost)

**Configuration Error**: Missing benchmark data
**Resolution**: Use general guidelines and recommend user testing

## Examples

**Example 1**: `/compare-git-secret-remediation "git-filter-repo vs BFG Repo-Cleaner"`
Output: Detailed comparison showing git-filter-repo is better for complex patterns, BFG is faster for large repos

**Example 2**: `/compare-git-secret-remediation "Azure Key Vault vs HashiCorp Vault"`
Output: Cost-benefit analysis showing Azure Key Vault is better for Azure-native apps

## References

Original: `vibe_cdo/git_secret_remediation/prompts/compare_prompt.md` | Constitution: (pre-loaded above)
