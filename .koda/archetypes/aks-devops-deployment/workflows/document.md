---
description: Generate comprehensive documentation for AKS deployment architecture and operations
---

User input: $ARGUMENTS

## Execution Steps

### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Parse Documentation Request

Extract from $ARGUMENTS:
- Service name and framework
- Documentation type (architecture, runbook, operations, API)
- Target audience (developers, ops, security)
- Existing documentation to update

### 2. Generate Architecture Documentation

Create `docs/ARCHITECTURE.md`:
- System architecture diagram (C4 model)
- AKS cluster topology
- Network flow diagram
- Security boundaries
- Integration points

### 3. Generate Deployment Runbook

Create `docs/DEPLOYMENT-RUNBOOK.md`:
- Prerequisites checklist
- Step-by-step deployment procedure
- Configuration parameters
- Environment-specific values
- Verification steps

### 4. Generate Operations Guide

Create `docs/OPERATIONS-GUIDE.md`:
- Health check procedures
- Monitoring dashboards
- Alert response procedures
- Troubleshooting guide
- Rollback procedures

### 5. Generate Security Documentation

Create `docs/SECURITY.md`:
- Security controls implemented
- Compliance evidence mapping
- Secret management approach
- RBAC configuration
- Vulnerability scanning results

### 6. Generate API Documentation

Create `docs/API.md`:
- OpenAPI/Swagger specs
- Health endpoints
- Metrics endpoints
- Authentication requirements

### 7. Assemble Documentation Package

Output structure:
```
docs/
├── README.md           # Quick start guide
├── ARCHITECTURE.md     # System design
├── DEPLOYMENT-RUNBOOK.md
├── OPERATIONS-GUIDE.md
├── SECURITY.md
└── API.md
```

## Error Handling

**Missing Service Info**: Request service name, framework, and cluster details.

**Incomplete Config**: Generate templates with TODO placeholders for missing values.

**Existing Docs**: Offer to update existing documentation vs. replace.

## Examples

### Example 1: Full Documentation Package

```
/document-aks-devops-deployment "
Generate documentation for fraud-api Python service.
Cluster: Fml-EastUs2-Dev-AKS-Cluster
Target: ops team onboarding
"
```

### Example 2: Runbook Only

```
/document-aks-devops-deployment "
Create deployment runbook for user-service Node.js app.
Include staging and production procedures.
"
```

## References

- **Constitution**: `${ARCHETYPES_BASEDIR}/aks-devops-deployment/aks-devops-deployment-constitution.md`
- **Templates**: Constitution Section IX
- **Related**: scaffold-aks-devops-deployment, test-aks-devops-deployment
