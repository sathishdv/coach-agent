"""Conversation history persistence."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Conversation

# Maximum messages to keep in context (rolling window)
MAX_CONTEXT_MESSAGES = 40


async def get_or_create_conversation(
    db: AsyncSession, student_id: str
) -> tuple[int, list[dict[str, Any]]]:
    """Get the latest conversation for a student, or create one.

    Returns (conversation_id, messages_list).
    """
    result = await db.execute(
        select(Conversation)
        .where(Conversation.student_id == student_id)
        .order_by(Conversation.updated_at.desc())
        .limit(1)
    )
    conv = result.scalar_one_or_none()

    if conv is None:
        conv = Conversation(student_id=student_id, messages=json.dumps([]))
        db.add(conv)
        await db.commit()
        await db.refresh(conv)

    messages = json.loads(conv.messages) if conv.messages else []
    return conv.id, messages


async def append_messages(
    db: AsyncSession,
    conversation_id: int,
    new_messages: list[dict[str, Any]],
) -> None:
    """Append messages to a conversation, keeping a rolling window."""
    result = await db.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conv = result.scalar_one_or_none()
    if conv is None:
        return

    messages = json.loads(conv.messages) if conv.messages else []
    messages.extend(new_messages)

    # Keep last N messages to manage context window
    if len(messages) > MAX_CONTEXT_MESSAGES:
        messages = messages[-MAX_CONTEXT_MESSAGES:]

    conv.messages = json.dumps(messages)
    await db.commit()
