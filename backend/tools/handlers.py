"""Execute tool calls from Claude and return results."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.services import (
    attempt_service,
    mastery_service,
    notes_service,
    plan_service,
    student_service,
    syllabus_service,
)


async def execute_tool(
    tool_name: str,
    tool_input: dict[str, Any],
    db: AsyncSession,
) -> str:
    """Dispatch a tool call and return JSON-string result."""
    try:
        result = await _dispatch(tool_name, tool_input, db)
        return json.dumps(result, default=str)
    except Exception as exc:
        return json.dumps({"error": str(exc)})


async def _dispatch(
    tool_name: str,
    tool_input: dict[str, Any],
    db: AsyncSession,
) -> Any:
    """Route tool calls to the appropriate service function."""

    if tool_name == "load_student":
        student = await student_service.load_student(db, tool_input["student_id"])
        if student is None:
            return {
                "error": "Student not found",
                "student_id": tool_input["student_id"],
            }
        return student

    elif tool_name == "upsert_student":
        return await student_service.upsert_student(
            db, tool_input["student_id"], tool_input.get("profile", {})
        )

    elif tool_name == "log_attempt":
        attempt_data = tool_input.get("attempt", {})
        attempt_data["student_id"] = tool_input["student_id"]
        return await attempt_service.log_attempt(db, attempt_data)

    elif tool_name == "update_mastery":
        return await mastery_service.update_mastery(
            db, tool_input["student_id"], tool_input.get("topic_updates", [])
        )

    elif tool_name == "get_mastery_map":
        return await mastery_service.get_mastery_map(db, tool_input["student_id"])

    elif tool_name == "get_syllabus":
        return syllabus_service.search_syllabus(tool_input.get("query", ""))

    elif tool_name == "search_notes":
        return notes_service.search_notes(tool_input.get("query", ""))

    elif tool_name == "generate_practice_set":
        # This is a "marker" tool – Claude generates the questions itself.
        # We return the input as acknowledgement so Claude knows what to generate.
        return {
            "status": "generate",
            "instruction": (
                "Generate JEE-style practice questions based on the following parameters. "
                "Return them in your response to the student."
            ),
            "params": tool_input,
        }

    elif tool_name == "generate_test_blueprint":
        return {
            "status": "generate",
            "instruction": (
                "Generate a test blueprint / mock exam plan based on these parameters. "
                "Return it in your response."
            ),
            "params": tool_input,
        }

    elif tool_name == "get_study_plan":
        plan = await plan_service.get_current_plan(db, tool_input["student_id"])
        if plan is None:
            return {"message": "No study plan found. Consider creating one."}
        return plan

    elif tool_name == "save_study_plan":
        return await plan_service.save_plan(
            db,
            tool_input["student_id"],
            tool_input["week_start"],
            tool_input.get("plan_data", {}),
        )

    else:
        return {"error": f"Unknown tool: {tool_name}"}
