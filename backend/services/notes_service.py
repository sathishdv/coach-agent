"""Simple RAG pipeline for notes – uses BM25 for MVP."""

from __future__ import annotations

from typing import Any

from rank_bm25 import BM25Okapi

from backend.config import settings

_documents: list[dict[str, Any]] = []
_bm25: BM25Okapi | None = None


def _load_notes() -> None:
    """Load all markdown notes and build BM25 index."""
    global _documents, _bm25

    notes_dir = settings.project_root / settings.notes_dir
    if not notes_dir.exists():
        return

    _documents = []
    for md_file in sorted(notes_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        # Split into sections by ## headings
        sections = _split_into_sections(content, md_file.stem)
        _documents.extend(sections)

    if _documents:
        tokenized = [doc["tokens"] for doc in _documents]
        _bm25 = BM25Okapi(tokenized)


def _split_into_sections(content: str, source: str) -> list[dict[str, Any]]:
    """Split a markdown document into sections by ## headings."""
    sections: list[dict[str, Any]] = []
    current_heading = source
    current_lines: list[str] = []

    for line in content.split("\n"):
        if line.startswith("## "):
            if current_lines:
                text = "\n".join(current_lines).strip()
                if text:
                    sections.append(
                        {
                            "source": source,
                            "heading": current_heading,
                            "text": text,
                            "tokens": text.lower().split(),
                        }
                    )
            current_heading = line.lstrip("# ").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    # Last section
    if current_lines:
        text = "\n".join(current_lines).strip()
        if text:
            sections.append(
                {
                    "source": source,
                    "heading": current_heading,
                    "text": text,
                    "tokens": text.lower().split(),
                }
            )
    return sections


def search_notes(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """Search notes using BM25. Returns top-k relevant sections."""
    global _bm25, _documents

    if _bm25 is None:
        _load_notes()

    if _bm25 is None or not _documents:
        return []

    tokenized_query = query.lower().split()
    scores = _bm25.get_scores(tokenized_query)

    # Pair with docs and sort
    scored_docs = sorted(zip(scores, _documents), key=lambda x: x[0], reverse=True)

    results: list[dict[str, Any]] = []
    for score, doc in scored_docs[:top_k]:
        if score > 0:
            results.append(
                {
                    "source": doc["source"],
                    "heading": doc["heading"],
                    "text": doc["text"][:2000],  # Truncate long sections
                    "score": round(float(score), 3),
                }
            )
    return results


def reload_notes() -> None:
    """Force reload of notes index."""
    global _bm25, _documents
    _bm25 = None
    _documents = []
    _load_notes()
