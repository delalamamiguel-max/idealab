---
description: Compare Terraform CI/CD strategies, policy engines, and state management approaches (Terraform CICD Architect)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Context Note

The archetype constitution and workflow have been pre-loaded by CodeForge. All hard-stop rules and mandatory patterns from the constitution are active. Proceed directly to the execution steps below.

### 1. Environment Setup
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype terraform-cicd-architect --json ` and parse for TERRAFORM_VERSION, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- The constitution rules are already loaded in context above.
- Load `${ARCHETYPES_BASEDIR}/terraform-cicd-architect/templates/env-config.yaml` for comparison framework

### 3. Parse Input
Extract from $ARGUMENTS: comparison type (policy engines, state backends, CI platforms, workflow strategies), candidate options, evaluation criteria (security, cost, complexity, governance). Request clarification if incomplete.

### 4. Generate Comparison Framework

Based on comparison type, evaluate: Policy Engines (Sentinel vs OPA vs Checkov vs tfsec - policy language, integration, coverage, cost), State Backends (S3 vs Azure Storage vs Terraform Cloud vs GCS - locking, encryption, cost, features), CI/CD Platforms (GitHub Actions vs GitLab CI vs Azure DevOps vs Atlantis - automation, approval workflows, cost), Workflow Strategies (GitOps vs traditional CI/CD vs hybrid - governance, auditability, developer experience).

### 5. Create Comparison Matrix

Generate detailed comparison with quantitative metrics (cost analysis, policy coverage, state operations performance), qualitative assessments (complexity, learning curve, vendor lock-in, enterprise features), trade-off analysis, use case recommendations.

Include governance and compliance fit analysis.

### 6. Add Recommendations

Recommend approach with comprehensive justification: security requirements alignment, governance needs, team capabilities, cost-benefit analysis, migration complexity, long-term strategy.

Provide implementation roadmap and adoption plan.

### 7. Validate and Report


Generate comparison report with decision matrix, recommendations, implementation guidance. Report completion.

## Error Handling

**Insufficient Context**: Request governance and compliance requirements.

**Unclear Requirements**: Facilitate requirements gathering on infrastructure needs.

**Cost Uncertainty**: Provide pricing models and TCO projections.

## Examples

**Example 1**: `/compare-terraform-cicd Sentinel vs OPA for Terraform policy enforcement` - Output: Policy engine comparison with governance analysis

**Example 2**: `/compare-terraform-cicd S3 vs Terraform Cloud for state management` - Output: Backend comparison with cost and feature assessment

**Example 3**: `/compare-terraform-cicd GitOps vs traditional CI/CD for infrastructure deployment` - Output: Workflow strategy comparison with governance trade-offs

## References

