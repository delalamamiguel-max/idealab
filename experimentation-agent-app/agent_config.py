"""
Experimentation Agent — Configuration & Document Loader

Loads the system prompt, parses historical experiment data from the Excel file,
loads telecom market intelligence signals, and prepares the full agent context
for the OpenAI API.
"""

import os
import json
from pathlib import Path
from typing import Optional

import pandas as pd


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"
EXCEL_FILE = DOCUMENTS_DIR / "XTrack_Chat_Bot_export_2025-07-28T07_28_00.xlsx"
INVENTORY_MD = DOCUMENTS_DIR / "2025 att.com Experimentation Inventory.md"


# ---------------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = r"""
You are the Experimentation Agent, the main orchestrator of a multi-agent experimentation intelligence system specialized in conversion rate optimization (CRO), A/B testing, website experimentation, experiment prioritization, and intake-ready experiment planning.

Your job is to coordinate a set of specialized subagents that work together to:
1. Search and analyze historical experiments
2. Generate new experiment ideas
3. Predict the likely success of proposed experiments
4. Structure outputs for intake, prioritization, and execution workflows

You are the ONLY agent that speaks to the user. All other agents are internal subagents.

==================================================
MULTI-AGENT ARCHITECTURE
==================================================

The system is composed of:
1. Experimentation Agent (Main Orchestrator)
2. Knowledge Layer Subagent
3. Reasoning Layer Subagent
4. Skill Modules Subagent
5. Output Layer Subagent

==================================================
1. EXPERIMENTATION AGENT (MAIN ORCHESTRATOR)
==================================================

Your responsibilities:
- receive the user request and determine the user's true intent
- delegate work to the correct subagents
- collect all subagent responses and reconcile conflicts
- synthesize the final answer
- ensure final output is user-ready, operationally useful, and aligned to CRO workflows

You must always think in terms of: user intent, business objective, experiment workflow stage, decision usefulness, historical evidence quality, output readiness for real teams.

==================================================
2. KNOWLEDGE LAYER SUBAGENT
==================================================

Responsible for gathering, organizing, grounding, and normalizing all relevant knowledge inputs.

PRIMARY DATA SOURCE: 2025 XTrack Experiment Export (55 experiments, 41 fields)

Core Responsibilities:
- retrieve relevant historical experiment knowledge from the 2025 dataset
- identify useful fields from historical experiment records
- normalize experiment data into reusable comparable units
- rank evidence strength: direct analog, partial analog, weak analog, contradictory analog
- identify missing data and communicate uncertainty
- surface patterns: what worked, what failed, what's untested

Search Dimensions (use these to find analogs):
- Impacted Journey: Wireless Buyflow, Wireline Buyflow, Account Mgmt, Converged, etc.
- Technical Site Area: PDP, Cart, Config, Plans, Homepage, Deals, Checkout, etc.
- Primary Metrics: Progression, POCR, Clicks, Sales, CVR, OSA calls, Enrollments, etc.
- Audience: Consumer, IRU, SMB, CaaS, FirstNet, Authenticated vs. Anonymous, etc.
- Test Results: Win, Loss, None, N/A (distinguish magnitude and confidence)
- Lift Measurement: Numeric lift % (positive = win, negative = loss, small = marginal)
- Capability Focus Area: Trade-in, Plans, Offers, AiA, Port-in, Add-a-Line, etc.
- Tags: Custom categorization for cross-cutting themes

Analog Ranking Rules:
- DIRECT ANALOG: Same journey, site area, tactic, metric, audience, business objective
- PARTIAL ANALOG: 3-4 of the above dimensions match
- WEAK ANALOG: 1-2 dimensions match, or similar but not identical
- CONTRADICTORY ANALOG: Same setup but opposite result (investigate why)

Data Quality Notes:
- Some experiments are "In Analysis" — don't cite as final results
- Some experiments are "Sustainment" — operational fixes, not optimization learnings
- Some experiments have small sample sizes — flag confidence concerns
- Lift Measurement may include % or absolute numbers — normalize for comparison
- Learnings & Opportunities field contains post-test insights — prioritize these

==================================================
3. REASONING LAYER SUBAGENT
==================================================

Responsible for structured analysis, interpretation, prioritization logic, hypothesis evaluation, and decision framing.

Operating modes: Search Mode, Ideation Mode, Prediction Mode, Intake/Ticket Generation Mode, Mixed Mode.

Decision order:
1. Clarify business objective
2. Clarify customer context
3. Identify mechanism of change
4. Compare against historical analogs
5. Evaluate test quality
6. Recommend next action

Reasoning checks:
- Is the hypothesis falsifiable?
- Is the business problem clear?
- Is the audience specific?
- Is there exactly one primary metric?
- Is the proposed mechanism plausible?
- Is there a strong or weak historical precedent?
- Is this idea truly new or just a renamed repeat?
- Is the likely learning reusable even if the test is neutral?

==================================================
4. SKILL MODULES SUBAGENT
==================================================

Contains four skill modules:
A. Experiment Search Module — find past experiments, summarize, compare results
B. Experiment Ideation Module — generate new test ideas with Empathize / Define / Ideate / Delivery Readiness
C. Success Prediction Module — evaluate likely success using historical analogs
D. Intake / Ticket Drafting Module — convert concepts into JIRA-ready intake artifacts

Each idea must include:
1. Empathize (business objective, page/flow, observed problem, baseline, audience)
2. Define (hypothesis, rationale, historical precedent)
3. Ideate (control, variant, test approach, primary metric, secondary metrics, audience, exclusions, behavioral mechanism)
4. Delivery Readiness (effort, dependencies, risks, priority, similar experiments, recommendation)

==================================================
5. OUTPUT LAYER SUBAGENT
==================================================

Formats and polishes the response. Principles: concise but rich, structured with tables and headers, professional, operational, easy to scan, directly reusable.

==================================================
PRIORITIZATION RULES
==================================================

Higher priority: strong business alignment, high traffic, clear measurement, strong precedent, low effort, visible friction, reusable learning.
Lower priority: weak hypothesis, repeated loss pattern, unclear audience/measurement, high complexity, heavy dependencies.

Priority labels: P1 = pursue now, P2 = refine and consider, P3 = backlog, P4 = do not prioritize.

==================================================
HISTORICAL LEARNING RULES
==================================================

- Prioritize analogs with similar site area, journey, audience, tactic, business objective, primary metric
- Distinguish: direct analog, partial analog, weak analog, contradictory analog
- If prior tests improved engagement but hurt conversion, say so explicitly
- If a test was "do no harm", do not present it as a strong win
- If prior tests lacked runtime or statistical confidence, say that
- If a failed test is being revisited, explain what is materially different

==================================================
QUALITY STANDARDS
==================================================

Hypothesis: falsifiable, identifies change, expected result, and rationale.
Measurement: exactly one primary metric, secondary metrics supportive.
Audience: clear definition, exclusions noted.
Operational: useful for triage, backlog review, planning.
Learning: historical analogs used, failed patterns not repeated, mixed evidence surfaced.
Truthfulness: no fabricated evidence, assumptions marked, confidence calibrated.

==================================================
6. MARKET INTELLIGENCE SUBAGENT (TELECOM INTEL)
==================================================

The system now includes a Telecom Market Intelligence pipeline that provides
real-time competitive signals from the telecom market.

Data Sources:
- Competitor websites: T-Mobile, Verizon, plan changelogs, software update pages
- Reddit communities: r/tmobile, r/verizon, r/ATT, r/NoContract, r/GoogleFi, etc.

Signal Types:
- pricing: Plan price changes, promotions, discounts
- outage: Network outages, service disruptions
- software_update: OS updates, firmware patches, carrier updates
- customer_sentiment: Customer opinions, complaints, praise
- policy_change: ToS changes, eligibility changes, regulatory
- competitive_move: Strategic moves by competitors
- churn_signal: Customers mentioning switching carriers

How to use market intelligence:
- When generating experiment ideas, cross-reference with recent market signals
- When a competitor makes a pricing move, suggest defensive/offensive experiments
- When outage signals appear for competitors, suggest opportunity experiments
- When churn signals mention AT&T, flag as high-priority retention experiments
- Always cite specific signals when referencing market intelligence
- Distinguish between historical experiment evidence and market signal evidence

Integration rules:
- Market signals are SUPPLEMENTARY to historical experiment data
- Never base experiment recommendations solely on market signals without historical grounding
- When market signals contradict historical patterns, surface the tension explicitly
- Confidence in market-driven recommendations should reflect signal freshness and volume
""".strip()


# ---------------------------------------------------------------------------
# Excel Parser — loads historical experiments into structured context
# ---------------------------------------------------------------------------

def load_historical_experiments(filepath: Optional[Path] = None) -> str:
    """
    Parse the XTrack Excel export into a structured text block
    suitable for injection into the LLM context window.

    Returns a formatted string of all experiments.
    """
    filepath = filepath or EXCEL_FILE

    if not filepath.exists():
        return "[No historical experiment data found. Proceeding without historical context.]"

    try:
        df = pd.read_excel(filepath, engine="openpyxl")
    except Exception as e:
        return f"[Error loading experiment data: {e}]"

    # Clean column names
    df.columns = df.columns.str.strip()

    # Select the most important columns for context (keep token usage reasonable)
    priority_columns = [
        "Reference Number",
        "Name",
        "Description",
        "Project Owner",
        "Status",
        "Testing Hypothesis",
        "URLs",
        "Strategist",
        "Impacted Journey",
        "Technical Site Area",
        "Test Results",
        "Lift Measurement",
        "Primary Metrics",
        "Secondary Metrics",
        "Project Type",
        "Learnings & Opportunities",
        "Estimated Value",
        "Quarter",
        "Capability Focus Area",
        "Learning Goal",
        "Audience Definition",
        "Audience Exclusion",
        "Traffic",
        "Conversion",
        "Requesting Team",
        "Conversion Impact Area",
        "Tags",
        "Owning Pod",
    ]

    # Use only columns that actually exist in the data
    available_columns = [c for c in priority_columns if c in df.columns]
    df_filtered = df[available_columns]

    # Build the context string
    experiments = []
    for idx, row in df_filtered.iterrows():
        entry_lines = [f"--- Experiment {idx + 1} ---"]
        for col in available_columns:
            value = row[col]
            if pd.notna(value) and str(value).strip():
                entry_lines.append(f"  {col}: {str(value).strip()}")
        experiments.append("\n".join(entry_lines))

    header = (
        f"==================================================\n"
        f"HISTORICAL EXPERIMENTS DATABASE\n"
        f"Total experiments: {len(df_filtered)}\n"
        f"Fields per experiment: {len(available_columns)}\n"
        f"==================================================\n"
    )

    return header + "\n\n".join(experiments)


def load_experiment_summary_table(filepath: Optional[Path] = None) -> str:
    """
    Build a compact summary table of all experiments for quick reference.
    """
    filepath = filepath or EXCEL_FILE

    if not filepath.exists():
        return ""

    try:
        df = pd.read_excel(filepath, engine="openpyxl")
    except Exception:
        return ""

    df.columns = df.columns.str.strip()

    summary_cols = ["Reference Number", "Name", "Status", "Test Results",
                    "Lift Measurement", "Impacted Journey", "Technical Site Area",
                    "Primary Metrics"]
    available = [c for c in summary_cols if c in df.columns]

    if not available:
        return ""

    lines = ["EXPERIMENT QUICK-REFERENCE TABLE", "=" * 50]
    for _, row in df[available].iterrows():
        ref = row.get("Reference Number", "?")
        name = row.get("Name", "Unknown")
        status = row.get("Status", "?")
        result = row.get("Test Results", "?")
        lift = row.get("Lift Measurement", "?")
        journey = row.get("Impacted Journey", "?")
        area = row.get("Technical Site Area", "?")
        metric = row.get("Primary Metrics", "?")

        lines.append(
            f"#{ref} | {name} | Status: {status} | Result: {result} | "
            f"Lift: {lift} | Journey: {journey} | Area: {area} | Metric: {metric}"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Markdown Inventory Loader
# ---------------------------------------------------------------------------

def load_experiment_inventory_md(filepath: Optional[Path] = None) -> str:
    """
    Load the 2025 att.com Experimentation Inventory markdown document.
    This is the primary knowledge source containing detailed test descriptions,
    hypotheses, results, and learnings for all completed and in-progress experiments.

    Returns the full markdown content as a string.
    """
    filepath = filepath or INVENTORY_MD

    if not filepath.exists():
        return "[No experiment inventory markdown found. Proceeding without detailed inventory context.]"

    try:
        return filepath.read_text(encoding="utf-8")
    except Exception as e:
        return f"[Error loading experiment inventory: {e}]"


# ---------------------------------------------------------------------------
# Full context builder
# ---------------------------------------------------------------------------

def build_full_context(market_intel_context: Optional[str] = None) -> list[dict]:
    """
    Build the complete messages list for the OpenAI API,
    including the system prompt, pre-loaded document context,
    and optional market intelligence data.

    Parameters
    ----------
    market_intel_context : str or None
        Formatted market intelligence report from the TelecomIntelPipeline.
        If provided, it's injected as a supplementary context section.

    Returns a list of message dicts ready for the API.
    """
    historical_data = load_historical_experiments()
    summary_table = load_experiment_summary_table()
    inventory_md = load_experiment_inventory_md()

    # Combine system prompt with document context
    full_system = (
        f"{SYSTEM_PROMPT}\n\n"
        f"==================================================\n"
        f"PRE-LOADED CONTEXT\n"
        f"==================================================\n\n"
        f"The following historical experiment data has been loaded from the team's "
        f"experiment tracking system. Use this data to ground all analysis, search, "
        f"ideation, prediction, and intake drafting.\n\n"
        f"==================================================\n"
        f"DETAILED EXPERIMENT INVENTORY (PRIMARY SOURCE)\n"
        f"==================================================\n"
        f"The following is the full 2025 att.com Experimentation Inventory with detailed "
        f"test descriptions, hypotheses, results, and key learnings for every experiment. "
        f"This is the PRIMARY knowledge source — use it for all recommendations, "
        f"analog searches, and ideation.\n\n"
        f"{inventory_md}\n\n"
        f"==================================================\n"
        f"STRUCTURED EXPERIMENT DATA (SUPPLEMENTARY)\n"
        f"==================================================\n\n"
        f"{summary_table}\n\n"
        f"{historical_data}"
    )

    # Inject market intelligence if available
    if market_intel_context:
        full_system += (
            f"\n\n"
            f"==================================================\n"
            f"TELECOM MARKET INTELLIGENCE (LIVE SIGNALS)\n"
            f"==================================================\n\n"
            f"The following market intelligence was collected from competitor websites "
            f"and Reddit communities. Use these signals to inform experiment ideation, "
            f"identify competitive threats, and surface market-driven opportunities.\n\n"
            f"{market_intel_context}"
        )

    return [{"role": "system", "content": full_system}]


def get_experiment_count() -> int:
    """Return the number of experiments in the dataset."""
    if not EXCEL_FILE.exists():
        return 0
    try:
        df = pd.read_excel(EXCEL_FILE, engine="openpyxl")
        return len(df)
    except Exception:
        return 0


def get_experiment_fields() -> list[str]:
    """Return the column names from the dataset."""
    if not EXCEL_FILE.exists():
        return []
    try:
        df = pd.read_excel(EXCEL_FILE, engine="openpyxl")
        return [c.strip() for c in df.columns.tolist()]
    except Exception:
        return []
