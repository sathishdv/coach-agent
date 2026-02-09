FROM python:3.13-slim

WORKDIR /app

# Install dependencies (exclude dev-only packages)
COPY requirements.txt .
RUN grep -v "^ruff" requirements.txt > requirements-prod.txt && \
    pip install --no-cache-dir -r requirements-prod.txt && \
    rm requirements-prod.txt

# Copy application code
COPY backend/ backend/
COPY data/ data/
COPY run.py .

# Create directory for SQLite database (persist via volume)
RUN mkdir -p /app/db

# Railway provides PORT env var; default to 8001
ENV PORT=8001
ENV HOST=0.0.0.0
ENV DEBUG=false
ENV DATABASE_URL=sqlite+aiosqlite:///./db/jee_coach.db

EXPOSE ${PORT}

CMD ["python", "run.py"]

