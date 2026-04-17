---
description: Compare security postures, compliance frameworks, and guardrail implementations across projects or approaches (Security Guardian)
---

User input: $ARGUMENTS

## Execution Steps


### 0. Set ARCHETYPES_BASEDIR [⋯]
 
**SUCCESS CRITERIA**:
- Search for directory: "00-core-orchestration"
- Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory
 
**HALT IF**:
- Directory "00-core-orchestration" is not found
- `${ARCHETYPES_BASEDIR}` is not set (workflow will halt if this variable is not present in the environment)
 
// turbo
Search for directory: "00-core-orchestration". Set variable `${ARCHETYPES_BASEDIR}` to immediate parent of this directory. Workflow must halt if the variable is not set.

### 1. Environment Setup
// turbo
Run `python ${ARCHETYPES_BASEDIR}/00-core-orchestration/scripts/validate_env.py --archetype security-guardian --json ` and parse for CI_TOOL, ORCHESTRATOR, ENV_VALID. Halt if ENV_VALID is false.

### 2. Load Configuration
- Read `${ARCHETYPES_BASEDIR}/security-guardian/security-guardian-constitution.md` for hard-stop rules
- Load `${ARCHETYPES_BASEDIR}/security-guardian/templates/` for comparison frameworks

### 3. Parse Input
Extract from $ARGUMENTS: comparison type (compliance frameworks, security tooling, SDLC gate strategies, risk management approaches), candidate options, evaluation criteria (coverage, enforcement strength, developer friction, audit readiness), organizational context. Request clarification if incomplete.

### 4. Generate Comparison Framework

Based on comparison type, evaluate: Compliance Frameworks (SOC2 vs ISO 27001 vs NIST 800-53 vs PCI-DSS - control coverage, audit effort, industry alignment, implementation cost), Security Tooling (SAST vs DAST vs SCA vs IAST - detection accuracy, CI/CD integration, false positive rate, remediation guidance), SDLC Gate Strategies (shift-left vs gate-based vs continuous - developer velocity impact, defect escape rate, feedback loop speed, governance fit), Risk Management (quantitative vs qualitative vs hybrid - precision, stakeholder buy-in, resource requirements, decision quality).

### 5. Create Comparison Matrix

Generate detailed comparison with guardrail effectiveness per option, compliance coverage mapping, developer experience impact assessment, cost-benefit analysis, risk reduction quantification, integration complexity with existing toolchain.

Include maturity model alignment for each option.

### 6. Add Recommendations

Recommend approach with security guardian justification: risk reduction effectiveness, compliance gap closure, implementation feasibility, organizational readiness assessment, phased adoption roadmap.

Provide migration strategy and success metrics.

### 7. Validate and Report

// turbo

Generate comparison report with security-focused decision matrix and adoption recommendations. Report completion.

## Error Handling

**Unclear Risk Profile**: Request organizational risk assessment and threat landscape.

**Non-Comparable Approaches**: Identify common evaluation dimensions and reframe.

**Regulatory Constraints**: Highlight mandatory requirements and evaluate compliance paths.

## Examples

**Example 1**: `/compare-security-guardian SOC2 Type II vs ISO 27001 for SaaS platform` - Output: Framework comparison with implementation roadmap

**Example 2**: `/compare-security-guardian Shift-left vs gate-based security for CI/CD pipeline` - Output: Strategy comparison with developer velocity analysis

**Example 3**: `/compare-security-guardian Snyk vs Dependabot vs Renovate for dependency security` - Output: Tool comparison with coverage and integration analysis

## References

