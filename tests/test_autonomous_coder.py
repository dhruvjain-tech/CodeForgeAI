import asyncio

from core.agents.autonomous_coder import (
    AutonomousCoder,
    CodeChange,
)
from core.tools.permissions import ToolPermissionManager
from core.tools.registry import ToolRegistry
from core.tools.runtime import create_tool_service


def test_autonomous_coder_requires_approval(tmp_path):

    tool_service = create_tool_service()

    coder = AutonomousCoder(tool_service)

    change = CodeChange(
        path=str(tmp_path / "hello.py"),
        content="print('Hello CodeForge AI')",
    )

    result = asyncio.run(
        coder.apply_changes(
            changes=[change],
            approved=False,
        )
    )

    assert result.success is False
    assert result.changes_applied == 0
    assert result.errors


def test_autonomous_coder_applies_change_with_approval(tmp_path):

    tool_service = create_tool_service()

    coder = AutonomousCoder(tool_service)

    file_path = tmp_path / "hello.py"

    change = CodeChange(
        path=str(file_path),
        content="print('Hello CodeForge AI')",
    )

    result = asyncio.run(
        coder.apply_changes(
            changes=[change],
            approved=True,
        )
    )

    assert result.success is True
    assert result.changes_applied == 1
    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == (
        "print('Hello CodeForge AI')"
    )