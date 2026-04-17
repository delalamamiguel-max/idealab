#!/usr/bin/env python3
"""
Demo script for the Thinking Agent - shows how it works without Streamlit UI.

This demonstrates the thinking agent's capabilities with mock data,
so you can see the multi-agent coordination in action.
"""

import json
import time
from typing import Dict, Any
from unittest.mock import Mock

# Mock OpenAI responses for demo purposes
MOCK_RESPONSES = {
    "intent_analysis": {
        "mode": "ideation",
        "description": "Generate experiment ideas for wireless PDP optimization",
        "entities": ["wireless", "PDP", "conversion", "trade-in"],
        "business_objective": "Improve wireless device purchase conversion",
        "analysis_depth": "detailed"
    },
    
    "dynamic_context": """
    RELEVANT EXPERIMENTS FOR WIRELESS PDP:
    
    Experiment #4199564: Auto-Select Trade-In on Upgrade PDP
    - Journey: Wireless Buyflow
    - Site Area: PDP  
    - Result: LOSS (-5.63%)
    - Learning: Customers resisted auto-assumptions; they want control
    
    Experiment #4506369: Trade-in for Trees
    - Journey: Wireless Buyflow
    - Site Area: PDP
    - Result: WIN (+0.74%)
    - Learning: Do-no-harm learning on 19.1M DUVs; environmental messaging works
    
    Experiment #4367400: CTO for 3+ Line Porters
    - Journey: Wireless Buyflow
    - Site Area: PDP
    - Result: WIN (+18.96%)
    - Learning: Human-assist escape valve increases OSA calls without cannibalizing online
    """,
    
    "knowledge_agent": """
    ## Historical Analysis - Wireless PDP Experiments
    
    **Direct Analogs Found:** 3 experiments
    
    **Key Patterns:**
    - Auto-assumptions fail: Auto-selecting trade-in reduced conversion by 5.63%
    - Environmental messaging works: Trade-in for Trees achieved +0.74% lift
    - Human assistance helps: CTO for porters achieved +18.96% lift
    
    **Evidence Strength:** HIGH - Multiple direct PDP experiments available
    **Confidence:** 85%
    """,
    
    "ideation_agent": """
    ## Experiment Ideas for Wireless PDP
    
    ### Idea 1: Smart Trade-In Recommendation Engine
    **Empathize:** Customers want trade-in value but don't want assumptions made for them
    **Define:** If we show personalized trade-in value with clear opt-in, then more customers will engage because they feel in control
    **Ideate:** 
    - Control: Current trade-in flow
    - Variant: AI-powered trade-in value estimator with clear "Add Trade-In" CTA
    **Delivery:** Medium effort, requires ML integration
    
    ### Idea 2: Environmental Impact Messaging
    **Empathize:** Customers care about sustainability but need gentle nudging
    **Define:** If we show environmental impact of trade-in, then more customers will participate because they feel good about the choice
    **Ideate:**
    - Control: Standard trade-in messaging
    - Variant: "Trade-in for Trees" style environmental impact messaging
    **Delivery:** Low effort, copy and design changes only
    
    ### Idea 3: Human-Assist for Complex Scenarios
    **Empathize:** Port-in customers face complex decisions and need help
    **Define:** If we offer human assistance for complex scenarios, then conversion improves because customers get expert help
    **Ideate:**
    - Control: Self-service only
    - Variant: "Need help? Chat with an expert" CTA for port-in customers
    **Delivery:** Medium effort, requires chat integration
    """,
    
    "prediction_agent": """
    ## Success Probability Analysis
    
    **Idea 1 - Smart Trade-In:** 65% success probability
    - Historical precedent: Trade-in optimization has mixed results
    - Risk: Technical complexity might delay launch
    - Success factors: Personalization + customer control
    
    **Idea 2 - Environmental Messaging:** 80% success probability  
    - Historical precedent: Trade-in for Trees achieved +0.74%
    - Risk: Low - copy-only change
    - Success factors: Proven messaging approach
    
    **Idea 3 - Human Assist:** 75% success probability
    - Historical precedent: CTO for porters achieved +18.96%
    - Risk: Operational complexity
    - Success factors: Proven pattern for complex scenarios
    
    **Overall Confidence:** 73% - Strong historical precedent available
    """,
    
    "reasoning_agent": """
    ## Strategic Analysis
    
    **Key Insights:**
    1. Customer control is critical - auto-assumptions consistently fail
    2. Environmental messaging is a proven winner for trade-in
    3. Human assistance works well for complex scenarios
    
    **Recommended Priority:**
    1. Environmental messaging (low risk, proven pattern)
    2. Human assist for port-in (high impact potential)
    3. Smart trade-in (higher complexity but good upside)
    
    **Strategic Implications:**
    - Focus on customer empowerment vs. automation
    - Leverage environmental consciousness as conversion driver
    - Invest in human-digital hybrid experiences
    """,
    
    "final_synthesis": """
    # Wireless PDP Optimization Strategy
    
    Based on analysis of 3 direct historical analogs and multi-agent evaluation, here are the recommended experiments:
    
    ## 🏆 Priority 1: Environmental Trade-In Messaging
    **Success Probability:** 80%
    **Effort:** Low
    **Historical Precedent:** Trade-in for Trees (+0.74% on 19.1M DUVs)
    
    **Recommendation:** Test environmental impact messaging for trade-in program
    - Control: Standard "Get up to $X for your device"
    - Variant: "Trade-in for Trees: Get up to $X and help plant trees"
    - Primary Metric: Trade-in attachment rate
    - Expected Impact: +0.5% to +1.0% lift
    
    ## 🥈 Priority 2: Human-Assist for Port-In
    **Success Probability:** 75%  
    **Effort:** Medium
    **Historical Precedent:** CTO for 3+ Line Porters (+18.96%)
    
    **Recommendation:** Add human assistance option for port-in customers
    - Control: Self-service port-in flow
    - Variant: "Switching carriers? Chat with an expert" CTA
    - Primary Metric: Port-in completion rate
    - Expected Impact: +5% to +15% lift for port-in segment
    
    ## 🥉 Priority 3: Smart Trade-In Recommendations
    **Success Probability:** 65%
    **Effort:** High
    **Historical Precedent:** Mixed results, but customer control is key
    
    **Recommendation:** AI-powered trade-in value with clear opt-in
    - Control: Current trade-in flow
    - Variant: Personalized trade-in value with "Add to Cart" CTA
    - Primary Metric: Trade-in attachment rate
    - Expected Impact: +1% to +3% lift (if executed well)
    
    ## Key Success Factors
    ✅ Maintain customer control - no auto-assumptions  
    ✅ Leverage environmental consciousness  
    ✅ Provide human assistance for complex scenarios  
    ✅ Use proven messaging patterns from historical wins  
    
    ## Next Steps
    1. Start with environmental messaging (quick win)
    2. Develop human-assist capability for port-in
    3. Prototype smart trade-in recommendations
    4. Monitor results and iterate based on learnings
    """
}

class MockOpenAIClient:
    """Mock OpenAI client that returns predefined responses for demo."""
    
    def __init__(self):
        self.call_count = 0
        self.response_map = {
            0: MOCK_RESPONSES["intent_analysis"],
            1: MOCK_RESPONSES["dynamic_context"], 
            2: MOCK_RESPONSES["knowledge_agent"],
            3: MOCK_RESPONSES["ideation_agent"],
            4: MOCK_RESPONSES["prediction_agent"],
            5: MOCK_RESPONSES["reasoning_agent"],
            6: MOCK_RESPONSES["final_synthesis"]
        }
    
    @property
    def chat(self):
        return self
    
    @property 
    def completions(self):
        return self
        
    def create(self, **kwargs):
        """Return mock response based on call order."""
        response_content = self.response_map.get(self.call_count, "Mock response")
        
        # For intent analysis, return JSON
        if self.call_count == 0:
            response_content = json.dumps(response_content)
        
        self.call_count += 1
        
        # Create mock response object
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = response_content
        
        return mock_response

def demo_thinking_agent():
    """Demonstrate the thinking agent with mock data."""
    
    print("🧪 Thinking Agent Demo")
    print("=" * 50)
    print()
    
    # Import the thinking agent
    try:
        from thinking_agent import ThinkingAgent
    except ImportError:
        print("❌ Could not import ThinkingAgent. Make sure thinking_agent.py is in the current directory.")
        return
    
    # Create mock client and thinking agent
    mock_client = MockOpenAIClient()
    agent = ThinkingAgent(mock_client, model="gpt-4o", temperature=0.4)
    
    # Demo query
    query = "Generate 3 experiment ideas for the wireless PDP to improve conversion"
    context = """
    Historical experiment data with 55 experiments across wireless, wireline, 
    and account management journeys. Key patterns include successful environmental
    messaging, failed auto-assumptions, and winning human-assist strategies.
    """
    
    print(f"**User Query:** {query}")
    print()
    print("**Processing with Thinking Agent...**")
    print()
    
    # Track thinking steps
    thinking_steps = []
    
    def demo_stream_callback(text):
        """Capture thinking steps for demo."""
        thinking_steps.append(text)
        print(text, end="", flush=True)
        time.sleep(0.5)  # Simulate processing time
    
    # Process the query
    try:
        result = agent.process_query(
            query=query,
            context=context, 
            stream_callback=demo_stream_callback
        )
        
        print("\n" + "=" * 50)
        print("🎯 FINAL RESULT")
        print("=" * 50)
        print()
        print(result)
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return
    
    print("\n" + "=" * 50)
    print("📊 DEMO SUMMARY")
    print("=" * 50)
    print()
    print("✅ Successfully demonstrated multi-agent thinking process")
    print(f"✅ Processed {len(thinking_steps)} thinking steps")
    print("✅ Generated actionable experiment recommendations")
    print("✅ Showed transparent reasoning with historical grounding")
    print()
    print("This is what your users will see when they interact with the")
    print("thinking agent through the Streamlit UI!")

if __name__ == "__main__":
    demo_thinking_agent()