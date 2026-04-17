# 🧠 Thinking Agent Integration Guide

## Overview

Your UI has been upgraded from a simple chatbot with static context to a **true thinking agent** with dynamic multi-agent orchestration. Here's what changed and how it works.

## What Was the Problem?

The original UI was essentially a fancy wrapper around a single LLM call with pre-loaded context:

```python
# OLD: Static context + single LLM call
system_context = build_full_context()  # Static prompt + all data
response = openai.chat.completions.create(
    messages=system_context + user_messages
)
```

This approach had several limitations:
- **No real reasoning** - just pattern matching on static context
- **No specialization** - one agent trying to do everything
- **No dynamic context** - same massive context for every query
- **No transparency** - user couldn't see the thinking process
- **Limited scalability** - context window fills up quickly

## What's the New Architecture?

The new system implements a **true multi-agent thinking architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                    THINKING AGENT                           │
│                  (Main Orchestrator)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                INTENT ANALYSIS                              │
│   • Determine query type (search/ideation/prediction)      │
│   • Extract key entities (journeys, metrics, tactics)      │
│   • Set processing mode and depth                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              DYNAMIC CONTEXT BUILDING                       │
│   • Focus context on query-relevant experiments            │
│   • Extract patterns specific to user's question           │
│   • Identify data gaps and uncertainties                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              SPECIALIST COORDINATION                        │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ KNOWLEDGE   │  │ IDEATION    │  │ PREDICTION  │         │
│  │ AGENT       │  │ AGENT       │  │ AGENT       │         │
│  │             │  │             │  │             │         │
│  │ • Search    │  │ • Generate  │  │ • Evaluate  │         │
│  │ • Analyze   │  │ • Structure │  │ • Risk      │         │
│  │ • Rank      │  │ • Ground    │  │ • Confidence│         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  ┌─────────────┐  ┌─────────────────────────────────────┐   │
│  │ INTAKE      │  │        REASONING AGENT              │   │
│  │ AGENT       │  │                                     │   │
│  │             │  │ • Meta-analysis                     │   │
│  │ • Structure │  │ • Conflict resolution               │   │
│  │ • Document  │  │ • Strategic synthesis               │   │
│  │ • Validate  │  │ • Quality assessment                │   │
│  └─────────────┘  └─────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                RESPONSE SYNTHESIS                           │
│   • Combine all specialist insights                        │
│   • Resolve conflicts and uncertainties                    │
│   • Format for immediate business use                      │
└─────────────────────────────────────────────────────────────┘
```

## Key Improvements

### 1. **Dynamic Context Building**
Instead of loading ALL experiment data for every query, the system now:
- Analyzes the user's question to understand intent
- Extracts key entities (journeys, site areas, metrics)
- Builds focused context with only relevant experiments
- Identifies patterns specific to the query

### 2. **Specialized Agents**
Each agent has a specific expertise:

**Knowledge Agent**: Historical experiment search and analysis
- Finds relevant experiments by journey, tactic, audience
- Ranks by relevance (direct/partial/weak analogs)
- Assesses evidence strength and confidence

**Ideation Agent**: New experiment concept generation
- Uses Empathize → Define → Ideate → Delivery framework
- Grounds ideas in historical precedent
- Structures for immediate implementation

**Prediction Agent**: Success probability assessment
- Analyzes historical patterns for similar experiments
- Identifies success factors and risks
- Provides calibrated confidence intervals

**Intake Agent**: JIRA-ready ticket creation
- Converts concepts into structured specifications
- Includes technical requirements and dependencies
- Ready for immediate handoff to dev teams

**Reasoning Agent**: Meta-analysis and synthesis
- Identifies patterns across all specialist analyses
- Resolves conflicts between different perspectives
- Provides strategic recommendations

### 3. **Transparent Thinking Process**
Users now see the agent's thinking in real-time:
```
🧠 Agent Coordination

🧠 Analyzing query intent...
Intent detected: Generate experiment ideas for wireless PDP
Mode: ideation
Key entities: wireless, PDP, conversion optimization

📊 Building dynamic context...
Context scope: Focused on wireless, PDP, trade-in optimization
Relevant experiments: 12
Key patterns: winning precedents, failure patterns

🤖 Coordinating specialist agents...
🔍 Knowledge Agent: Searching historical experiments...
💡 Ideation Agent: Generating experiment concepts...
📊 Prediction Agent: Evaluating success probability...
🧮 Reasoning Agent: Analyzing patterns and implications...

🔄 Synthesizing insights...
✅ Analysis complete
```

### 4. **Adaptive Processing**
The system automatically adapts its processing based on query type:
- **Search queries** → Focus on Knowledge + Reasoning agents
- **Ideation requests** → Full pipeline with emphasis on Ideation agent
- **Success prediction** → Knowledge + Prediction + Reasoning agents
- **Intake tickets** → All agents for comprehensive specification

## How to Use the New System

### 1. **Install Dependencies**
```bash
cd experimentation-agent-app
pip install -r requirements.txt
```

### 2. **Set Up Environment**
```bash
cp .env.example .env
# Add your OpenAI API key to .env
```

### 3. **Add Your Data**
Place your experiment data in the `documents/` folder:
- Excel export: `XTrack_Chat_Bot_export_2025-07-28T07_28_00.xlsx`
- Markdown inventory: `2025 att.com Experimentation Inventory.md`

### 4. **Launch the App**
```bash
./start.sh
# or
streamlit run app.py
```

### 5. **Try Different Query Types**

**Search Queries:**
- "What experiments have we run on the wireless PDP?"
- "Show me all trade-in optimization tests and their results"
- "Which experiments failed on the cart page and why?"

**Ideation Requests:**
- "Generate 3 experiment ideas for the internet buy flow"
- "What should we test next on the upgrade PDP?"
- "Create experiments to improve add-a-line conversion"

**Success Prediction:**
- "Would testing urgency messaging on checkout likely win?"
- "Evaluate the success probability of a simplified trade-in flow"
- "What are the risks of testing auto-select on the PDP?"

**Intake Tickets:**
- "Draft a JIRA ticket for testing social proof on plans page"
- "Create intake documentation for a mobile-first cart redesign"
- "Structure a test plan for personalized offer messaging"

## Technical Implementation Details

### Core Files

**`thinking_agent.py`** - Main orchestrator with specialist coordination
**`app.py`** - Streamlit UI with thinking agent integration
**`agent_config.py`** - Context building and data loading (unchanged)

### Key Classes

```python
class ThinkingAgent:
    def process_query(query, context, stream_callback):
        # 1. Analyze intent
        # 2. Build dynamic context  
        # 3. Coordinate specialists
        # 4. Synthesize response
        
class AgentResponse:
    content: str
    confidence: float
    reasoning: List[str]
    evidence: List[str]
    next_actions: List[str]
```

### Customization Points

**Add New Specialists:**
```python
def _custom_agent(self, query, context):
    # Implement your specialist logic
    return AgentResponse(...)
```

**Modify Intent Analysis:**
```python
def _analyze_intent(self, query):
    # Customize how queries are categorized
    # Add new modes or entity types
```

**Extend Context Building:**
```python
def _build_dynamic_context(self, query, context, intent):
    # Customize how context is filtered and focused
    # Add new data sources or filtering logic
```

## Performance Considerations

### Context Window Management
- Dynamic context building keeps token usage reasonable
- Only relevant experiments loaded per query
- Specialist agents work with focused subsets

### Response Time
- Parallel specialist processing where possible
- Streaming updates keep UI responsive
- Caching for repeated context builds

### Cost Optimization
- Smaller, focused prompts vs. massive context dumps
- Specialist agents use appropriate model sizes
- Intent analysis prevents unnecessary processing

## Monitoring and Debugging

### Thinking History
```python
agent.get_thinking_summary()  # See recent thinking steps
```

### Confidence Tracking
Each specialist provides confidence scores for their analysis

### Evidence Trails
All recommendations include source experiments and reasoning

## Next Steps

1. **Test with Real Queries** - Try the different query types above
2. **Customize Specialists** - Add domain-specific agents for your use cases
3. **Extend Data Sources** - Connect additional experiment databases
4. **Add Feedback Loops** - Track which recommendations get implemented
5. **Monitor Performance** - Watch response times and accuracy

## Troubleshooting

**"No module named 'openai'"**
```bash
pip install openai>=1.12.0
```

**"Context too large"**
- The dynamic context building should prevent this
- Check if your experiment data is extremely large
- Consider chunking large datasets

**"Thinking agent not responding"**
- Check API key configuration
- Verify model availability (gpt-4o recommended)
- Check network connectivity

**"Specialists returning empty results"**
- Verify experiment data is loaded correctly
- Check that context building finds relevant experiments
- Review intent analysis for proper query categorization

---

## Summary

You now have a **true thinking agent** instead of a simple chatbot. The system:

✅ **Thinks step-by-step** with transparent reasoning  
✅ **Specializes by domain** with expert agents  
✅ **Adapts dynamically** to different query types  
✅ **Builds focused context** instead of loading everything  
✅ **Provides actionable outputs** ready for business use  

The UI shows the thinking process in real-time, so users understand how conclusions were reached and can trust the recommendations.