---
description: Compare microservice CI/CD strategies, progressive delivery patterns, and security approaches (Microservice CICD Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype microservice-cicd-architect --json ` and parse for CI_PLATFORM, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/microservice-cicd-architect/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type (delivery strategies, CI platforms, security tools, observability solutions), candidate options, evaluation criteria (safety, speed, cost, complexity). Request clarification if incomplete.

### 4. Generate Comparison Framework

Based on comparison type, evaluate: Progressive Delivery Strategies (canary vs blue-green vs shadow vs rolling - risk mitigation, speed, complexity, resource usage), CI/CD Platforms (GitHub Actions vs GitLab CI vs Azure DevOps vs Jenkins - features, cost, integration, enterprise capabilities), Security Scanning Tools (Trivy vs Snyk vs Aqua vs Prisma - coverage, accuracy, cost, integration), Image Signing Solutions (Cosign vs Notary vs Docker Content Trust - adoption, integration, verification speed).

### 5. Create Comparison Matrix

Generate detailed comparison with quantitative metrics (deployment frequency impact, MTTR comparison, cost analysis, DORA metrics capability), qualitative assessments (complexity, team learning curve, vendor lock-in), trade-off analysis, use case recommendations.

Include progressive delivery risk analysis.

### 6. Add Recommendations

Recommend approach with comprehensive justification: safety requirements alignment, deployment frequency goals, team capabilities, cost-benefit analysis, migration path, compliance fit.

Provide implementation roadmap.

### 7. Validate and Report


Generate comparison report with decision matrix, recommendations. Report completion.

## Error Handling

**Insufficient Metrics**: Request current deployment KPIs and failure rates.

**Unclear Requirements**: Facilitate requirements gathering on safety vs speed.

**Cost Uncertainty**: Provide TCO models for each option.

## Examples

**Example 1**: `/compare-microservice-cicd Canary vs blue-green deployment for high-traffic service` - Output: Strategy comparison with risk and performance analysis

**Example 2**: `/compare-microservice-cicd GitHub Actions vs Azure DevOps for microservice CI/CD` - Output: Platform comparison with integration and cost assessment

**Example 3**: `/compare-microservice-cicd Trivy vs Snyk for container security scanning` - Output: Tool comparison with coverage and accuracy analysis

## References

