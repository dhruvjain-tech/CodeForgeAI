from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from core.agents.service import agent_service


router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
)


class AgentRunRequest(BaseModel):
    agent_name: str = Field(..., min_length=1)
    task: str = Field(..., min_length=1)
    context: dict[str, Any] = Field(default_factory=dict)


@router.get("")
async def list_agents():
    return {
        "agents": agent_service.registry.list_agents()
    }


@router.post("/run")
async def run_agent(request: AgentRunRequest):

    try:
        result = await agent_service.run(
            agent_name=request.agent_name,
            task=request.task,
            context=request.context,
        )

        return {
            "agent_name": result.agent_name,
            "success": result.success,
            "output": result.output,
            "metadata": result.metadata,
            "error": result.error,
            "latency_ms": result.latency_ms,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )