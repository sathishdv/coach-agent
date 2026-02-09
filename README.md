# JEE Coach Agent

An AI-powered tutoring agent for IIT-JEE preparation, built with FastAPI and Anthropic Claude.

## Features

- **Personalized Onboarding** — Student profile with strengths, weaknesses, and study preferences
- **Socratic Tutoring** — Hints-first approach; never gives full solutions until the student attempts
- **Weekly & Daily Study Plans** — Time-boxed tasks with spaced repetition
- **JEE-Style Practice** — Generates practice questions across Physics, Chemistry, Mathematics
- **Step-by-Step Grading** — Evaluates attempts with misconception tagging
- **Mastery Map** — Per-topic mastery tracking (0–100%) with error pattern analysis
- **RAG Pipeline** — BM25-based search over curated JEE notes
- **Web UI** — Clean chat interface with profile sidebar and mastery visualization

## Quick Start

### 1. Prerequisites

- Python 3.11+
- An Anthropic API key

### 2. Setup

```bash
# Clone and enter the project
cd coach-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run

```bash
# Start the server (one command!)
python run.py
```

The app will be available at **http://localhost:8000**

### 4. Optional: Seed Sample Data

```bash
python scripts/seed.py
```

### 5. Smoke Test

```bash
# With server running in another terminal:
python scripts/smoke_test.py
```

## Project Structure

```
coach-agent/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Environment config
│   ├── database.py             # Async SQLAlchemy setup
│   ├── models.py               # ORM models (Postgres-ready)
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── routers/
│   │   ├── chat.py             # POST /chat
│   │   ├── student.py          # GET/POST /student/{id}
│   │   ├── attempt.py          # POST /attempt
│   │   └── syllabus.py         # GET /syllabus/search
│   ├── services/
│   │   ├── coach_orchestrator.py  # Claude tool-use loop
│   │   ├── student_service.py
│   │   ├── mastery_service.py
│   │   ├── plan_service.py
│   │   ├── attempt_service.py
│   │   ├── syllabus_service.py
│   │   ├── notes_service.py       # BM25 RAG pipeline
│   │   └── conversation_service.py
│   ├── tools/
│   │   ├── definitions.py      # Claude tool schemas
│   │   └── handlers.py         # Tool execution dispatch
│   └── prompts/
│       ├── system.md           # Main system prompt
│       └── onboarding.md       # Onboarding prompt
├── frontend/
│   └── index.html              # Single-page chat UI
├── data/
│   ├── syllabus.json           # Full JEE syllabus hierarchy
│   └── notes/
│       ├── mechanics.md
│       ├── organic_chemistry.md
│       └── calculus.md
├── scripts/
│   ├── seed.py                 # Seed sample data
│   └── smoke_test.py           # Automated smoke test
├── run.py                      # Server entry point
├── requirements.txt
├── .env.example
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Send a message, get AI coaching response |
| `GET` | `/student/{id}` | Get full student profile + mastery + plan |
| `POST` | `/student/{id}/onboard` | Onboard a new student |
| `POST` | `/attempt` | Log a student attempt |
| `GET` | `/syllabus/search?q=...` | Search the JEE syllabus |
| `GET` | `/syllabus/full` | Get the complete syllabus |
| `GET` | `/health` | Health check |

## Claude Tools

The Coach Orchestrator provides these tools to Claude:

1. `load_student` — Load student profile
2. `upsert_student` — Create/update student profile
3. `log_attempt` — Log a practice attempt
4. `update_mastery` — Update topic mastery scores
5. `get_syllabus` — Search syllabus topics
6. `search_notes` — Search curated JEE notes (RAG)
7. `generate_practice_set` — Generate practice questions
8. `generate_test_blueprint` — Create mock test plans
9. `get_mastery_map` — Retrieve mastery map
10. `get_study_plan` — Get current study plan
11. `save_study_plan` — Save a new study plan

## Tutoring Policy

The agent follows a strict hints-first (Socratic) approach:

1. **Hint 1** — Guiding question pointing to the relevant concept
2. **Hint 2** — More specific hint about the approach/formula
3. **Partial Step** — First step of the solution
4. **Full Solution** — Only after student attempts or explicitly requests

Every interaction ends with:
- 3 suggested next actions
- 1 quick retrieval question (30-second recall)

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy (async)
- **AI**: Anthropic Claude via Messages API with tool-use
- **Database**: SQLite (MVP) — schema is Postgres-ready
- **RAG**: BM25 (rank_bm25) over markdown notes
- **Frontend**: Vanilla HTML/CSS/JS (no build step)

