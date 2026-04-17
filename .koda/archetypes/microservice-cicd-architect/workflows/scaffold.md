---
description: Generate microservice CI/CD pipeline with progressive delivery, security scanning, and governance (Microservice CICD Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype microservice-cicd-architect --json ` and parse for CI_PLATFORM, CONTAINER_REGISTRY, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/microservice-cicd-architect/templates/env-config.yaml` for configuration

### 3. Parse Input
Extract from $ARGUMENTS: service name and type, programming language, deployment target (Kubernetes, cloud platform), progressive delivery strategy (canary, blue-green), security requirements, observability needs. Request clarification if incomplete.

### 4. Generate CI/CD Pipeline

Create comprehensive pipeline: Build Stage (compile and package, run unit tests, static code analysis, dependency vulnerability scanning, SBOM generation, reproducible builds with pinned dependencies), Security Stage (container image signing with Cosign, vulnerability scanning (Trivy/Snyk), license compliance checks, SLSA provenance attestation, secret scanning), Artifact Stage (container image build with digest pinning, artifact signing and verification, push to registry with tags, metadata and manifest generation), Deployment Stages (dev deployment with smoke tests, staging deployment with integration tests, canary/blue-green to production, automated rollback triggers, traffic shift controls), Governance Gates (production approval workflow, CAB reference and RFC linkage, change freeze enforcement, P1/P0 incident checks, compliance validation).

### 5. Generate Progressive Delivery Configuration

Implement deployment strategy: canary configuration (traffic splitting rules, metrics monitoring, automated promotion/rollback), blue-green setup (environment switching, validation gates, traffic cutover), observability integration (structured deploy events, DORA metrics tracking, deployment dashboards, alert configurations).

### 6. Add Recommendations

Include best practices: GitOps implementation, automated testing strategies, monitoring and alerting setup, incident response procedures, continuous security scanning, cost optimization, documentation and runbooks.

### 7. Validate and Report


Generate complete CI/CD pipeline with documentation. Report completion.

## Error Handling

**Missing Security Tools**: Provide integration instructions for scanning and signing.

**Approval Workflow Undefined**: Create CAB reference template and RFC process.

**Progressive Delivery Not Configured**: Set up canary or blue-green with metrics.

## Examples

**Example 1**: `/scaffold-microservice-cicd Create pipeline for order-service with canary deployment` - Output: Complete CI/CD with security scanning and canary strategy

**Example 2**: `/scaffold-microservice-cicd Generate blue-green deployment for payment-api` - Output: Pipeline with blue-green delivery and automated rollback

**Example 3**: `/scaffold-microservice-cicd Build pipeline with SLSA provenance and SBOM` - Output: Secure pipeline with supply chain attestation

## References

