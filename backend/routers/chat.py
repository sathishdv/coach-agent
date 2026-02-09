"""Chat endpoint – main interaction point."""

from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import ChatRequest, ChatResponse
from backend.services.coach_orchestrator import coach

logger = logging.getLogger(__name__)
router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """Send a message to the JEE Coach and get a response."""
    try:
        result = await coach.chat(
            db=db,
            student_id=request.student_id,
            user_message=request.message,
        )
        return ChatResponse(
            reply=result["reply"],
            plan_summary=result.get("plan_summary"),
        )
    except ValueError as exc:
        logger.error("Configuration error in chat: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected error in chat endpoint")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your message: {exc}",
        ) from exc
