# 🧪 Experimentation Agent

A conversational CRO (Conversion Rate Optimization) intelligence system that helps teams search historical experiments, generate new test ideas, predict experiment success, and draft intake-ready tickets — all grounded in your real experiment data.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green)

---

## ✨ What It Does

| Capability | Description |
|---|---|
| 🔍 **Search** | Find past experiments by topic, site area, metric, audience, or outcome |
| 💡 **Ideate** | Generate new experiment ideas grounded in historical evidence |
| 📊 **Predict** | Evaluate whether a proposed test is likely to succeed |
| 📝 **Draft** | Create JIRA-ready intake tickets with full hypothesis and measurement plans |
| 🏆 **Prioritize** | Rank ideas by business impact, effort, and historical precedent |

The agent automatically loads your **2025 XTrack experiment export** (55 experiments, 41 fields) and uses it to ground every recommendation in real evidence — not generic best practices.

**Knowledge Layer Data Source:** Your complete 2025 experiment dataset is the foundation for all searches, analogs, and recommendations. See `2025_EXPERIMENTS_QUICK_REFERENCE.md` for a summary of top wins, losses, and opportunities.

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.10+** — [Download here](https://www.python.org/downloads/)
- **OpenAI API Key** — [Get one here](https://platform.openai.com/api-keys)

### 2. Install

```bash
# Clone or navigate to the project
cd experimentation-agent-app

# Install dependencies
python3 -m pip install -r requirements.txt
```

### 3. Configure

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
open .env   # or use your preferred editor
```

Set your key in `.env`:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 4. Run

```bash
# Option A: Use the startup script
./start.sh

# Option B: Run directly
python3 -m streamlit run app.py
```

Open your browser to **http://localhost:8501** — the agent is ready.

---

## 📁 Project Structure

```
experimentation-agent-app/
├── app.py                           # Streamlit chat application
├── agent_config.py                  # System prompt + Excel data parser
├── requirements.txt                 # Python dependencies
├── start.sh                         # One-click startup script
├── .env.example                     # Environment config template
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
├── KNOWLEDGE_LAYER_GUIDE.md         # How the Knowledge Layer uses 2025 data
├── 2025_EXPERIMENTS_QUICK_REFERENCE.md  # Summary of all 55 experiments
├── .streamlit/
│   └── config.toml                  # Streamlit theme & server config
└── documents/
    ├── XTrack_Chat_Bot_export_2025-07-28T07_28_00.xlsx   # 55 experiments, 41 fields
    └── Optimization Concept Intake Guide.pdf
```

---

## 📊 Loading Your Own Data

The agent reads experiment data from the Excel file in the `/documents` folder.

### Supported Fields

The parser automatically detects and uses these columns (all optional — it uses whatever is available):

| Field | Description |
|---|---|
| Reference Number | Unique experiment ID |
| Name | Experiment title |
| Description | What was tested |
| Status | Complete, In Analysis, Pending, etc. |
| Testing Hypothesis | The falsifiable hypothesis |
| Test Results | Win, Loss, None, N/A |
| Lift Measurement | Numeric lift percentage |
| Primary Metrics | Main success metric |
| Secondary Metrics | Supporting metrics |
| Impacted Journey | Wireless Buyflow, Wireline, Account Mgmt, etc. |
| Technical Site Area | PDP, Cart, Config, Plans, etc. |
| Learnings & Opportunities | Post-test insights |
| Audience Definition | Who was targeted |
| Estimated Value | Dollar impact estimate |
| Tags | Categorization labels |

### Updating the Data

1. Export your latest experiment data from XTrack (or your tracking tool)
2. Save the `.xlsx` file to the `/documents` folder
3. Update the filename in `agent_config.py` line 18 (`EXCEL_FILE = ...`) if the name changed
4. Restart the app — the new data loads automatically

---

## ⚙️ Configuration

### Environment Variables (`.env`)

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | *(required)* | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o` | Model to use (`gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-3.5-turbo`) |
| `OPENAI_TEMPERATURE` | `0.4` | Response creativity (0.0–1.0) |

### Runtime Settings (Sidebar)

All settings can also be adjusted in the app sidebar without restarting:
- API Key
- Model selection
- Temperature slider

---

## 💬 Example Prompts

**Search:**
> "What experiments have we run on the wireless PDP? What worked and what didn't?"

**Ideation:**
> "Generate 3 new experiment ideas for the internet buy flow based on our winning patterns."

**Prediction:**
> "Would an A/B test adding urgency messaging to the cart page likely win?"

**Intake Drafting:**
> "Draft a JIRA-ready intake ticket for testing a simplified trade-in flow on the upgrade PDP."

**Analysis:**
> "Which lines of business perform best in experimentation? Where should I invest?"

**Cross-reference:**
> "Recommend an experiment for the add-a-line flow based on insights from our top 3 winning experiments."

---

## 🌐 Deployment Options

### Local (Default)
```bash
./start.sh
```

### Streamlit Cloud (Free)
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set `app.py` as the main file
4. Add your `OPENAI_API_KEY` in Streamlit Cloud's Secrets management
5. Deploy — your team gets a shareable URL

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
```

```bash
docker build -t experimentation-agent .
docker run -p 8501:8501 --env-file .env experimentation-agent
```

---

## 🏗️ Architecture

The agent uses a **multi-agent orchestration pattern** internally:

```
User Query
    │
    ▼
┌─────────────────────────────────────────┐
│  Experimentation Agent (Orchestrator)   │  ← Main orchestrator (speaks to user)
└────────┬────────────────────────────────┘
         │
    ┌────┴────┬──────────┬──────────────┐
    ▼         ▼          ▼              ▼
┌────────┐ ┌────────┐ ┌──────────┐ ┌────────┐
│Knowledge│ │Reasoning│ │  Skill   │ │ Output │
│ Layer  │ │ Layer  │ │ Modules  │ │ Layer  │
└────────┘ └────────┘ └──────────┘ └────────┘
    ▲
    │
    └─ Powered by: 2025 XTrack Export
       (55 experiments, 41 fields)
       ├─ Impacted Journey
       ├─ Technical Site Area
       ├─ Test Results & Lift
       ├─ Primary/Secondary Metrics
       ├─ Audience Definition
       ├─ Learnings & Opportunities
       └─ Capability Focus Area
                          │
                    ┌─────┼─────┬──────────┐
                    ▼     ▼     ▼          ▼
                 Search  Ideate  Predict  Intake
```

**Knowledge Layer** retrieves and ranks experiments from your 2025 data using these search dimensions:
- Journey (Wireless, Wireline, Account Mgmt, Converged, etc.)
- Site Area (PDP, Cart, Config, Plans, Homepage, etc.)
- Metrics (Progression, POCR, Clicks, Sales, CVR, OSA calls, etc.)
- Audience (Consumer, IRU, SMB, CaaS, FirstNet, etc.)
- Results (Win, Loss, None, N/A)
- Capability Focus (Trade-in, Plans, Offers, AiA, Port-in, Add-a-Line, etc.)

All subagents are orchestrated within a single LLM call via structured prompting — no separate API calls per subagent. This keeps latency low and costs manageable.

---

## 📝 License

Internal use. Not for external distribution.

---

## 🤝 Contributing

To extend the agent:

1. **Add new skill modules** — Edit the system prompt in `agent_config.py` to add new capabilities
2. **Add new data sources** — Extend `load_historical_experiments()` to parse additional files
3. **Customize the UI** — Modify `app.py` styling and layout
4. **Add authentication** — Use Streamlit's built-in auth or add a password gate

---

*Built with the Experimentation Agent system — making experiment search, ideation, prioritization, and intake dramatically faster.*
