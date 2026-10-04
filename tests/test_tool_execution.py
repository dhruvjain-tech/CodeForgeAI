import pytest

from core.tools.file_read import FileReadTool
from core.tools.file_write import FileWriteTool
from core.tools.permissions import ToolPermissionManager
from core.tools.registry import ToolRegistry
from core.tools.service import ToolService


@pytest.mark.asyncio
async def test_file_read_end_to_end(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text(
        "CodeForge AI Tool System",
        encoding="utf-8",
    )

    registry = ToolRegistry()
    permissions = ToolPermissionManager()

    tool = FileReadTool()

    registry.register(tool)

    permissions.register(
        tool_name="file_read",
        allowed=True,
        requires_approval=False,
    )

    service = ToolService(
        registry=registry,
        permission_manager=permissions,
    )

    result = await service.execute(
        tool_name="file_read",
        arguments={
            "path": str(test_file),
        },
    )

    assert result.success is True
    assert result.output == "CodeForge AI Tool System"


@pytest.mark.asyncio
async def test_file_write_requires_approval(tmp_path):
    test_file = tmp_path / "output.txt"

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
            "path": str(test_file),
            "content": "Hello CodeForge AI",
        },
    )

    assert result.success is False
    assert "Approval required" in result.error


@pytest.mark.asyncio
async def test_file_write_with_approval(tmp_path):
    test_file = tmp_path / "approved.txt"

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
            "path": str(test_file),
            "content": "Approved write",
        },
        approved=True,
    )

    assert result.success is True
    assert test_file.read_text(encoding="utf-8") == "Approved write"