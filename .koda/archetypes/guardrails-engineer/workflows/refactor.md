---
description: Refactor existing guardrails configuration for improved security, performance, or coverage (Guardrails Engineer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Environment Setup

// turbo
Verify guardrails dependencies are available:
- deepeval
- presidio-analyzer
- presidio-anonymizer

### 2. Load Configuration

- Read `guardrails-engineer-constitution.md` for hard-stop rules
- Load existing guardrails configuration from specified path

### 3. Parse Input

Extract from $ARGUMENTS:
- **Config path**: Path to existing guardrails configuration
- **Refactoring goal**: security/performance/coverage/compliance
- **Specific concerns**: Optional specific issues to address
- **Target metrics**: Desired latency, accuracy, or coverage targets

If incomplete, request:
```
Please provide:
1. Config Path: (e.g., "guardrails config file")
2. Refactoring Goal: security | performance | coverage | compliance
3. Specific Concerns: (optional, e.g., "too many false positives")
4. Target Metrics: (optional, e.g., "latency < 200ms")
```

### 4. Analyze Current Configuration

**4.1. Security Analysis**
- Check if all required guardrails are enabled for agent level
- Verify thresholds meet minimum security requirements
- Identify missing guardrail types
- Check for hardcoded bypass patterns

**4.2. Performance Analysis**
- Measure current guardrail latency
- Identify expensive operations (LLM calls vs regex)
- Check for unnecessary sequential evaluations
- Assess caching opportunities

**4.3. Coverage Analysis**
- Review adversarial test suite coverage
- Identify untested attack vectors
- Check for gaps in PII type coverage
- Assess topic boundary completeness

**4.4. Compliance Analysis**
- Verify SOX requirements are met
- Check audit logging completeness
- Validate Phoenix integration
- Review retention policies

### 5. Generate Refactoring Plan

Based on analysis, create prioritized refactoring plan:

```markdown
## Guardrails Refactoring Plan

### Current State
- Agent: {agent_name}
- Guardrails Version: {version}
- Issues Identified: {count}

### Priority 1: Critical Security
{list of security issues}

### Priority 2: Performance Optimization
{list of performance improvements}

### Priority 3: Coverage Gaps
{list of coverage improvements}

### Estimated Impact
- Security: {current} → {target}
- Latency: {current_ms} → {target_ms}
- Coverage: {current}% → {target}%
```

### 6. Implement Refactorings

**6.1. Security Refactorings**
- Enable missing guardrails
- Increase thresholds to meet minimums
- Add missing PII types
- Remove bypass vulnerabilities

**6.2. Performance Refactorings**
- Implement tiered evaluation (fast checks first)
- Add caching for repeated inputs
- Parallelize independent guardrails
- Use lighter models where appropriate

**6.3. Coverage Refactorings**
- Add missing adversarial test cases
- Expand PII type detection
- Add new attack pattern detection
- Improve topic boundary definitions

### 7. Generate Changelog

```markdown
## Guardrails Changelog

### Version {new_version} ({date})

#### Security
- {change_1}
- {change_2}

#### Performance
- {change_1}
- {change_2}

#### Coverage
- {change_1}
- {change_2}

#### Breaking Changes
- {if any}

#### Migration Notes
- {if any}
```

### 8. Validate and Report

// turbo
Validate refactored configuration against constitution:
- [ ] All hard-stop rules satisfied
- [ ] All mandatory patterns applied
- [ ] Performance targets met
- [ ] Test suite passes

## Error Handling

| Error | Resolution |
|-------|------------|
| Config not found | Request valid path |
| Invalid YAML | Fix syntax errors first |
| Breaking changes | Generate migration guide |
| Tests fail after refactor | Rollback and investigate |

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide agent name, scope (input/output/both), and guardrail level (L1–L4). |
| `guardrails-engineer-constitution.md` not found | Stop. Ensure file is present at repo root. |
| `deepeval` or `presidio` not installed | Run `pip install deepeval presidio-analyzer presidio-anonymizer`. |
| Guardrail blocks all inputs unexpectedly | Check threshold in `config.template.json` — L1 defaults may be too strict for your domain. |
| PII detection false positives | Review Presidio entity list; exclude irrelevant entity types for your context. |
| Injection pattern test fails | Verify test prompts in `references/` match your threat model; add domain-specific patterns. |

## Examples

**Example 1**: `/refactor-guardrails-engineer guardrails/config.yaml security`
- Output: Security-hardened configuration with increased thresholds

**Example 2**: `/refactor-guardrails-engineer guardrails/config.yaml performance latency<200ms`
- Output: Optimized configuration with tiered evaluation and caching

**Example 3**: `/refactor-guardrails-engineer guardrails/config.yaml compliance SOX`
- Output: SOX-compliant configuration with full audit logging

## References

Constitution: `guardrails-engineer-constitution.md`
