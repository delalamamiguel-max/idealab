"""
Example Workflow Optimization Analysis
Archetype: workflow-optimizer
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class NodeMetrics:
    """Metrics for a workflow node."""
    node_name: str
    avg_latency_ms: float
    call_count: int
    token_usage: int
    cost_usd: float


@dataclass
class OptimizationRecommendation:
    """Optimization recommendation."""
    node_name: str
    issue: str
    recommendation: str
    estimated_improvement: str


class WorkflowOptimizer:
    """Analyze and optimize workflow performance."""
    
    def __init__(self, workflow_name: str):
        self.workflow_name = workflow_name
        self.node_metrics = []
    
    def add_node_metrics(self, metrics: NodeMetrics):
        """Add metrics for a node."""
        self.node_metrics.append(metrics)
    
    def analyze(self) -> list[OptimizationRecommendation]:
        """Analyze workflow and generate recommendations."""
        recommendations = []
        
        # Find latency bottlenecks
        total_latency = sum(m.avg_latency_ms for m in self.node_metrics)
        for metrics in self.node_metrics:
            latency_pct = (metrics.avg_latency_ms / total_latency) * 100
            
            if latency_pct > 40:
                recommendations.append(OptimizationRecommendation(
                    node_name=metrics.node_name,
                    issue=f"Node accounts for {latency_pct:.0f}% of total latency",
                    recommendation="Consider caching, parallel execution, or faster model",
                    estimated_improvement=f"Reduce latency by {latency_pct * 0.5:.0f}%",
                ))
        
        # Find cost hotspots
        total_cost = sum(m.cost_usd for m in self.node_metrics)
        for metrics in self.node_metrics:
            if total_cost > 0:
                cost_pct = (metrics.cost_usd / total_cost) * 100
                
                if cost_pct > 50:
                    recommendations.append(OptimizationRecommendation(
                        node_name=metrics.node_name,
                        issue=f"Node accounts for {cost_pct:.0f}% of total cost",
                        recommendation="Consider smaller model or prompt optimization",
                        estimated_improvement=f"Reduce cost by {cost_pct * 0.3:.0f}%",
                    ))
        
        # Find redundant calls
        for metrics in self.node_metrics:
            if metrics.call_count > 5:
                recommendations.append(OptimizationRecommendation(
                    node_name=metrics.node_name,
                    issue=f"Node called {metrics.call_count} times per workflow",
                    recommendation="Consider loop detection or early termination",
                    estimated_improvement="Reduce calls by 50%",
                ))
        
        return recommendations
    
    def generate_report(self) -> dict:
        """Generate optimization report."""
        recommendations = self.analyze()
        
        return {
            "workflow": self.workflow_name,
            "total_nodes": len(self.node_metrics),
            "total_latency_ms": sum(m.avg_latency_ms for m in self.node_metrics),
            "total_cost_usd": sum(m.cost_usd for m in self.node_metrics),
            "recommendations": [
                {
                    "node": r.node_name,
                    "issue": r.issue,
                    "recommendation": r.recommendation,
                    "improvement": r.estimated_improvement,
                }
                for r in recommendations
            ],
        }
