"""Mastery map operations."""

from __future__ import annotations

import datetime
import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import MasteryEntry


async def get_mastery_map(db: AsyncSession, student_id: str) -> list[dict[str, Any]]:
    """Return all mastery entries for a student."""
    result = await db.execute(
        select(MasteryEntry).where(MasteryEntry.student_id == student_id)
    )
    entries = result.scalars().all()
    return [e.to_dict() for e in entries]


async def update_mastery(
    db: AsyncSession,
    student_id: str,
    topic_updates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Upsert mastery entries for given topics.

    Each item in topic_updates should have:
      - topic_id (required)
      - topic_name (optional)
      - mastery_score (optional, 0..1)
      - error_tags (optional, dict)
      - delta_attempts (optional, int to add)
    """
    updated: list[dict[str, Any]] = []
    for update in topic_updates:
        topic_id = update["topic_id"]
        result = await db.execute(
            select(MasteryEntry).where(
                MasteryEntry.student_id == student_id,
                MasteryEntry.topic_id == topic_id,
            )
        )
        entry = result.scalar_one_or_none()

        if entry is None:
            entry = MasteryEntry(student_id=student_id, topic_id=topic_id)
            db.add(entry)

        if "topic_name" in update:
            entry.topic_name = update["topic_name"]
        if "mastery_score" in update:
            entry.mastery_score = float(update["mastery_score"])
        if "error_tags" in update:
            existing_tags: dict[str, int] = (
                json.loads(entry.error_tags) if entry.error_tags else {}
            )
            for tag, count in update["error_tags"].items():
                existing_tags[tag] = existing_tags.get(tag, 0) + count
            entry.error_tags = json.dumps(existing_tags)
        if "delta_attempts" in update:
            entry.attempts_count = (entry.attempts_count or 0) + int(
                update["delta_attempts"]
            )

        entry.last_practiced = datetime.datetime.now(datetime.timezone.utc)
        updated.append(entry)

    await db.commit()
    return [e.to_dict() for e in updated]
