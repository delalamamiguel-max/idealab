"""
Example Agent Similarity Detection
Archetype: scope-deduplicator
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AgentProfile:
    """Profile of an agent for comparison."""
    name: str
    description: str
    capabilities: list[str]
    tools: list[str]
    data_products: list[str]


@dataclass
class SimilarityResult:
    """Result of similarity analysis."""
    agent1: str
    agent2: str
    similarity_score: float
    overlapping_capabilities: list[str]
    recommendation: str


class ScopeDeduplicator:
    """Detect duplicate or overlapping agent capabilities."""
    
    def __init__(self):
        self.agents = []
    
    def register_agent(self, profile: AgentProfile):
        """Register an agent profile."""
        self.agents.append(profile)
    
    def _calculate_similarity(self, agent1: AgentProfile, agent2: AgentProfile) -> float:
        """Calculate similarity score between two agents."""
        # Capability overlap
        cap_overlap = len(set(agent1.capabilities) & set(agent2.capabilities))
        cap_total = len(set(agent1.capabilities) | set(agent2.capabilities))
        cap_score = cap_overlap / cap_total if cap_total > 0 else 0
        
        # Tool overlap
        tool_overlap = len(set(agent1.tools) & set(agent2.tools))
        tool_total = len(set(agent1.tools) | set(agent2.tools))
        tool_score = tool_overlap / tool_total if tool_total > 0 else 0
        
        # Data product overlap
        data_overlap = len(set(agent1.data_products) & set(agent2.data_products))
        data_total = len(set(agent1.data_products) | set(agent2.data_products))
        data_score = data_overlap / data_total if data_total > 0 else 0
        
        # Weighted average
        return (cap_score * 0.5) + (tool_score * 0.3) + (data_score * 0.2)
    
    def find_duplicates(self, threshold: float = 0.7) -> list[SimilarityResult]:
        """Find agents with high similarity."""
        results = []
        
        for i, agent1 in enumerate(self.agents):
            for agent2 in self.agents[i+1:]:
                similarity = self._calculate_similarity(agent1, agent2)
                
                if similarity >= threshold:
                    overlapping = list(set(agent1.capabilities) & set(agent2.capabilities))
                    
                    if similarity >= 0.9:
                        recommendation = "CONSOLIDATE: Agents are nearly identical"
                    elif similarity >= 0.7:
                        recommendation = "REVIEW: Significant overlap, consider merging"
                    else:
                        recommendation = "MONITOR: Some overlap detected"
                    
                    results.append(SimilarityResult(
                        agent1=agent1.name,
                        agent2=agent2.name,
                        similarity_score=similarity,
                        overlapping_capabilities=overlapping,
                        recommendation=recommendation,
                    ))
        
        return sorted(results, key=lambda x: x.similarity_score, reverse=True)
