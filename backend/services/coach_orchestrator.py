"""Coach Orchestrator – Claude Messages API with tool-use loop."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import anthropic
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.services import conversation_service, plan_service
from backend.tools.definitions import TOOL_DEFINITIONS
from backend.tools.handlers import execute_tool

logger = logging.getLogger(__name__)

# Maximum tool-use iterations to prevent infinite loops
MAX_TOOL_ITERATIONS = 10


def _load_prompt(name: str) -> str:
    """Load a prompt from backend/prompts/."""
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / name
    return prompt_path.read_text(encoding="utf-8")


def _get_system_prompt(is_onboarding: bool = False) -> str:
    """Build the full system prompt."""
    base = _load_prompt("system.md")
    if is_onboarding:
        base += "\n\n---\n\n" + _load_prompt("onboarding.md")
    return base


class CoachOrchestrator:
    """Manages a conversation with Claude using tool-use."""

    def __init__(self) -> None:
        self._client: anthropic.Anthropic | None = None
        self.model = settings.anthropic_model

    @property
    def client(self) -> anthropic.Anthropic:
        """Lazily initialize the Anthropic client."""
        if self._client is None:
            self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        return self._client

    async def chat(
        self,
        db: AsyncSession,
        student_id: str,
        user_message: str,
        is_onboarding: bool = False,
    ) -> dict[str, Any]:
        """Process a user message through the Claude tool-use loop.

        Returns {"reply": str, "plan_summary": dict | None}.
        """
        # 1. Load conversation history
        conv_id, history = await conversation_service.get_or_create_conversation(
            db, student_id
        )

        # 2. Build messages
        messages = self._build_messages(history, user_message)

        # 3. Get system prompt
        system_prompt = _get_system_prompt(is_onboarding)

        # 4. Run the tool-use loop
        assistant_text, new_messages = await self._tool_loop(
            db=db,
            system_prompt=system_prompt,
            messages=messages,
        )

        # 5. Persist conversation
        # Save user message + all assistant/tool messages
        to_persist = [{"role": "user", "content": user_message}]
        to_persist.extend(new_messages)
        await conversation_service.append_messages(db, conv_id, to_persist)

        # 6. Get current plan summary
        plan = await plan_service.get_current_plan(db, student_id)
        plan_summary = plan.get("plan_data") if plan else None

        return {"reply": assistant_text, "plan_summary": plan_summary}

    def _build_messages(
        self,
        history: list[dict[str, Any]],
        user_message: str,
    ) -> list[dict[str, Any]]:
        """Build the messages list for the API call."""
        messages: list[dict[str, Any]] = []

        # Add history (already in Claude message format)
        for msg in history:
            if isinstance(msg.get("content"), str):
                messages.append({"role": msg["role"], "content": msg["content"]})
            elif isinstance(msg.get("content"), list):
                messages.append({"role": msg["role"], "content": msg["content"]})

        # Add new user message
        messages.append({"role": "user", "content": user_message})

        return messages

    async def _tool_loop(
        self,
        db: AsyncSession,
        system_prompt: str,
        messages: list[dict[str, Any]],
    ) -> tuple[str, list[dict[str, Any]]]:
        """Execute the Claude tool-use loop until we get a final text response.

        Returns (final_text, list_of_new_messages_to_persist).
        """
        new_messages: list[dict[str, Any]] = []
        final_text = ""

        for iteration in range(MAX_TOOL_ITERATIONS):
            logger.info(f"Tool loop iteration {iteration + 1}")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                tools=TOOL_DEFINITIONS,
                messages=messages,
            )

            # Process the response
            assistant_content = response.content
            stop_reason = response.stop_reason

            # Build serializable content for persistence
            serialized_content = self._serialize_content(assistant_content)
            assistant_msg = {"role": "assistant", "content": serialized_content}
            messages.append(assistant_msg)
            new_messages.append(assistant_msg)

            # If stop reason is "end_turn", extract text and return
            if stop_reason == "end_turn":
                final_text = self._extract_text(assistant_content)
                break

            # If stop reason is "tool_use", execute tools and continue
            if stop_reason == "tool_use":
                tool_results = await self._execute_tool_calls(db, assistant_content)

                tool_result_msg = {
                    "role": "user",
                    "content": tool_results,
                }
                messages.append(tool_result_msg)
                new_messages.append(tool_result_msg)
            else:
                # Unexpected stop reason; extract what we can
                final_text = self._extract_text(assistant_content)
                break

        if not final_text:
            final_text = "I'm processing your request. Please try again if you don't see a complete response."

        return final_text, new_messages

    async def _execute_tool_calls(
        self,
        db: AsyncSession,
        content: list,
    ) -> list[dict[str, Any]]:
        """Execute all tool_use blocks in a response."""
        results: list[dict[str, Any]] = []

        for block in content:
            if block.type == "tool_use":
                logger.info(
                    f"Executing tool: {block.name} with input: {json.dumps(block.input)[:200]}"
                )
                result_str = await execute_tool(block.name, block.input, db)
                results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result_str,
                    }
                )

        return results

    def _extract_text(self, content: list) -> str:
        """Extract text blocks from Claude's response."""
        texts: list[str] = []
        for block in content:
            if block.type == "text":
                texts.append(block.text)
        return "\n".join(texts)

    def _serialize_content(self, content: list) -> list[dict[str, Any]]:
        """Serialize Claude content blocks for persistence."""
        serialized: list[dict[str, Any]] = []
        for block in content:
            if block.type == "text":
                serialized.append({"type": "text", "text": block.text})
            elif block.type == "tool_use":
                serialized.append(
                    {
                        "type": "tool_use",
                        "id": block.id,
                        "name": block.name,
                        "input": block.input,
                    }
                )
        return serialized


# Singleton instance
coach = CoachOrchestrator()
