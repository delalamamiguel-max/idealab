---
description: Debug microservice CI/CD pipeline failures, deployment issues, and security gate violations (Microservice CICD Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype microservice-cicd-architect --json ` and parse for CI_PLATFORM, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/microservice-cicd-architect/templates/env-config.yaml` for debugging tools

### 3. Parse Input
Extract from $ARGUMENTS: failure type (build failure, security gate, deployment failure, rollback needed), error messages, pipeline ID, service name, environment. Request clarification if incomplete.

### 4. Diagnose Issue

Run diagnostic checks: Build Failures (compile errors, test failures, dependency issues), Security Gate Violations (vulnerability scan failures, unsigned images, SBOM issues, secret exposure), Deployment Failures (canary metrics breach, rollout timeout, health check failures, traffic shift issues), Progressive Delivery Issues (automated rollback triggers, traffic routing problems, metric threshold breaches), Compliance Violations (missing CAB approval, RFC linkage missing, change freeze violation).

Provide diagnostic report with root cause.

### 5. Generate Fix Recommendations

Provide targeted fixes: for build issues (fix dependencies, resolve test failures, update configurations), for security violations (remediate vulnerabilities, implement signing, fix secrets management), for deployment failures (adjust health checks, fix canary metrics, update rollout configuration), for compliance (add CAB references, create RFC linkage, document exceptions).

Include configuration fixes and code changes.

### 6. Add Prevention Measures

Recommend improvements: enhanced pre-merge validation, improved security scanning, better canary metrics, automated compliance checks, proactive monitoring.

### 7. Validate and Report


Generate debug report with analysis, fixes, prevention measures. Report completion.

## Error Handling

**Insufficient Logs**: Enable debug logging and collect pipeline artifacts.

**Multiple Failures**: Prioritize critical path and provide sequenced fixes.

**Security Block**: Coordinate with security team for exception process.

## Examples

**Example 1**: `/debug-microservice-cicd Canary deployment failed metrics threshold` - Output: Metrics analysis with threshold adjustments

**Example 2**: `/debug-microservice-cicd Security scan blocking release with high CVEs` - Output: Vulnerability remediation plan

**Example 3**: `/debug-microservice-cicd Missing CAB approval blocking production deploy` - Output: Compliance workflow with RFC template

## References

