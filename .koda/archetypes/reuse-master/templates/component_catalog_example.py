"""
Example Component Catalog
Archetype: reuse-master
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ComponentMetadata:
    """Metadata for a reusable component."""
    name: str
    type: str  # "tool", "prompt", "guardrail", "workflow"
    description: str
    tags: list[str]
    author: str
    version: str
    usage_count: int = 0


class ComponentCatalog:
    """Catalog of reusable components."""
    
    def __init__(self):
        self.components = []
    
    def register(self, component: ComponentMetadata):
        """Register a component in the catalog."""
        self.components.append(component)
    
    def search(self, query: str, component_type: Optional[str] = None) -> list[ComponentMetadata]:
        """
        Search for components.
        
        Args:
            query: Search query
            component_type: Filter by component type
            
        Returns:
            Matching components
        """
        query_lower = query.lower()
        results = []
        
        for component in self.components:
            # Type filter
            if component_type and component.type != component_type:
                continue
            
            # Search in name, description, tags
            matches = (
                query_lower in component.name.lower() or
                query_lower in component.description.lower() or
                any(query_lower in tag.lower() for tag in component.tags)
            )
            
            if matches:
                results.append(component)
        
        # Sort by usage count
        return sorted(results, key=lambda x: x.usage_count, reverse=True)
    
    def recommend(self, context: str, limit: int = 5) -> list[ComponentMetadata]:
        """
        Recommend components based on context.
        
        Args:
            context: Context description
            limit: Maximum recommendations
            
        Returns:
            Recommended components
        """
        # Simple keyword-based recommendation
        keywords = context.lower().split()
        scored = []
        
        for component in self.components:
            score = 0
            for keyword in keywords:
                if keyword in component.description.lower():
                    score += 1
                if keyword in component.tags:
                    score += 2
            
            if score > 0:
                scored.append((score, component))
        
        # Sort by score and usage
        scored.sort(key=lambda x: (x[0], x[1].usage_count), reverse=True)
        return [comp for _, comp in scored[:limit]]
    
    def increment_usage(self, component_name: str):
        """Increment usage count for a component."""
        for component in self.components:
            if component.name == component_name:
                component.usage_count += 1
                break


# Example catalog
catalog = ComponentCatalog()

catalog.register(ComponentMetadata(
    name="search_tool",
    type="tool",
    description="Web search tool with rate limiting",
    tags=["search", "web", "retrieval"],
    author="team@example.com",
    version="1.0.0",
    usage_count=45,
))

catalog.register(ComponentMetadata(
    name="pii_masking_guardrail",
    type="guardrail",
    description="Mask PII in user input and agent output",
    tags=["security", "pii", "compliance"],
    author="security@example.com",
    version="2.1.0",
    usage_count=120,
))
