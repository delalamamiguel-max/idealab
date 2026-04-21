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
├── agent_config.py                  # System prompt + Excel data parser + market intel loader
├── thinking_agent.py                # Multi-agent orchestrator with market intel integration
├── requirements.txt                 # Python dependencies
├── start.sh                         # One-click startup script
├── .env.example                     # Environment config template
├── .gitignore                       # Git ignore rules
├── README.md                        # This file
├── KNOWLEDGE_LAYER_GUIDE.md         # How the Knowledge Layer uses 2025 data
├── 2025_EXPERIMENTS_QUICK_REFERENCE.md  # Summary of all 55 experiments
├── .streamlit/
│   └── config.toml                  # Streamlit theme & server config
├── documents/
│   ├── XTrack_Chat_Bot_export_2025-07-28T07_28_00.xlsx   # 55 experiments, 41 fields
│   └── Optimization Concept Intake Guide.pdf
├── telecom_intel/                   # 📡 Market Intelligence Pipeline
│   ├── __init__.py                  # Package exports
│   ├── models.py                    # Data models (MarketSignal, ClassifiedSignal, etc.)
│   ├── config.py                    # URLs, subreddits, Apify config
│   ├── ingestion_agent.py           # Apify scraper (websites + Reddit)
│   ├── classification_agent.py      # LLM-powered signal classification
│   ├── reasoning_agent.py           # Cross-signal pattern detection + insights
│   ├── pipeline.py                  # Full pipeline orchestrator (4 modes — see below)
│   └── output/                      # Auto-created: raw data, signals, insights, cache
│       ├── raw/                     # Includes web_search_signals_*.json files
│       ├── signals/
│       └── insights/
└── output/                          # Generated experiment briefs
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
| `APIFY_API_TOKEN` | *(optional)* | Apify API token for live scraping mode (not required for `web_search` mode) |
| `APIFY_BASE_URL` | `https://api.apify.com/v2` | Apify API base URL |
| `CLASSIFICATION_MODEL` | `gpt-4o-mini` | Model for signal classification (cost-optimized) |
| `SIGNAL_CACHE_TTL` | `3600` | How long cached signals remain valid (seconds) |

### Pipeline Modes

The Telecom Intel Pipeline supports four ingestion modes:

| Mode | Description | Requires Apify? | Requires Network? |
|------|-------------|-----------------|--------------------|
| `web_search` | **Recommended.** Loads real signals from `web_search_signals_*.json` files in `telecom_intel/output/raw/`. Data is collected externally via web search and saved to disk. | ❌ No | ❌ No |
| `live` | Runs Apify Website Content Crawler + Reddit Scraper in real time. | ✅ Yes | ✅ Yes (api.apify.com) |
| `cached` | Loads most recent classified signals from disk. Skips ingestion + classification. | ❌ No | ❌ No |
| `dry_run` | Uses hardcoded sample data. **For development/testing only — data is synthetic.** | ❌ No | ❌ No |

> ⚠️ **Corporate network note:** If your firewall blocks `api.apify.com` (common on VPN), use `web_search` mode. It produces the same pipeline output from real data without any Apify dependency.

### Runtime Settings (Sidebar)

All settings can also be adjusted in the app sidebar without restarting:
- API Key
- Model selection
- Temperature slider
- **Market Intelligence toggle** — enable/disable competitive signals
- **Data source** — web search signals, cached signals, live Apify scrape, or sample data
- **LLM Classification** — toggle between LLM and keyword-fallback classification

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

**Market-Driven (with Market Intel enabled):**
> "Based on current market signals from competitors, what experiments should we prioritize?"

> "T-Mobile just dropped their plan prices — what defensive experiments should we run?"

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

The agent uses a **multi-agent orchestration pattern** with two integrated data pipelines:

```
User Query
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│              ThinkingAgent (Multi-Agent Orchestrator)             │
│                                                                  │
│  Intent Analysis → Dynamic Context → Subagent Coordination       │
└────────┬─────────────────────────────────────────────────────────┘
         │
    ┌────┴────┬──────────┬──────────┬──────────┬──────────────┐
    ▼         ▼          ▼          ▼          ▼              ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Knowledge│ │Ideation│ │Predict │ │ Intake │ │Market  │ │Reason- │
│ Agent  │ │ Agent  │ │ Agent  │ │ Agent  │ │ Intel  │ │  ing   │
└───┬────┘ └────────┘ └────────┘ └────────┘ └───┬────┘ └────────┘
    │                                            │
    ▼                                            ▼
┌──────────────────────┐          ┌──────────────────────────────┐
│  INTERNAL KNOWLEDGE   │          │  EXTERNAL MARKET SIGNALS     │
│                       │          │                              │
│  55 experiments       │          │  📡 Telecom Intel Pipeline   │
│  2025 XTrack Export   │          │                              │
│  41 fields per test   │          │  Ingestion → Classification  │
│  Win/loss patterns    │          │       → Reasoning            │
│  Historical lifts     │          │                              │
│                       │          │  Sources:                    │
│  Source: Excel        │          │  • T-Mobile, Verizon sites   │
│                       │          │  • Reddit communities        │
│                       │          │  • Plan changelogs           │
│                       │          │  • Software update pages     │
│                       │          │                              │
│                       │          │  Classification: LLM-powered │
│                       │          │  (GPT-4o-mini)               │
└──────────────────────┘          └──────────────────────────────┘
```

### Data Pipelines

**Internal (Historical Experiments):**
- 55 experiments from 2025 XTrack export
- Searchable by journey, site area, metrics, audience, results, capability focus
- Primary source for all recommendations and analogs

**External (Market Intelligence):**
- Competitive signals from **web search** (primary) or **Apify scrapers** (when network allows)
- `web_search` mode loads real, sourced signals from JSON files on disk — no Apify or network dependency
- `live` mode uses Apify Website Content Crawler + Reddit Scraper (requires `api.apify.com` access)
- LLM-powered classification (with keyword fallback when no OpenAI key)
- Signal types: pricing, outage, software_update, customer_sentiment, policy_change, competitive_move, churn_signal
- Cross-signal reasoning generates actionable insights with experiment recommendations

### How They Work Together

When Market Intelligence is enabled, the agent sees **both worlds**:
- Historical experiments tell it *what AT&T has tried and what worked*
- Market signals tell it *what competitors are doing right now*
- The Reasoning Agent synthesizes both into market-aware experiment recommendations

Example: "T-Mobile dropped pricing → Reddit shows AT&T churn mentions → Historical data shows value-surfacing experiments win → **Recommend:** Test competitive price-match messaging on wireless PDP"

### Web Search Mode — How It Works

When Apify is blocked (e.g. corporate firewall), the pipeline uses pre-collected web search data:

```
External Web Search (runs outside corporate network)
    │
    ▼
telecom_intel/output/raw/web_search_signals_YYYYMMDD.json   ← real, sourced signals
    │
    ▼
┌──────────────────────────────────────────────────────────┐
│  Pipeline (mode='web_search')                            │
│                                                          │
│  1. Load signals from JSON          (no Apify needed)    │
│  2. Classification Agent            (LLM or keyword)     │
│  3. Reasoning Agent                 (pattern detection)  │
│  4. → Insights + experiment recs                         │
└──────────────────────────────────────────────────────────┘
```

The JSON files contain the same data Apify would scrape — competitor pricing pages, Reddit posts, news articles — collected from the same approved sources listed in `config.py`. Every signal includes a `source_citation` field for audit.

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
