import asyncio

from core.agents.tool_access import AgentToolAccess
from core.tools.permissions import ToolPermissionManager
from core.tools.registry import ToolRegistry
from core.tools.service import ToolService


def test_agent_can_execute_sandbox_tool(tmp_path):
    registry = ToolRegistry()

    permissions = ToolPermissionManager()
    permissions.register(
        "sandbox_execute",
        allowed=True,
        requires_approval=False,
    )

    service = ToolService(
        registry=registry,
        permission_manager=permissions,
    )

    access = AgentToolAccess(service)

    result = asyncio.run(
        access.use_tool(
            tool_name="sandbox_execute",
            arguments={
                "command": [
                    "python",
                    "-c",
                    "print('CodeForge Agent Sandbox OK')",
                ],
                "workspace": str(tmp_path),
            },
        )
    )

    assert result.tool_name == "sandbox_execute"
    assert result.success is True
    assert "CodeForge Agent Sandbox OK" in result.output


def test_agent_sandbox_permission_denied(tmp_path):
    registry = ToolRegistry()

    permissions = ToolPermissionManager()
    permissions.register(
        "sandbox_execute",
        allowed=False,
    )

    service = ToolService(
        registry=registry,
        permission_manager=permissions,
    )

    access = AgentToolAccess(service)

    result = asyncio.run(
        access.use_tool(
            tool_name="sandbox_execute",
            arguments={
                "command": ["python", "-c", "print('blocked')"],
                "workspace": str(tmp_path),
            },
        )
    )

    assert result.tool_name == "sandbox_execute"
    assert result.success is False
    assert "denied" in result.error.lower()