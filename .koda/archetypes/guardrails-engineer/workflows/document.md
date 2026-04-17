---
description: Generate comprehensive documentation for guardrails implementation including configuration guides and runbooks (Guardrails Engineer)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Environment Setup

// turbo
Verify documentation tools available:
- Markdown support
- Mermaid diagram support (optional)

### 2. Load Configuration

- Read `guardrails-engineer-constitution.md` for documentation requirements
- Load guardrails configuration to document

### 3. Parse Input

Extract from $ARGUMENTS:
- **Config path**: Path to guardrails configuration
- **Documentation type**: full | quickstart | runbook | api | compliance
- **Audience**: developer | operator | auditor | all
- **Output format**: markdown | html | confluence

If incomplete, request:
```
Please provide:
1. Config Path: (e.g., "guardrails config file")
2. Documentation Type: full | quickstart | runbook | api | compliance
3. Audience: developer | operator | auditor | all
4. Output Format: markdown | html | confluence
```

### 4. Analyze Configuration

Extract documentation elements:
- Enabled guardrails and their configurations
- Threshold values and justifications
- Fallback behaviors
- Monitoring and alerting settings
- Integration points

### 5. Generate Documentation Package

**5.1. README.md (Always Generated)**
```markdown
# Guardrails for {agent_name}

## Overview

This guardrails implementation provides runtime safety controls for {agent_name}, 
including input validation and output filtering.

**Agent Level:** {L1-L4}
**SOX Scope:** {Yes/No}
**Version:** {version}

## Quick Start

### Installation

\`\`\`bash
pip install deepeval presidio-analyzer presidio-anonymizer
\`\`\`

### Basic Usage

\`\`\`python
from guardrails import with_guardrails

@with_guardrails(load_guardrails_config(config_ref))
async def my_agent(user_input: str, context: list[str] = None):
    # Your agent logic here
    return response
\`\`\`

## Enabled Guardrails

### Input Guardrails

| Guardrail | Status | Threshold | Action |
|-----------|--------|-----------|--------|
| Prompt Injection | {enabled/disabled} | {threshold} | {action} |
| PII Detection | {enabled/disabled} | N/A | {action} |
| Topic Boundary | {enabled/disabled} | {threshold} | {action} |

### Output Guardrails

| Guardrail | Status | Threshold | Action |
|-----------|--------|-----------|--------|
| Hallucination | {enabled/disabled} | {threshold} | {action} |
| PII Leakage | {enabled/disabled} | {threshold} | {action} |
| Toxicity | {enabled/disabled} | {threshold} | {action} |
| Non-Advice | {enabled/disabled} | {threshold} | {action} |

## Configuration

See `config.yaml` for full configuration options.

## Testing

\`\`\`bash
pytest tests/ -v
\`\`\`

## Monitoring

Guardrail triggers are logged to {logging destination}.
{If Phoenix enabled: Telemetry exported to Arize Phoenix.}

## Support

Contact: {team/channel}
```

**5.2. Configuration Guide (Developer)**
```markdown
# Guardrails Configuration Guide

## Configuration Schema

### Input Guardrails

#### Prompt Injection Detection

Detects attempts to override system instructions.

\`\`\`yaml
input:
  prompt_injection:
    enabled: true
    model: "gpt-3.5-turbo"  # Classifier model
    threshold: 0.8           # Confidence threshold (0-1)
    action: "block"          # block | warn | log
    fallback_message: "..."  # User-facing message when blocked
\`\`\`

**Tuning Guide:**
- Lower threshold (0.6-0.7): More aggressive, more false positives
- Higher threshold (0.85-0.95): Less aggressive, may miss attacks
- Recommended: 0.8 for balanced security/UX

#### PII Detection

Detects and masks personally identifiable information.

\`\`\`yaml
input:
  pii_detection:
    enabled: true
    engine: "presidio"
    types:
      - SSN
      - CREDIT_CARD
      - PHONE
      - EMAIL
      - ADDRESS
      - PERSON
    action: "mask"
    mask_pattern: "[REDACTED-{type}]"
\`\`\`

**Supported PII Types:**
- SSN: Social Security Numbers (US)
- CREDIT_CARD: Credit/debit card numbers
- PHONE: Phone numbers
- EMAIL: Email addresses
- ADDRESS: Physical addresses
- PERSON: Person names
- [Full list: https://microsoft.github.io/presidio/]

### Output Guardrails

#### Hallucination Check

Ensures output is grounded in provided context.

\`\`\`yaml
output:
  hallucination:
    enabled: true
    metric: "FaithfulnessMetric"
    threshold: 0.9
    action: "block"
    require_context: true
\`\`\`

**Important:** Requires context to be provided. Without context, 
this guardrail cannot evaluate faithfulness.

[Continue for each guardrail type...]
```

**5.3. Operations Runbook (Operator)**
```markdown
# Guardrails Operations Runbook

## Monitoring Dashboard

### Key Metrics

| Metric | Normal Range | Warning | Critical |
|--------|--------------|---------|----------|
| Trigger Rate | <5% | 5-10% | >10% |
| False Positive Rate | <2% | 2-5% | >5% |
| P95 Latency | <500ms | 500-1000ms | >1000ms |
| Error Rate | <0.1% | 0.1-1% | >1% |

### Alerts

| Alert | Condition | Action |
|-------|-----------|--------|
| High Trigger Rate | >10% triggers/hour | Investigate attack or config issue |
| Bypass Attempt | Any bypass logged | Security review required |
| Latency Spike | P95 >1000ms | Check model availability |
| Error Spike | >1% errors | Check logs, restart if needed |

## Incident Response

### Guardrail Blocking Legitimate Requests

**Symptoms:** Users report valid requests being blocked

**Diagnosis:**
1. Check logs for blocked request details
2. Review confidence scores
3. Check for pattern matches

**Resolution:**
1. If false positive, add exception pattern
2. If threshold too low, adjust configuration
3. If attack pattern, no action needed

\`\`\`bash
# Find recent blocks
grep "guardrail_trigger" /var/log/agent.log | tail -100

# Check specific request
python3 -c "from guardrails import debug; debug.analyze('{input}')"
\`\`\`

### Guardrail Missing Threats

**Symptoms:** Malicious content getting through

**Diagnosis:**
1. Review the bypassed content
2. Check if pattern is known
3. Check threshold configuration

**Resolution:**
1. Add new attack pattern
2. Lower detection threshold
3. Add additional guardrail layer

### Performance Degradation

**Symptoms:** Increased latency, timeouts

**Diagnosis:**
1. Check model provider status
2. Check resource utilization
3. Review recent config changes

**Resolution:**
1. Enable caching if not already
2. Switch to lighter model
3. Scale horizontally

## Maintenance Procedures

### Updating Thresholds

\`\`\`bash
# 1. Backup current config
cp config.yaml config.yaml.bak

# 2. Update threshold
vim config.yaml

# 3. Run test suite
pytest tests/ -v

# 4. Deploy with canary
kubectl rollout restart deployment/agent --canary

# 5. Monitor for 1 hour
watch -n 60 guardrails-metrics-check

# 6. Full rollout
kubectl rollout resume deployment/agent
\`\`\`

### Adding New Guardrail

1. Add configuration to config.yaml
2. Update test suite with new cases
3. Run full test suite
4. Deploy to staging
5. Monitor for 24 hours
6. Deploy to production

## Emergency Procedures

### Disable All Guardrails (Emergency Only)

**WARNING:** Only use in critical production incidents

\`\`\`bash
# Set emergency bypass flag
export GUARDRAILS_BYPASS=true

# Restart agent
kubectl rollout restart deployment/agent

# IMMEDIATELY investigate root cause
# Re-enable guardrails ASAP
\`\`\`

### Rollback Configuration

\`\`\`bash
# Restore previous config
cp config.yaml.bak config.yaml

# Restart
kubectl rollout restart deployment/agent
\`\`\`
```

**5.4. Compliance Documentation (Auditor)**
```markdown
# Guardrails Compliance Documentation

## SOX Control Mapping

| Control ID | Control Description | Guardrails Implementation |
|------------|---------------------|---------------------------|
| SOX-AGT-001 | Decision Traceability | All guardrail triggers logged with rationale |
| SOX-AGT-002 | Model Version Control | Classifier model version recorded in config |
| SOX-AGT-003 | Evaluation Governance | Threshold changes require approval |
| SOX-AGT-004 | Change Authorization | Config changes logged with approver |
| SOX-AGT-005 | Drift Detection | Trigger rate monitoring enabled |
| SOX-AGT-006 | Access Logging | All config access logged |

## Audit Evidence

### Configuration History

All configuration changes are version-controlled in Git with:
- Change description
- Approver identity
- Timestamp
- Test results

### Trigger Logs

Guardrail trigger logs include:
- Timestamp (ISO 8601)
- Guardrail type
- Confidence score
- Action taken
- Request ID (for correlation)

**Retention:** {retention_period} per policy

### Effectiveness Metrics

Monthly reports include:
- Total requests processed
- Trigger rate by guardrail type
- False positive rate (sampled)
- Latency percentiles

## Audit Queries

### All Triggers in Date Range

\`\`\`sql
SELECT * FROM guardrail_logs
WHERE timestamp BETWEEN '{start}' AND '{end}'
ORDER BY timestamp DESC;
\`\`\`

### Configuration Changes

\`\`\`bash
git log --oneline --since="{date}" -- guardrails/config.yaml
\`\`\`

### Bypass Attempts

\`\`\`sql
SELECT * FROM guardrail_logs
WHERE event_type = 'bypass_attempt'
ORDER BY timestamp DESC;
\`\`\`
```

**5.5. API Reference (Developer)**
```markdown
# Guardrails API Reference

## Classes

### GuardrailsWrapper

Main wrapper class for applying guardrails to agent functions.

\`\`\`python
class GuardrailsWrapper:
    def __init__(self, config_path: str):
        """
        Initialize guardrails from configuration file.
        
        Args:
            config_path: Path to guardrails config.yaml
        """
    
    async def __call__(
        self,
        agent_fn: Callable,
        user_input: str,
        context: list[str] = None,
        **kwargs
    ) -> dict[str, Any]:
        """
        Execute agent with guardrails.
        
        Args:
            agent_fn: Async agent function to wrap
            user_input: User input text
            context: Optional context for hallucination check
            **kwargs: Additional args passed to agent_fn
            
        Returns:
            dict with keys:
                - status: "success" | "blocked"
                - stage: "input" | "output" (if blocked)
                - output: Agent output (if success)
                - message: Fallback message (if blocked)
                - guardrail_results: List of evaluation results
        """
\`\`\`

### GuardrailResult

Result of a single guardrail evaluation.

\`\`\`python
@dataclass
class GuardrailResult:
    passed: bool              # Whether guardrail passed
    guardrail_type: str       # Type of guardrail
    confidence: float         # Confidence score (0-1)
    action_taken: str         # Action: none | mask | block | warn
    details: Optional[str]    # Additional details
    masked_input: Optional[str]  # Masked input (for PII)
\`\`\`

## Decorators

### @with_guardrails

Decorator to wrap agent function with guardrails.

\`\`\`python
@with_guardrails(load_guardrails_config(config_ref))
async def my_agent(user_input: str, context: list[str] = None):
    # Agent logic
    return response
\`\`\`

## Configuration Options

See Configuration Guide for full schema.
```

### 6. Validate Documentation

// turbo
Validate documentation completeness:
- [ ] README with quick start
- [ ] Configuration guide with all options
- [ ] Runbook with incident procedures
- [ ] API reference with all classes/methods
- [ ] Compliance documentation (if SOX)

### 7. Generate Output

Package documentation based on output format:
- **Markdown**: Output as .md files
- **HTML**: Convert to HTML with styling
- **Confluence**: Format for Confluence import

## Error Handling

| Error | Resolution |
|-------|------------|
| Config not found | Request valid path |
| Missing sections | Generate with defaults, flag for review |
| Invalid format | Default to markdown |

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

**Example 1**: `/document-guardrails-engineer guardrails/config.yaml full developer markdown`
- Output: Complete documentation package for developers

**Example 2**: `/document-guardrails-engineer guardrails/config.yaml runbook operator`
- Output: Operations runbook for SRE team

**Example 3**: `/document-guardrails-engineer guardrails/config.yaml compliance auditor`
- Output: SOX compliance documentation for auditors

## References

Constitution: `guardrails-engineer-constitution.md`
