# 🧳 AI Travel Planner

A multi-agent travel planning system built from scratch with **LangGraph**, **Groq**, and real-time web search. Specialized agents research flights, accommodation, and activities independently, and an orchestrator combines their output into one coherent, budget-aware itinerary.

**🔗 Live demo:** [travel-planner-zoe5.onrender.com](https://travel-planner-zoe5.onrender.com)
*(Hosted on Render's free tier — the first request after inactivity can take 30–60 seconds to wake up.)*

---

## What it does

You provide an origin, destination, dates, budget, and preferences. Three specialized agents each research their part of the trip using **real web search** (not just LLM guesswork), and a LangGraph orchestrator merges their results into a single itinerary — flagging clearly when a price is a live figure vs. a "starting from" estimate.

## Features

- **Multi-agent architecture** — independent Flight, Accommodation, and Activity agents, each with a focused prompt and role
- **LangGraph orchestration** — a stateful graph coordinates agent execution and merges results
- **Real-data grounding** — every agent runs a live DuckDuckGo search before generating its answer, and is explicitly instructed to cite sources and flag estimates vs. confirmed prices
- **Budget-aware output** — agents check suggestions against the stated budget and call out when options exceed it
- **Personalization** — the Activity agent tailors its day-by-day plan to stated preferences (food, culture, nightlife, etc.)
- **Deterministic day-numbering** — trip length is calculated in Python (not left to the LLM to count), eliminating a class of itinerary bugs where the model skipped or duplicated days
- **FastAPI backend + browser frontend** — a simple web UI with Markdown-to-HTML rendering for readable output

## Architecture

```
User request (origin, destination, dates, budget, preferences)
        │
        ▼
   LangGraph Orchestrator
        │
   ┌────┼────────────┬───────────────┐
   ▼    ▼             ▼               ▼
Flight  Accommodation  Activity        │
Agent   Agent          Agent           │
   │      │             │              │
   └──────┴─────────────┴──────────────┘
                  │
                  ▼
        Combine Node → Final Itinerary
                  │
                  ▼
         FastAPI → Browser Frontend
```

Each agent follows the same pattern: run a live web search → feed the results into a role-specific prompt → generate a grounded, cited response. The orchestrator calls them in sequence and merges their outputs into one document.

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | Groq (`openai/gpt-oss-20b`) |
| Agent orchestration | LangGraph |
| Web search | `ddgs` (DuckDuckGo, free, no API key) |
| Backend | FastAPI |
| Frontend | HTML/CSS/JS, `marked.js` for Markdown rendering |
| Hosting | Render (free tier) |

## Running it locally

**1. Clone the repo**
```bash
git clone https://github.com/muhdfinaan-lab/travel-planner.git
cd travel-planner
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

**3. Add your Groq API key**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_key_here
```
Get a free key at [console.groq.com](https://console.groq.com).

**4. Run the server**
```bash
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000` in your browser.

## Engineering notes

A few real issues came up during development and how they were fixed — noted here for transparency:

- **Deprecated model**: `llama-3.1-8b-instant` was retired by Groq mid-development; migrated to `openai/gpt-oss-20b`.
- **Truncated output**: itineraries were silently cut off mid-generation because no `max_completion_tokens` was set, defaulting to a low limit. Fixed by explicitly setting a higher token budget.
- **Unreliable day-numbering**: the LLM occasionally miscounted trip length from date strings like "Oct 10-17" (skipping or duplicating days). Fixed by calculating the exact day count in Python and passing it as a hard constraint in the prompt, rather than trusting the model to count correctly.

## Known limitations

- Prices are grounded in real search snippets, but are **not** live booking-API data — they should be treated as a starting point, not a final quote.
- No persistent storage — each request is stateless; there's no way to save or revisit a past itinerary.
- Free-tier Groq and Render both have rate/uptime constraints not suited for production use.

## Possible next steps

- Parallelize the three agents (they're currently independent and could run concurrently rather than sequentially)
- Add a real flight/hotel pricing API for confirmed quotes
- Persist generated itineraries (e.g., SQLite) so users can revisit past plans

---

Built as a learning project to understand multi-agent orchestration, LLM grounding via search, and shipping a full-stack AI app end-to-end.
