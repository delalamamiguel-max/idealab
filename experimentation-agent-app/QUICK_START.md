# 🚀 Quick Start Guide - Thinking Agent

## 30-Second Setup

1. **Install Dependencies**
   ```bash
   cd experimentation-agent-app
   pip install streamlit openai pandas python-dotenv openpyxl
   ```

2. **Add Your API Key**
   ```bash
   cp .env.example .env
   echo "OPENAI_API_KEY=your_key_here" >> .env
   ```

3. **Launch the App**
   ```bash
   streamlit run app.py
   ```

4. **Test Without Dependencies**
   ```bash
   python3 simple_demo.py  # See the thinking process in action
   ```

## What Changed?

**Before:** Static chatbot with placeholder responses  
**After:** Multi-agent thinking system with real reasoning

## Try These Queries

**Ideation:**
- "Generate experiment ideas for wireless PDP conversion"
- "What should we test on the cart page?"

**Search:**
- "What trade-in experiments have we run?"
- "Show me all wireless PDP tests and results"

**Prediction:**
- "Would environmental messaging on trade-in likely win?"
- "Evaluate the success probability of auto-select features"

**Intake:**
- "Create a JIRA ticket for testing social proof on plans page"
- "Draft intake documentation for mobile-first redesign"

## What You'll See

Instead of a simple response, you'll see the thinking process:

```
🧠 Analyzing query intent...
📊 Building dynamic context...
🤖 Coordinating specialist agents...
🔍 Knowledge Agent: Searching historical experiments...
💡 Ideation Agent: Generating experiment concepts...
📊 Prediction Agent: Evaluating success probability...
🧮 Reasoning Agent: Analyzing patterns and implications...
🔄 Synthesizing insights...
✅ Analysis complete
```

Then you get actionable recommendations with:
- Success probability estimates
- Historical precedent
- Implementation details
- Risk assessments

## Files Added/Changed

- ✅ `thinking_agent.py` - Multi-agent orchestrator (NEW)
- ✅ `app.py` - Updated to use thinking agent
- ✅ `simple_demo.py` - Demo without dependencies (NEW)
- ✅ `THINKING_AGENT_INTEGRATION.md` - Full documentation (NEW)
- ✅ `TRANSFORMATION_SUMMARY.md` - Before/after comparison (NEW)

## Need Help?

1. **Dependencies issue?** Try `pip install -r requirements-simple.txt`
2. **API key not working?** Check your .env file has `OPENAI_API_KEY=sk-...`
3. **Want to see it work first?** Run `python3 simple_demo.py`

**You now have a true thinking agent instead of a chatbot!** 🧠✨