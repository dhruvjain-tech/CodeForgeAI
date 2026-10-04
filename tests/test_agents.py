from unittest.mock import AsyncMock, patch

import pytest

from core.agents.service import agent_service
from core.agents.types import AgentResult
from core.llm.types import LLMResponse, LLMUsage


EXPECTED_AGENTS = [
    "architect",
    "researcher",
    "developer",
    "tester",
    "debugger",
    "reviewer",
    "evaluator",
]


def test_default_agents_registered():
    agents = agent_service.registry.list_agents()

    assert agents == EXPECTED_AGENTS


def test_get_registered_agent():
    agent = agent_service.registry.get("architect")

    assert agent.agent_name == "architect"
    assert agent.agent_role


def test_unknown_agent_raises_error():
    with pytest.raises(ValueError, match="Agent not registered"):
        agent_service.registry.get("unknown")


@pytest.mark.asyncio
async def test_architect_build_request():
    agent = agent_service.registry.get("architect")

    request = await agent.build_request(
        task="Design a REST API",
        context={"language": "Python"},
    )

    assert request.messages
    assert "REST API" in request.messages[0]["content"]
    assert request.temperature == 0.2


@pytest.mark.asyncio
async def test_developer_build_request():
    agent = agent_service.registry.get("developer")

    request = await agent.build_request(
        task="Create a login endpoint",
        context={"framework": "FastAPI"},
    )

    assert request.messages
    assert "login endpoint" in request.messages[0]["content"]


@pytest.mark.asyncio
async def test_agent_run_success():
    mock_response = LLMResponse(
        content="Test response",
        provider="gemini",
        model="gemini-3.8-flash",
        usage=LLMUsage(
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30,
        ),
        latency_ms=100.0,
    )

    with patch(
        "core.agents.base.llm_service.generate",
        new=AsyncMock(return_value=mock_response),
    ):
        result: AgentResult = await agent_service.run(
            agent_name="architect",
            task="Design a test API",
        )

    assert result.success is True
    assert result.agent_name == "architect"
    assert result.output == "Test response"
    assert result.metadata["provider"] == "gemini"
    assert result.metadata["model"] == "gemini-3.8-flash"
    assert result.metadata["usage"]["total_tokens"] == 30


@pytest.mark.asyncio
async def test_agent_run_failure():
    with patch(
        "core.agents.base.llm_service.generate",
        new=AsyncMock(side_effect=RuntimeError("LLM unavailable")),
    ):
        result = await agent_service.run(
            agent_name="tester",
            task="Create tests",
        )

    assert result.success is False
    assert result.agent_name == "tester"
    assert result.error == "LLM unavailable"