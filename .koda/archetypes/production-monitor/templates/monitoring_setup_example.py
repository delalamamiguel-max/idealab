"""
Example Production Monitoring Setup
Archetype: production-monitor
"""

from dataclasses import dataclass
from typing import Optional
from agent_development.common import setup_phoenix_tracing, create_sox_dashboard_config
import logging

logger = logging.getLogger(__name__)


@dataclass
class MonitoringConfig:
    """Monitoring configuration."""
    agent_name: str
    sox_scope: bool
    slo_latency_p95_ms: float
    slo_success_rate: float
    alert_email: str


class ProductionMonitor:
    """Production monitoring for agents."""
    
    def __init__(self, config: MonitoringConfig):
        self.config = config
        self.metrics = {
            "requests": 0,
            "successes": 0,
            "failures": 0,
            "latencies": [],
        }
        
        # Setup Phoenix tracing
        self.tracer = setup_phoenix_tracing(
            project_name=config.agent_name,
            sox_scope=config.sox_scope,
        )
        
        # Create SOX dashboard if needed
        if config.sox_scope:
            self.dashboard_config = create_sox_dashboard_config(config.agent_name)
            logger.info(f"SOX dashboard configured: {self.dashboard_config['dashboard_name']}")
    
    def record_request(self, latency_ms: float, success: bool):
        """Record request metrics."""
        self.metrics["requests"] += 1
        self.metrics["latencies"].append(latency_ms)
        
        if success:
            self.metrics["successes"] += 1
        else:
            self.metrics["failures"] += 1
        
        # Check SLOs
        self._check_slos()
    
    def _check_slos(self):
        """Check if SLOs are met."""
        if self.metrics["requests"] < 10:
            return  # Not enough data
        
        # Check success rate
        success_rate = self.metrics["successes"] / self.metrics["requests"]
        if success_rate < self.config.slo_success_rate:
            logger.warning(
                f"SLO violation: Success rate {success_rate:.2%} below target {self.config.slo_success_rate:.2%}"
            )
        
        # Check latency
        sorted_latencies = sorted(self.metrics["latencies"])
        p95_index = int(len(sorted_latencies) * 0.95)
        p95_latency = sorted_latencies[p95_index]
        
        if p95_latency > self.config.slo_latency_p95_ms:
            logger.warning(
                f"SLO violation: P95 latency {p95_latency:.0f}ms above target {self.config.slo_latency_p95_ms:.0f}ms"
            )
    
    def get_health_status(self) -> dict:
        """Get current health status."""
        if self.metrics["requests"] == 0:
            return {"status": "unknown", "reason": "No requests yet"}
        
        success_rate = self.metrics["successes"] / self.metrics["requests"]
        
        if success_rate >= self.config.slo_success_rate:
            return {"status": "healthy", "success_rate": success_rate}
        else:
            return {"status": "degraded", "success_rate": success_rate}
