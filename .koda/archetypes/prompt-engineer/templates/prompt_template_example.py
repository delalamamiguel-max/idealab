"""
Example Prompt Template
Archetype: prompt-engineer
"""

from dataclasses import dataclass
from typing import Optional
from jinja2 import Template


@dataclass
class PromptMetadata:
    """Prompt metadata for governance."""
    name: str
    version: str
    author: str
    description: str
    sox_scope: bool = False


class VersionedPrompt:
    """Versioned prompt template with testing."""
    
    def __init__(self, metadata: PromptMetadata, template: str):
        self.metadata = metadata
        self.template = Template(template)
        self.token_count = len(template.split())
    
    def render(self, **kwargs) -> str:
        """Render template with variables."""
        return self.template.render(**kwargs)
    
    def validate(self, test_cases: list[dict]) -> list[bool]:
        """Validate template with test cases."""
        results = []
        for case in test_cases:
            try:
                output = self.render(**case["input"])
                results.append(len(output) > 0)
            except Exception:
                results.append(False)
        return results


# Example prompt
CUSTOMER_SUPPORT_PROMPT = VersionedPrompt(
    metadata=PromptMetadata(
        name="customer_support",
        version="1.0.0",
        author="team@example.com",
        description="Customer support agent system prompt",
        sox_scope=False,
    ),
    template="""You are a helpful customer support agent for {{ company_name }}.

Your role:
- Answer customer questions accurately
- Be polite and professional
- Escalate complex issues to human agents

Guidelines:
- Never make promises about refunds without checking policy
- Always verify customer identity for account changes
- Use the provided context to answer questions

Context:
{{ context }}

Customer Question: {{ question }}

Your Response:"""
)
