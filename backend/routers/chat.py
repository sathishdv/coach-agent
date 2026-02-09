"""Chat endpoint – main interaction point."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.schemas import ChatRequest, ChatResponse
from backend.services.coach_orchestrator import coach

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """Send a message to the JEE Coach and get a response."""
    result = await coach.chat(
        db=db,
        student_id=request.student_id,
        user_message=request.message,
    )
    return ChatResponse(
        reply=result["reply"],
        plan_summary=result.get("plan_summary"),
    )
