import pytest

from core.tools.file_write import FileWriteTool
from core.tools.permissions import ToolPermissionManager
from core.tools.registry import ToolRegistry
from core.tools.service import ToolService
from core.tools.terminal import TerminalTool


def test_file_write_requires_approval():
    tool = FileWriteTool()

    assert tool.requires_approval is True


def test_terminal_requires_approval():
    tool = TerminalTool()

    assert tool.requires_approval is True


def test_permission_manager_denies_revoked_tool():
    manager = ToolPermissionManager()

    manager.register(
        tool_name="terminal",
        allowed=True,
        requires_approval=True,
    )

    manager.revoke("terminal")

    assert manager.is_allowed("terminal") is False


@pytest.mark.asyncio
async def test_tool_service_denies_disallowed_tool():
    registry = ToolRegistry()
    permissions = ToolPermissionManager()

    tool = TerminalTool()

    registry.register(tool)

    permissions.register(
        tool_name="terminal",
        allowed=False,
        requires_approval=True,
    )

    service = ToolService(
        registry=registry,
        permission_manager=permissions,
    )

    result = await service.execute(
        tool_name="terminal",
        arguments={"command": "echo hello"},
        approved=True,
    )

    assert result.success is False
    assert "denied" in result.error.lower()


@pytest.mark.asyncio
async def test_tool_service_blocks_missing_approval():
    registry = ToolRegistry()
    permissions = ToolPermissionManager()

    tool = FileWriteTool()

    registry.register(tool)

    permissions.register(
        tool_name="file_write",
        allowed=True,
        requires_approval=True,
    )

    service = ToolService(
        registry=registry,
        permission_manager=permissions,
    )

    result = await service.execute(
        tool_name="file_write",
        arguments={
            "path": "security_test.txt",
            "content": "blocked",
        },
    )

    assert result.success is False
    assert "approval required" in result.error.lower()