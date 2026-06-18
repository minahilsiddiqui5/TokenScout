# TokenScout

A budget-aware AI research agent. Give it a topic and a dollar budget, it
searches the web, writes a sourced briefing, critiques its own draft, and
tracks the cost of every step so it never overspends.

## Why it's different
- **Budget governor** — set a spend limit; the agent stops before it crosses it.
- **Two-tier models** — a cheap, fast model for grunt work; a strong model only
  for synthesis and self-critique.
- **Self-critique loop** — the agent finds gaps in its own report and digs deeper.
- **Cost ledger** — token and cost breakdown for every step.

Runs entirely on Groq's free tier — no credit card needed.

## How it works
Plan → Research → Draft → Critique → Refine (while budget allows)

## Setup
1. Get a free Groq key at https://console.groq.com/keys
2. Install:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.tx
3. Copy `.env.example` to `.env` and add your key.

## Usage
python main.py "impact of prompt caching on LLM API costs"
python main.py "model routing strategies" --budget 0.03 --rounds 2

## Project structure
- `search.py` — free web search (the agent's eyes)
- `ledger.py` — cost tracking + budget governor
- `llm.py` — Groq wrapper that auto-logs every call's tokens
- `agent.py` — the plan → research → draft → critique → refine loop
- `main.py` — command-line entry point
