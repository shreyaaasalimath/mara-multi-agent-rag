cat > /Users/shreyasalimath/Desktop/multi-agent-rag/README.md << 'ENDOFFILE'
# MARA — Multi-Agent RAG System

A production-grade multi-agent AI system where three specialist agents (Finance, Research, Legal) collaborate to answer complex questions.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)

## What it does

- **Orchestrator agent** routes your query to the right specialist agents
- **Finance agent** answers questions about markets, revenue, crypto, economics
- **Research agent** answers questions about AI, science, technology, papers
- **Legal agent** answers questions about contracts, GDPR, employment law, IP
- **Synthesizer** merges all agent answers into one final response
- **Memory** — agents remember context across turns
- **Confidence scoring** — every answer rated 0-100%
- **Full audit trail** — every query logged with latency, tokens, confidence
- **Chat interface** — multiple conversations, recent chat history, new chat

## Tech stack

- Python 3.11
- Anthropic Claude API (claude-haiku)
- ChromaDB vector store
- Sentence Transformers embeddings
- Streamlit dashboard
- Plotly charts

## Setup

Clone the repo and install dependencies:

    git clone https://github.com/shreyaaasalimath/mara-multi-agent-rag.git
    cd mara-multi-agent-rag
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Add your API key:

    echo "ANTHROPIC_API_KEY=your_key_here" > .env

Launch the dashboard:

    streamlit run dashboard/app.py

## Architecture

    User Query
        ↓
    Orchestrator (routes query)
        ↓
    Finance Agent   Research Agent   Legal Agent
        ↓                ↓               ↓
    Claude LLM      Claude LLM      Claude LLM
        ↓                ↓               ↓
    Synthesizer (merges answers)
        ↓
    Final Answer

