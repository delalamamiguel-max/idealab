---
description: Generate comprehensive documentation for microservice CI/CD pipeline with security and progressive delivery (Microservice CICD Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype microservice-cicd-architect --json ` and parse for CI_PLATFORM, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/microservice-cicd-architect/templates/env-config.yaml` for documentation templates

### 3. Parse Input
Extract from $ARGUMENTS: pipeline location, target audience (developers, operators, security, governance), documentation scope (architecture, operations, security, compliance). Request clarification if incomplete.

### 4. Analyze Pipeline Architecture

Extract pipeline information: stages and gates (build, security, deployment), progressive delivery configuration (canary/blue-green setup, rollback triggers), security controls (signing, scanning, SBOM, secret management), compliance integration (CAB approvals, RFC linkage), observability (deploy events, DORA metrics, dashboards).

### 5. Generate Documentation Package

Create comprehensive documentation suite: Pipeline Architecture (stage overview and dependencies, security gate definitions, progressive delivery flow, rollback mechanisms, compliance checkpoints), Developer Guide (local development setup, pipeline usage, code promotion workflow, security requirements, testing procedures, troubleshooting), Operations Runbook (deployment procedures for each environment, canary/blue-green management, rollback procedures, incident response, monitoring and alerting, performance tuning), Security Documentation (image signing process, vulnerability scanning thresholds, SBOM generation and verification, secret management practices, supply chain security, compliance requirements), Governance Documentation (CAB approval workflow, RFC linkage process, change freeze enforcement, audit logging, compliance evidence, DORA metrics tracking).

Include supporting artifacts: pipeline flow diagrams, progressive delivery visualizations, security tool configurations, runbook checklists, metric dashboards.

### 6. Add Recommendations

Include operational best practices: documentation maintenance, security review schedules, progressive delivery optimization, incident post-mortems, continuous improvement, team onboarding.

### 7. Validate and Report


Generate documentation artifacts organized in docs/ directory. Create index with navigation. Report completion.

## Error Handling

**Incomplete Information**: Request additional pipeline and security details.

**Missing Diagrams**: Generate flow diagrams from pipeline configuration.

**Outdated Metrics**: Update with current DORA KPIs.

## Examples

**Example 1**: `/document-microservice-cicd Create complete documentation for order-service pipeline` - Output: Architecture docs, operations runbook, security documentation

**Example 2**: `/document-microservice-cicd Generate progressive delivery guide for payment-api` - Output: Canary deployment documentation with rollback procedures

**Example 3**: `/document-microservice-cicd Document security and compliance for production pipeline` - Output: Security guide with CAB workflow and audit requirements

## References

