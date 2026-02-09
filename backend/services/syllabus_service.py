"""Syllabus search & retrieval."""

from __future__ import annotations

import json
from typing import Any

from backend.config import settings

_syllabus_cache: dict[str, Any] | None = None


def _load_syllabus() -> dict[str, Any]:
    global _syllabus_cache
    if _syllabus_cache is None:
        syllabus_path = settings.project_root / settings.syllabus_path
        with open(syllabus_path, encoding="utf-8") as f:
            _syllabus_cache = json.load(f)
    return _syllabus_cache


def get_full_syllabus() -> dict[str, Any]:
    """Return the entire syllabus."""
    return _load_syllabus()


def search_syllabus(query: str) -> list[dict[str, Any]]:
    """Search syllabus topics by keyword (case-insensitive substring match)."""
    syllabus = _load_syllabus()
    query_lower = query.lower()
    results: list[dict[str, Any]] = []

    for subject in syllabus.get("subjects", []):
        for topic in subject.get("topics", []):
            for subtopic in topic.get("subtopics", []):
                if (
                    query_lower in subtopic["name"].lower()
                    or query_lower in subtopic["id"].lower()
                    or query_lower in topic["name"].lower()
                    or query_lower in subject["name"].lower()
                ):
                    results.append(
                        {
                            "topic_id": subtopic["id"],
                            "topic_name": subtopic["name"],
                            "subject": subject["name"],
                            "parent_topic": topic["name"],
                            "weight": subtopic.get("weight", 0),
                        }
                    )
    return results


def get_topic_hierarchy() -> list[dict[str, Any]]:
    """Return a flat list of all topics with hierarchy info."""
    syllabus = _load_syllabus()
    topics: list[dict[str, Any]] = []
    for subject in syllabus.get("subjects", []):
        for topic in subject.get("topics", []):
            for subtopic in topic.get("subtopics", []):
                topics.append(
                    {
                        "topic_id": subtopic["id"],
                        "topic_name": subtopic["name"],
                        "subject": subject["name"],
                        "parent_topic": topic["name"],
                        "weight": subtopic.get("weight", 0),
                    }
                )
    return topics
