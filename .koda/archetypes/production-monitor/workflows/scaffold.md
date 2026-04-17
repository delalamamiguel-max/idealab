---
description: Set up production monitoring with Arize Phoenix and SOX compliance (Production Monitor)
---

User input: $ARGUMENTS

## Execution Steps

### 1. Parse Input
- **Agent name**: Agent to monitor
- **SOX scope**: Whether SOX compliance required
- **SLOs**: Latency, error rate targets

### 2. Generate Phoenix Integration

```python
from phoenix.otel import register
from opentelemetry import trace

tracer_provider = register(
    project_name="{agent_name}",
    endpoint="${PHOENIX_ENDPOINT}"
)

# Instrument LangChain
from openinference.instrumentation.langchain import LangChainInstrumentor
LangChainInstrumentor().instrument()
```

### 3. Configure SLOs and Alerts

```yaml
slos:
  latency_p95_ms: 2000
  error_rate: 0.01
  eval_pass_rate: 0.95

alerts:
  - name: high_latency
    condition: latency_p95 > 2000
    channel: slack
```

### 4. Add LLM Quality Alerts + SOX Dashboard (if required)

```python
# LLM Quality SLOs — add to your SLO config
slos_quality = """
slos:
  latency_p95_ms: 2000
  error_rate: 0.01
  eval_pass_rate: 0.95
  hallucination_rate_max: 0.05   # Alert if hallucination > 5%
  faithfulness_min: 0.80
  answer_relevancy_min: 0.80
"""

# Configure DeepEval + Phoenix eval-based alerting
from deepeval.metrics import HallucinationMetric, FaithfulnessMetric, AnswerRelevancyMetric

quality_alerts = {
    "hallucination_rate": {
        "metric": HallucinationMetric(threshold=0.05),
        "condition": "score > 0.05",
        "channel": "slack",
        "severity": "critical",
    },
    "faithfulness": {
        "metric": FaithfulnessMetric(threshold=0.80),
        "condition": "score < 0.80",
        "channel": "slack",
        "severity": "warning",
    },
    "answer_relevancy": {
        "metric": AnswerRelevancyMetric(threshold=0.80),
        "condition": "score < 0.80",
        "channel": "slack",
        "severity": "warning",
    },
}
```

**SOX Dashboard (if `SOX scope = yes`):**

```python
import json

sox_dashboard_config = {
    "dashboard_name": f"{agent_name}_sox_audit",
    "retention_days": 2555,  # 7 years per SOX
    "required_fields": ["agent_name", "user_id", "timestamp", "input_hash", "output_hash"],
    "alert_on_missing_fields": True,
    "export_format": "jsonl",
    "export_destination": "${AUDIT_LOG_PATH}",
}

with open("sox_dashboard_config.json", "w") as f:
    json.dump(sox_dashboard_config, f, indent=2)
```

### 5. Validate

```bash
# Confirm Phoenix endpoint is reachable
> Use a platform-appropriate HTTP client to query the Phoenix health endpoint and verify that the response contains `ok`.
Run the Phoenix health check with the platform's default HTTP client and confirm the service is reachable.

# Run a sample trace through the monitored agent and verify it appears in Phoenix
python3 -c "
from opentelemetry import trace
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span('validation-ping'):
    print('Trace emitted — check Phoenix dashboard')
"
```

**Checklist:**
- [ ] Phoenix dashboard shows traces from the agent
- [ ] Latency SLO alert fires when latency > threshold (test with a slow mock)
- [ ] Hallucination alert fires when `hallucination_rate > 0.05`
- [ ] SOX audit log receives events if `SOX scope = yes`
- [ ] All 7 env vars from `config.template.json` are set (PHOENIX_ENDPOINT, ARIZE_API_KEY, SLACK_WEBHOOK_URL, etc.)

## Error Handling

| Condition | Action |
|-----------|--------|
| `$ARGUMENTS` missing or empty | Stop. Prompt user: provide agent name, SOX scope (yes/no), and SLO targets. |
| `production-monitor-constitution.md` not found | Stop. Ensure file is present at repo root. |
| `PHOENIX_ENDPOINT` not set | Set environment variable. Default for local dev: `http://localhost:6006`. |
| Phoenix unreachable | Verify Phoenix server is running. Check network/firewall. Fall back to local OTLP collector. |
| LLM quality alert never fires | Confirm `deepeval` is installed and eval pipeline is wired to emit metrics to Phoenix. |
| SOX audit log missing events | Verify `AUDIT_LOG_PATH` env var is set and writable. Check `log_sox_event()` calls in agent code. |

## Examples
**Example**: `/scaffold-production-monitor support-agent SOX=yes`
