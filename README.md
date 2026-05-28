# MARA — Multi-Agent RAG System

A production-grade multi-agent AI system where three specialist agents (Finance, Research, Legal) collaborate to answer complex questions using retrieval-augmented generation.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)

## What it does

- **Orchestrator agent** routes your query to the right specialist agents
- **Finance agent** answers questions about markets, revenue, crypto, economics
- **Research agent** answers questions about AI, science, technology, papers
- **Legal agent** answers questions about contracts, GDPR, employment law, IP
- **Synthesizer** merges all agent answers into one final response
- **Memory** — agents remember context across turns in a conversation
- **Confidence scoring** — every answer rated 0-100% by the agent
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

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/mara-multi-agent-rag.git
cd mara-multi-agent-rag

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Ingest knowledge base (optional - system works without it)
python ingest.py

# Launch dashboard
streamlit run dashboard/app.py
```

## Architecture