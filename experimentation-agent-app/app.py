"""
Experimentation Agent — Streamlit Chat Application

A conversational CRO experimentation assistant powered by OpenAI,
pre-loaded with historical experiment data and structured reasoning.
"""

import os
import time

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

from agent_config import build_full_context, get_experiment_count, get_experiment_fields
from thinking_agent import ThinkingAgent

# ---------------------------------------------------------------------------
# Environment & Configuration
# ---------------------------------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.4"))


# ---------------------------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Experimentation Agent",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom Styling
# ---------------------------------------------------------------------------

st.markdown("""
<style>
    /* Main container */
    .stApp {
        background-color: #0e1117;
    }

    /* Header styling */
    .agent-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #1e3a5f;
    }
    .agent-header h1 {
        color: #e2e8f0;
        font-size: 1.8rem;
        margin: 0;
        font-weight: 700;
    }
    .agent-header p {
        color: #94a3b8;
        font-size: 0.95rem;
        margin: 0.3rem 0 0 0;
    }

    /* Status badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        color: #22c55e;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    /* Sidebar styling */
    .sidebar-section {
        background: #1a1a2e;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #2d2d44;
    }
    .sidebar-section h3 {
        color: #e2e8f0;
        font-size: 0.9rem;
        margin: 0 0 0.5rem 0;
    }
    .sidebar-section p {
        color: #94a3b8;
        font-size: 0.82rem;
        margin: 0.2rem 0;
    }

    /* Capability cards */
    .capability-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-top: 0.5rem;
    }
    .capability-card {
        background: #1e293b;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #334155;
        text-align: center;
    }
    .capability-card .icon {
        font-size: 1.3rem;
    }
    .capability-card .label {
        color: #cbd5e1;
        font-size: 0.78rem;
        margin-top: 2px;
    }

    /* Chat messages */
    .stChatMessage {
        border-radius: 12px !important;
    }

    /* Starter prompt buttons */
    .starter-btn {
        background: #1e293b;
        border: 1px solid #334155;
        color: #cbd5e1;
        padding: 10px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.85rem;
        text-align: left;
        transition: all 0.2s;
        width: 100%;
        margin-bottom: 6px;
    }
    .starter-btn:hover {
        background: #2d3a4f;
        border-color: #4a90d9;
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div class="sidebar-section">
        <h3>⚙️ Configuration</h3>
    </div>
    """, unsafe_allow_html=True)

    # API Key input (with env fallback)
    api_key_input = st.text_input(
        "OpenAI API Key",
        value=OPENAI_API_KEY,
        type="password",
        help="Enter your OpenAI API key. You can also set it in the .env file.",
    )

    model_choice = st.selectbox(
        "Model",
        options=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"].index(OPENAI_MODEL)
        if OPENAI_MODEL in ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
        else 0,
        help="Select the OpenAI model. gpt-4o recommended for best results.",
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=OPENAI_TEMPERATURE,
        step=0.1,
        help="Lower = more deterministic. Higher = more creative.",
    )

    st.divider()

    # Data status
    experiment_count = get_experiment_count()
    fields = get_experiment_fields()

    st.markdown(f"""
    <div class="sidebar-section">
        <h3>📊 Loaded Data</h3>
        <p><strong>{experiment_count}</strong> historical experiments</p>
        <p><strong>{len(fields)}</strong> data fields per experiment</p>
        <p style="color: {'#22c55e' if experiment_count > 0 else '#ef4444'};">
            {'✅ Data loaded successfully' if experiment_count > 0 else '❌ No data found — place Excel file in /documents'}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Capabilities
    st.markdown("""
    <div class="sidebar-section">
        <h3>🧠 Agent Capabilities</h3>
        <div class="capability-grid">
            <div class="capability-card">
                <div class="icon">🔍</div>
                <div class="label">Search Experiments</div>
            </div>
            <div class="capability-card">
                <div class="icon">💡</div>
                <div class="label">Generate Ideas</div>
            </div>
            <div class="capability-card">
                <div class="icon">📊</div>
                <div class="label">Predict Success</div>
            </div>
            <div class="capability-card">
                <div class="icon">📝</div>
                <div class="label">Draft Tickets</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Clear chat button
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.context_messages = None
        st.rerun()


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.markdown(f"""
<div class="agent-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1>🧪 Experimentation Agent</h1>
            <p>CRO Intelligence System — Search, Ideate, Predict, and Plan experiments grounded in historical evidence</p>
        </div>
        <div class="status-badge">
            ● {experiment_count} experiments loaded
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "context_messages" not in st.session_state:
    st.session_state.context_messages = None


# ---------------------------------------------------------------------------
# Pre-load context on first run
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner=False)
def get_system_context():
    """Load and cache the full system context (system prompt + experiment data)."""
    return build_full_context()


# ---------------------------------------------------------------------------
# Starter Prompts (shown when chat is empty)
# ---------------------------------------------------------------------------

STARTER_PROMPTS = [
    {
        "icon": "🔍",
        "label": "Search past experiments",
        "prompt": "What experiments have we run on the wireless PDP? Summarize the results and key learnings.",
    },
    {
        "icon": "💡",
        "label": "Generate experiment ideas",
        "prompt": "Generate 3 new experiment ideas for the internet buy flow, grounded in our historical data.",
    },
    {
        "icon": "📊",
        "label": "Analyze performance by LOB",
        "prompt": "Which lines of business tend to perform better in experimentation? Where should I invest my time?",
    },
    {
        "icon": "📝",
        "label": "Draft an intake ticket",
        "prompt": "Draft a JIRA-ready intake ticket for testing a simplified trade-in flow on the upgrade PDP.",
    },
    {
        "icon": "🏆",
        "label": "Predict experiment success",
        "prompt": "Would an A/B test adding urgency messaging to the wireless cart page likely win? Evaluate with historical evidence.",
    },
    {
        "icon": "📈",
        "label": "Find winning patterns",
        "prompt": "What are the common patterns across our winning experiments? What mechanisms drive success?",
    },
]


def render_starter_prompts():
    """Render clickable starter prompt cards."""
    st.markdown("### 👋 How can I help with your experimentation program?")
    st.markdown("Choose a starting point or type your own question below.")
    st.markdown("")

    cols = st.columns(2)
    for i, starter in enumerate(STARTER_PROMPTS):
        with cols[i % 2]:
            if st.button(
                f"{starter['icon']}  {starter['label']}",
                key=f"starter_{i}",
                use_container_width=True,
            ):
                st.session_state.messages.append(
                    {"role": "user", "content": starter["prompt"]}
                )
                st.rerun()


# ---------------------------------------------------------------------------
# Chat Display
# ---------------------------------------------------------------------------

if not st.session_state.messages:
    render_starter_prompts()
else:
    for message in st.session_state.messages:
        avatar = "🧪" if message["role"] == "assistant" else "👤"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])


# ---------------------------------------------------------------------------
# Chat Input & Response Generation
# ---------------------------------------------------------------------------

if prompt := st.chat_input("Ask about experiments, ideas, predictions, or intake..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Validate API key
    active_key = api_key_input or OPENAI_API_KEY
    if not active_key or active_key == "sk-your-key-here":
        with st.chat_message("assistant", avatar="🧪"):
            st.error(
                "⚠️ **No API key configured.** Please enter your OpenAI API key in the sidebar "
                "or set it in the `.env` file."
            )
        st.stop()

    # Initialize thinking agent
    client = OpenAI(api_key=active_key)
    thinking_agent = ThinkingAgent(client, model=model_choice, temperature=temperature)
    
    # Get system context for the thinking agent
    system_context = get_system_context()
    context_content = system_context[0]["content"] if system_context else ""

    # Stream the response with thinking agent
    with st.chat_message("assistant", avatar="🧪"):
        message_placeholder = st.empty()
        thinking_placeholder = st.empty()
        full_response = ""

        try:
            # Use a simple list to track thinking log for the callback
            thinking_log = [""]
            
            def stream_callback(text):
                thinking_log[0] += text
                thinking_placeholder.markdown(f"### 🧠 Agent Coordination\n\n{thinking_log[0]}")

            # Process with thinking agent
            full_response = thinking_agent.process_query(
                query=prompt,
                context=context_content,
                stream_callback=stream_callback
            )
            
            # Clear thinking log and show final response
            thinking_placeholder.empty()
            message_placeholder.markdown(full_response)

        except Exception as e:
            error_msg = str(e)
            if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                message_placeholder.error(
                    "🔑 **Authentication failed.** Please check your OpenAI API key."
                )
            elif "rate_limit" in error_msg.lower():
                message_placeholder.warning(
                    "⏳ **Rate limited.** Please wait a moment and try again."
                )
            elif "model" in error_msg.lower():
                message_placeholder.error(
                    f"🤖 **Model error.** The model `{model_choice}` may not be available "
                    f"on your API plan. Try switching to `gpt-4o-mini` in the sidebar."
                )
            else:
                message_placeholder.error(f"❌ **Error:** {error_msg}")
            full_response = ""

    # Save assistant response
    if full_response:
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 0.8rem;'>"
    "Experimentation Agent v1.0 — Powered by OpenAI | "
    "Historical data auto-loaded from /documents"
    "</p>",
    unsafe_allow_html=True,
)
