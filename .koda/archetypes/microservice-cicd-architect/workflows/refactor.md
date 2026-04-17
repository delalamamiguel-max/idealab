---
description: Refactor microservice CI/CD pipeline to apply security, progressive delivery, and observability patterns (Microservice CICD Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype microservice-cicd-architect --json ` and parse for CI_PLATFORM, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/microservice-cicd-architect/templates/env-config.yaml` for best practices

### 3. Parse Input
Extract from $ARGUMENTS: pipeline location, refactoring goals (security, progressive delivery, observability, compliance), specific issues (missing signing, no canary, poor monitoring). Request clarification if incomplete.

### 4. Analyze Current State

Assess pipeline: security posture (image signing, vulnerability scanning, SBOM, secret management), deployment safety (progressive delivery, automated rollback, approval gates), observability (deploy events, DORA metrics, dashboards), compliance (CAB references, RFC linkage, audit trails), supply chain security (reproducible builds, provenance attestation, pinned dependencies).

Identify gaps and risks.

### 5. Generate Refactoring Plan

Create improvements: Security Enhancements (add image signing with Cosign, implement vulnerability scanning, generate SBOM, add SLSA provenance, secure secret management), Progressive Delivery (implement canary or blue-green strategy, add automated rollback triggers, configure traffic controls, set up metric-based promotion), Observability Additions (structured deploy events, DORA metrics tracking, deployment dashboards, alert configurations), Compliance Strengthening (add CAB approval gates, create RFC linkage, implement change freeze checks, enhance audit logging).

### 6. Implement Refactorings

Generate refactored pipeline: updated stages with security scanning, progressive delivery configuration, enhanced observability, compliance gates, updated documentation.

Include migration guide with validation strategy.

### 7. Validate and Report


Generate refactoring report with security improvements, delivery enhancements, observability gains. Report completion.

## Error Handling

**Breaking Changes**: Provide phased rollout with backward compatibility.

**Tool Integration**: Provide setup instructions for new security tools.

**Compliance Requirements**: Coordinate with governance team for approval process.

## Examples

**Example 1**: `/refactor-microservice-cicd Add progressive delivery to existing pipeline` - Output: Enhanced pipeline with canary deployment

**Example 2**: `/refactor-microservice-cicd Implement supply chain security for microservice` - Output: Pipeline with signing, SBOM, and provenance

**Example 3**: `/refactor-microservice-cicd Add DORA metrics tracking to deployment pipeline` - Output: Observable pipeline with KPI dashboards

## References

