#!/bin/bash
# =============================================================
# Experimentation Agent — Startup Script
# =============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "🧪 Experimentation Agent — Starting..."
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found."
    echo "   Copy .env.example to .env and add your OpenAI API key:"
    echo ""
    echo "   cp .env.example .env"
    echo "   open .env"
    echo ""
    exit 1
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ python3 not found. Please install Python 3.10+."
    exit 1
fi

# Check for pip dependencies
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    python3 -m pip install -r requirements.txt
    echo ""
fi

# Check for documents
if [ ! -f "documents/XTrack_Chat_Bot_export_2025-07-28T07_28_00.xlsx" ]; then
    echo "⚠️  No experiment data found in /documents."
    echo "   The agent will run without historical context."
    echo ""
fi

echo "🚀 Launching Experimentation Agent..."
echo "   Open your browser to: http://localhost:8501"
echo ""

python3 -m streamlit run app.py --server.port 8501 --server.headless true
