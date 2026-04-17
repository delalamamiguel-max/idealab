---
description: Refactor secret management practices to prevent future git secret exposures
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

### 3. Parse Refactoring Scope
Extract from $ARGUMENTS: Areas to refactor (e.g., configuration management, secret storage, CI/CD pipeline, developer workflows)

### 4. Audit Current Secret Management

#### Scan for Hardcoded Secrets
```bash
# Search for common secret patterns
git grep -i "password\s*=\s*['\"]"
git grep -i "api[_-]key\s*=\s*['\"]"
git grep -i "secret\s*=\s*['\"]"
git grep -i "token\s*=\s*['\"]"
git grep -i "connectionstring\s*=\s*['\"]"
```

#### Identify Secret Files
```bash
# Find potential secret files
find . -name "*.env" -o -name "*.pem" -o -name "*.key" -o -name "credentials.json"
```

#### Check .gitignore Coverage
```bash
# Verify secret files are ignored
cat .gitignore | grep -E "\\.env|\\.pem|\\.key|credentials"
```

### 5. Refactor Configuration Management

#### Before (Hardcoded):
```python
# ❌ Bad - Hardcoded secret
DATABASE_URL = "postgresql://user:MyPassword123@host/db"
API_KEY = "sk-1234567890abcdef"
```

#### After (Environment Variables):
```python
# ✅ Better - Environment variable
import os
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
```

#### After (Key Vault):
```python
# ✅ Best - Azure Key Vault
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://my-vault.vault.azure.net/", credential=credential)
DATABASE_URL = client.get_secret("database-url").value
API_KEY = client.get_secret("api-key").value
```

### 6. Refactor .gitignore

Add comprehensive secret file patterns:
```gitignore
# Environment files
.env
.env.local
.env.*.local
*.env

# Configuration with secrets
config/secrets.yaml
config/database.yml
**/appsettings.Development.json
**/appsettings.*.json

# Key files
*.pem
*.key
*.p12
*.pfx
*.cer
*.crt
id_rsa
id_dsa

# Credential files
credentials.json
service-account.json
*-credentials.json
auth.json

# Cloud provider configs
.aws/credentials
.azure/credentials
gcloud-service-key.json
```

### 7. Refactor CI/CD Pipeline

#### Add Secret Scanning
```yaml
# GitHub Actions example
name: Security Scan
on: [push, pull_request]
jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run secret detection
        uses: Yelp/detect-secrets-action@v0.1.0
```

#### Use Secure Secret Injection
```yaml
# Use GitHub Secrets instead of hardcoding
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}
```

### 8. Refactor Developer Workflow

#### Install Pre-Commit Hooks
```bash
# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        exclude: package-lock.json
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: detect-private-key
EOF

# Install and setup
pip install pre-commit
pre-commit install
detect-secrets scan > .secrets.baseline
```

#### Enable GitHub Push Protection
1. Go to repository **Settings** → **Security**
2. Enable **Push protection** for secret scanning
3. Configure custom patterns if needed

### 9. Refactor Key Vault Integration

#### Create Centralized Secret Manager
```python
# secret_manager.py
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from functools import lru_cache

class SecretManager:
    def __init__(self, vault_url: str):
        self.client = SecretClient(
            vault_url=vault_url,
            credential=DefaultAzureCredential()
        )
    
    @lru_cache(maxsize=128)
    def get_secret(self, name: str) -> str:
        """Get secret from Key Vault with caching"""
        return self.client.get_secret(name).value
    
    def set_secret(self, name: str, value: str):
        """Set secret in Key Vault"""
        self.client.set_secret(name, value)

# Usage
secrets = SecretManager("https://my-vault.vault.azure.net/")
db_password = secrets.get_secret("database-password")
```

### 10. Refactor Documentation

Update team documentation with:
- Secret management best practices
- Key Vault usage guide
- Pre-commit hook setup instructions
- Incident response procedures
- AT&T attestation requirements

### 11. Generate Refactoring Report

Document all changes made:
- Files modified
- Secrets migrated to Key Vault
- .gitignore patterns added
- CI/CD pipeline updates
- Pre-commit hooks installed
- Team training completed

### 12. Validate and Report
Generate outputs and documentation. Report completion.

## Error Handling

**Common Issue**: Breaking changes to application configuration
**Resolution**: Test thoroughly in dev environment before production deployment

**Configuration Error**: Key Vault access denied
**Resolution**: Request proper RBAC roles from Azure admin

## Examples

**Example 1**: `/refactor-git-secret-remediation "Migrate all hardcoded secrets to Azure Key Vault"`
Output: Refactored code with Key Vault integration and updated configuration

**Example 2**: `/refactor-git-secret-remediation "Add pre-commit hooks for secret detection"`
Output: .pre-commit-config.yaml created, hooks installed, baseline generated

## References

Original: `vibe_cdo/git_secret_remediation/prompts/refactor_prompt.md` | Constitution: (pre-loaded above)
