You are Cursor AI. Build a production-quality MVP called "jee-coach-agent".

Goal:
An AI tutoring agent for IIT-JEE that:
- onboards student profile
- builds a weekly + daily study plan
- teaches using hints-first (Socratic), not instant full solutions
- generates JEE-style practice questions
- grades student attempts step-by-step
- maintains a mastery map per topic
- persists state per student
- exposes an API + simple web UI (optional but preferred)

Tech constraints:
- Python 3.11+
- FastAPI backend
- Anthropic Claude via official Messages API (tool_use loop)
- SQLite for MVP persistence (Postgres-ready schema)
- Optional: RAG with local files using a simple vector store (FAISS) or even naive BM25 for MVP
- Everything runnable locally with docker-compose optional

Repo structure:
1) backend/: FastAPI + tool loop + persistence
2) frontend/: minimal Next.js or a simple static page that calls backend (optional)
3) data/: sample syllabus and curated notes in markdown/json
4) scripts/: seed, migrations, smoke tests

Key product requirements:
- Strict tutoring policy:
  * If the student asks "solve this", do not give full solution until the student attempts.
  * Provide Hint1 -> Hint2 -> partial step -> full solution only after request + attempt.
- Every interaction ends with:
  * Next 3 actions
  * 1 quick retrieval question (30 seconds)
- Mastery map:
  * topic_id -> mastery_score [0..1], last_practiced, error_tags counters
- Evaluation:
  * Log attempts with time_taken, steps, correctness, misconception tags
- Plan:
  * Weekly plan -> daily tasks with time boxes, spaced repetition, backlog.

Claude integration:
- Use Messages API tool-use.
- Provide tools:
  1) load_student(student_id)
  2) upsert_student(profile/state)
  3) log_attempt(student_id, attempt)
  4) update_mastery(student_id, topic_updates)
  5) get_syllabus(query)
  6) search_notes(query)  (for RAG; can be naive v1)
  7) generate_practice_set(topics, difficulty, count, format)
  8) generate_test_blueprint(duration_min, topics, difficulty_mix)

Implement:
- A central "Coach Orchestrator" that calls Claude with system prompt + tools and executes tool calls.
- Store system prompts in backend/prompts/*.md and load them.
- Provide a default syllabus for JEE (topic hierarchy) under data/syllabus.json.
- Provide sample notes for 2-3 topics under data/notes/ to prove RAG pipeline.

API endpoints:
- POST /chat {student_id, message} -> response + updated plan summary
- GET /student/{id} -> profile + mastery + plan
- POST /student/{id}/onboard -> create/update profile
- POST /attempt -> log attempt (or via tool)
- GET /syllabus/search?q=...

Deliverables:
- Complete code
- README with setup steps
- .env.example
- A smoke test script that onboards a student and runs 3 interactions.

Important: Make sensible choices when details are missing. Do not ask me questions; just implement.
After implementing, run formatting, add type hints, and ensure the project starts with one command.
