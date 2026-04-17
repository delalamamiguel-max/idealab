"""
Thinking Agent — Multi-Agent Orchestrator with Dynamic Reasoning

This implements a true thinking agent that coordinates specialized subagents
for experimentation intelligence, with dynamic context building and reasoning.
"""

import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from openai import OpenAI


class AgentMode(Enum):
    SEARCH = "search"
    IDEATION = "ideation"
    PREDICTION = "prediction"
    INTAKE = "intake"
    MIXED = "mixed"


@dataclass
class ThinkingStep:
    agent: str
    thought: str
    action: str
    result: str
    confidence: float
    timestamp: float


@dataclass
class AgentResponse:
    content: str
    confidence: float
    reasoning: List[str]
    evidence: List[str]
    next_actions: List[str]


class ThinkingAgent:
    """
    Main orchestrator that coordinates specialized subagents for experimentation intelligence.
    
    This agent thinks step-by-step, delegates to specialists, and synthesizes responses
    with full reasoning transparency.
    """
    
    def __init__(self, client: OpenAI, model: str = "gpt-4o", temperature: float = 0.4):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.thinking_history: List[ThinkingStep] = []
        self.context_cache: Dict[str, Any] = {}
        
    def process_query(self, query: str, context: str, stream_callback=None) -> str:
        """
        Main entry point: analyze query, coordinate subagents, synthesize response.
        """
        # Step 1: Analyze user intent and determine mode
        if stream_callback:
            stream_callback("🧠 **Analyzing query intent...**\n\n")
        
        intent_analysis = self._analyze_intent(query)
        mode = intent_analysis["mode"]
        
        if stream_callback:
            stream_callback(f"**Intent detected:** {intent_analysis['description']}\n")
            stream_callback(f"**Mode:** {mode.value}\n")
            stream_callback(f"**Key entities:** {', '.join(intent_analysis['entities'])}\n\n")
        
        # Step 2: Build dynamic context based on query
        if stream_callback:
            stream_callback("📊 **Building dynamic context...**\n\n")
            
        relevant_context = self._build_dynamic_context(query, context, intent_analysis)
        
        if stream_callback:
            stream_callback(f"**Context scope:** {relevant_context['scope']}\n")
            stream_callback(f"**Relevant experiments:** {relevant_context['experiment_count']}\n")
            stream_callback(f"**Key patterns:** {', '.join(relevant_context['patterns'])}\n\n")
        
        # Step 3: Coordinate subagents based on mode
        if stream_callback:
            stream_callback("🤖 **Coordinating specialist agents...**\n\n")
            
        subagent_results = self._coordinate_subagents(mode, query, relevant_context, stream_callback)
        
        # Step 4: Synthesize final response
        if stream_callback:
            stream_callback("🔄 **Synthesizing insights...**\n\n")
            
        final_response = self._synthesize_response(query, subagent_results, relevant_context)
        
        if stream_callback:
            stream_callback("✅ **Analysis complete**\n\n---\n\n")
            
        return final_response
    
    def _analyze_intent(self, query: str) -> Dict[str, Any]:
        """Analyze user query to determine intent, mode, and key entities."""
        
        intent_prompt = f"""
        Analyze this experimentation query to determine the user's intent and required processing mode.
        
        Query: "{query}"
        
        Determine:
        1. Primary intent (search, ideation, prediction, intake, mixed)
        2. Key entities (journeys, site areas, metrics, tactics mentioned)
        3. Specific business objective
        4. Required depth of analysis
        
        Return JSON with:
        {{
            "mode": "search|ideation|prediction|intake|mixed",
            "description": "brief description of what user wants",
            "entities": ["entity1", "entity2"],
            "business_objective": "what business goal this serves",
            "analysis_depth": "surface|detailed|comprehensive"
        }}
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": intent_prompt}],
            temperature=0.1,
            max_tokens=500
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            result["mode"] = AgentMode(result["mode"])
            return result
        except:
            # Fallback if JSON parsing fails
            return {
                "mode": AgentMode.MIXED,
                "description": "General experimentation query",
                "entities": [],
                "business_objective": "Improve conversion",
                "analysis_depth": "detailed"
            }
    
    def _build_dynamic_context(self, query: str, full_context: str, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Build focused context based on query intent and entities."""
        
        context_prompt = f"""
        Extract the most relevant context for this experimentation query.
        
        Query: "{query}"
        Intent: {intent['description']}
        Key entities: {intent['entities']}
        
        From this full context, identify:
        1. Most relevant experiments (by journey, site area, tactic)
        2. Key patterns that apply
        3. Success/failure precedents
        4. Data gaps or uncertainties
        
        Full Context:
        {full_context[:8000]}  # Truncate to fit in context window
        
        Return a focused summary of relevant experiments and patterns.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": context_prompt}],
            temperature=0.2,
            max_tokens=2000
        )
        
        relevant_experiments = response.choices[0].message.content
        
        return {
            "scope": f"Focused on {', '.join(intent['entities'])}",
            "experiment_count": len([line for line in relevant_experiments.split('\n') if 'Experiment' in line]),
            "patterns": self._extract_patterns(relevant_experiments),
            "content": relevant_experiments
        }
    
    def _extract_patterns(self, context: str) -> List[str]:
        """Extract key patterns from context."""
        # Simple pattern extraction - could be enhanced with NLP
        patterns = []
        if "win" in context.lower():
            patterns.append("winning precedents")
        if "loss" in context.lower():
            patterns.append("failure patterns")
        if "neutral" in context.lower():
            patterns.append("neutral results")
        if "+" in context:
            patterns.append("positive lifts")
        if "-" in context:
            patterns.append("negative impacts")
        return patterns[:3]  # Top 3 patterns
    
    def _coordinate_subagents(self, mode: AgentMode, query: str, context: Dict[str, Any], stream_callback=None) -> Dict[str, AgentResponse]:
        """Coordinate specialized subagents based on the determined mode."""
        
        results = {}
        
        if mode == AgentMode.SEARCH or mode == AgentMode.MIXED:
            if stream_callback:
                stream_callback("🔍 **Knowledge Agent:** Searching historical experiments...\n")
            results["knowledge"] = self._knowledge_agent(query, context)
            
        if mode == AgentMode.IDEATION or mode == AgentMode.MIXED:
            if stream_callback:
                stream_callback("💡 **Ideation Agent:** Generating experiment concepts...\n")
            results["ideation"] = self._ideation_agent(query, context)
            
        if mode == AgentMode.PREDICTION or mode == AgentMode.MIXED:
            if stream_callback:
                stream_callback("📊 **Prediction Agent:** Evaluating success probability...\n")
            results["prediction"] = self._prediction_agent(query, context)
            
        if mode == AgentMode.INTAKE or mode == AgentMode.MIXED:
            if stream_callback:
                stream_callback("📝 **Intake Agent:** Structuring for delivery...\n")
            results["intake"] = self._intake_agent(query, context)
        
        # Always include reasoning agent for synthesis
        if stream_callback:
            stream_callback("🧮 **Reasoning Agent:** Analyzing patterns and implications...\n")
        results["reasoning"] = self._reasoning_agent(query, context, results)
        
        return results
    
    def _knowledge_agent(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        """Specialized agent for searching and analyzing historical experiments."""
        
        prompt = f"""
        You are the Knowledge Agent, specialized in searching and analyzing historical experiment data.
        
        Query: "{query}"
        
        Context: {context['content']}
        
        Your tasks:
        1. Find the most relevant historical experiments
        2. Rank them by relevance (direct analog, partial analog, weak analog)
        3. Extract key learnings and patterns
        4. Identify data gaps or uncertainties
        5. Provide evidence strength assessment
        
        Format your response as structured analysis with:
        - Relevant experiments (with reference numbers)
        - Key patterns identified
        - Evidence strength (high/medium/low)
        - Confidence in findings (0-100%)
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        
        return AgentResponse(
            content=content,
            confidence=0.85,  # Could be dynamically calculated
            reasoning=["Historical data analysis", "Pattern recognition"],
            evidence=["XTrack experiment database"],
            next_actions=["Validate findings", "Check for recent updates"]
        )
    
    def _ideation_agent(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        """Specialized agent for generating new experiment ideas."""
        
        prompt = f"""
        You are the Ideation Agent, specialized in generating new experiment concepts grounded in historical evidence.
        
        Query: "{query}"
        
        Historical Context: {context['content']}
        
        Generate 2-3 experiment ideas using this framework:
        
        For each idea:
        1. **Empathize**: Business objective, observed problem, baseline metrics
        2. **Define**: Clear hypothesis with expected mechanism of change
        3. **Ideate**: Control vs variant description, test approach
        4. **Delivery**: Effort estimate, dependencies, risks, priority
        
        Ground each idea in historical precedent - reference similar experiments and explain what would be different.
        
        Focus on:
        - Falsifiable hypotheses
        - Clear primary metrics
        - Realistic implementation
        - Strong historical grounding
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        
        return AgentResponse(
            content=content,
            confidence=0.75,
            reasoning=["Historical pattern analysis", "Creative synthesis"],
            evidence=["Similar experiment outcomes", "Pattern extrapolation"],
            next_actions=["Validate feasibility", "Estimate traffic requirements"]
        )
    
    def _prediction_agent(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        """Specialized agent for predicting experiment success probability."""
        
        prompt = f"""
        You are the Prediction Agent, specialized in evaluating the likely success of proposed experiments.
        
        Query: "{query}"
        
        Historical Context: {context['content']}
        
        Analyze the proposed experiment(s) and predict success probability based on:
        
        1. **Historical Precedent**: Direct and partial analogs
        2. **Pattern Matching**: Similar tactics, audiences, site areas
        3. **Success Factors**: What drives wins vs losses
        4. **Risk Assessment**: What could go wrong
        5. **Confidence Calibration**: How certain are you?
        
        Provide:
        - Success probability (0-100%)
        - Key success factors
        - Primary risks
        - Historical evidence supporting prediction
        - Confidence level in prediction
        
        Be honest about uncertainty - if historical data is limited, say so.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        
        return AgentResponse(
            content=content,
            confidence=0.70,
            reasoning=["Statistical pattern analysis", "Risk assessment"],
            evidence=["Historical success rates", "Analog performance"],
            next_actions=["Monitor similar experiments", "Adjust based on new data"]
        )
    
    def _intake_agent(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        """Specialized agent for creating intake-ready experiment specifications."""
        
        prompt = f"""
        You are the Intake Agent, specialized in converting experiment concepts into JIRA-ready intake tickets.
        
        Query: "{query}"
        
        Context: {context['content']}
        
        Create a structured intake ticket with:
        
        **EXPERIMENT BRIEF**
        - Title: Clear, descriptive name
        - Business Objective: What we're trying to achieve
        - Success Metrics: Primary and secondary KPIs
        
        **HYPOTHESIS & RATIONALE**
        - Hypothesis: If [change], then [expected result] because [rationale]
        - Historical Precedent: Similar experiments and their outcomes
        - Expected Impact: Quantified prediction with confidence interval
        
        **TEST DESIGN**
        - Control: Current experience description
        - Variant(s): Proposed changes with mockups/wireframes needed
        - Audience: Who gets the test (inclusion/exclusion criteria)
        - Traffic Split: Recommended allocation
        - Runtime: Estimated test duration
        
        **IMPLEMENTATION**
        - Technical Requirements: What needs to be built
        - Dependencies: Other teams/systems involved
        - Effort Estimate: T-shirt size (S/M/L/XL)
        - Risk Assessment: What could go wrong
        
        **MEASUREMENT PLAN**
        - Primary Metric: Single success measure
        - Secondary Metrics: Supporting measurements
        - Minimum Detectable Effect: Statistical requirements
        - Analysis Plan: How we'll interpret results
        
        Make this ready for immediate handoff to development teams.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=2500
        )
        
        content = response.choices[0].message.content
        
        return AgentResponse(
            content=content,
            confidence=0.80,
            reasoning=["Requirements analysis", "Structured documentation"],
            evidence=["Best practice templates", "Historical specifications"],
            next_actions=["Review with stakeholders", "Validate technical feasibility"]
        )
    
    def _reasoning_agent(self, query: str, context: Dict[str, Any], subagent_results: Dict[str, AgentResponse]) -> AgentResponse:
        """Meta-agent that analyzes patterns and provides strategic reasoning."""
        
        # Collect all subagent insights
        all_insights = []
        for agent_name, result in subagent_results.items():
            all_insights.append(f"**{agent_name.title()} Agent Insights:**\n{result.content}\n")
        
        prompt = f"""
        You are the Reasoning Agent, responsible for meta-analysis and strategic insight synthesis.
        
        Original Query: "{query}"
        
        Subagent Analysis Results:
        {chr(10).join(all_insights)}
        
        Your tasks:
        1. **Pattern Recognition**: What patterns emerge across all analyses?
        2. **Conflict Resolution**: Where do subagents disagree? What's the truth?
        3. **Strategic Implications**: What does this mean for the broader program?
        4. **Quality Assessment**: How confident should we be in these recommendations?
        5. **Next Steps**: What are the highest-value follow-up actions?
        
        Provide:
        - Key insights that emerge from combining all analyses
        - Areas of uncertainty or disagreement
        - Strategic recommendations for the experimentation program
        - Confidence assessment of overall analysis
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        
        return AgentResponse(
            content=content,
            confidence=0.85,
            reasoning=["Meta-analysis", "Strategic synthesis"],
            evidence=["Cross-agent validation", "Pattern convergence"],
            next_actions=["Validate with stakeholders", "Monitor implementation"]
        )
    
    def _synthesize_response(self, query: str, subagent_results: Dict[str, AgentResponse], context: Dict[str, Any]) -> str:
        """Synthesize all subagent results into a coherent, actionable response."""
        
        # Build final synthesis
        synthesis_prompt = f"""
        Synthesize these specialist analyses into a single, coherent response for the user.
        
        Original Query: "{query}"
        
        Specialist Analysis:
        {chr(10).join([f"**{name.title()}:** {result.content}" for name, result in subagent_results.items()])}
        
        Create a user-ready response that:
        1. Directly answers their question
        2. Provides actionable insights
        3. Shows the reasoning behind recommendations
        4. Includes relevant historical evidence
        5. Suggests concrete next steps
        
        Format as a polished, professional analysis that a CRO team can immediately use.
        Use markdown formatting for clarity.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": synthesis_prompt}],
            temperature=0.3,
            max_tokens=3000
        )
        
        return response.choices[0].message.content
    
    def get_thinking_summary(self) -> str:
        """Return a summary of the thinking process for transparency."""
        if not self.thinking_history:
            return "No thinking steps recorded."
        
        summary = "## 🧠 Thinking Process\n\n"
        for step in self.thinking_history[-5:]:  # Last 5 steps
            summary += f"**{step.agent}:** {step.thought}\n"
            summary += f"*Action:* {step.action}\n"
            summary += f"*Confidence:* {step.confidence:.0%}\n\n"
        
        return summary