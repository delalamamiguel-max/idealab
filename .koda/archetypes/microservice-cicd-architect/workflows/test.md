---
description: Validate microservice CI/CD pipeline for security, progressive delivery, and governance readiness (Microservice CICD Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype microservice-cicd-architect --json ` and parse for CI_PLATFORM, PYTEST_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/microservice-cicd-architect/templates/env-config.yaml` for test specifications

### 3. Parse Input
Extract from $ARGUMENTS: pipeline location, test scope (unit, integration, security, progressive delivery, compliance), acceptance criteria, target environment. Request clarification if incomplete.

### 4. Analyze Test Requirements

Identify testable components: pipeline stages (build, security, deployment), progressive delivery (canary/blue-green configuration, automated rollback, traffic controls), security controls (image signing, vulnerability scanning, SBOM generation, secret management), compliance gates (CAB approval, RFC linkage, audit logging), observability (deploy events, DORA metrics, dashboards).

Define test scenarios: unit tests (pipeline configuration validation, script logic, policy enforcement), integration tests (end-to-end pipeline execution, progressive delivery flow, rollback validation), security tests (signing verification, vulnerability gate enforcement, secret scanning), compliance tests (approval workflow validation, RFC linkage, audit trail verification), performance tests (deployment speed, rollback time, DORA metrics).

### 5. Generate Test Suite

Create comprehensive test suite with unit tests (pipeline YAML validation, security tool configuration, canary policy tests), integration tests (full deployment workflow, canary progression tests, automated rollback validation), security tests (image signature validation, vulnerability threshold enforcement, SBOM completeness), compliance tests (CAB approval gate tests, RFC linkage validation, audit log verification), performance tests (deployment frequency tracking, MTTR validation, change failure rate monitoring).

Include test fixtures, mock services, test environments.

### 6. Add Recommendations

Include testing best practices: automated pipeline testing, security validation in PR, progressive delivery dry runs, continuous compliance monitoring, DORA metrics tracking.

Provide test execution commands.

### 7. Validate and Report


Execute test suite: `pytest tests/ --junitxml=results.xml --cov --cov-report=html`

Generate test report with pass/fail summary, security validation, progressive delivery readiness, DORA metrics. Report completion.

## Error Handling

**Test Environment Missing**: Provide setup instructions for test infrastructure.

**Security Tools Unavailable**: Use mock scanners or provide integration guidance.

**Compliance Workflow Undefined**: Create test approval process.

## Examples

**Example 1**: `/test-microservice-cicd Validate canary deployment pipeline for order-service` - Output: Complete test suite with progressive delivery validation

**Example 2**: `/test-microservice-cicd Test security gates for payment-api pipeline` - Output: Security validation suite with signing and scanning tests

**Example 3**: `/test-microservice-cicd Validate compliance for production deployment pipeline` - Output: Compliance test suite with CAB and RFC validation

## References

