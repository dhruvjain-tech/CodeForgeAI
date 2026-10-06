import asyncio

from core.sandbox.tool import SandboxTool
from core.tools.types import ToolRequest


def test_sandbox_tool_execution(tmp_path):

    tool = SandboxTool()

    request = ToolRequest(
        tool_name="sandbox_execute",
        arguments={
            "command": [
                "python",
                "-c",
                "print('Tool Sandbox OK')",
            ],
            "workspace": str(tmp_path),
        },
    )

    result = asyncio.run(
        tool.execute(request)
    )

    assert result.tool_name == "sandbox_execute"
    assert result.success is True
    assert "Tool Sandbox OK" in result.output


def test_sandbox_tool_blocks_command(tmp_path):

    tool = SandboxTool()

    request = ToolRequest(
        tool_name="sandbox_execute",
        arguments={
            "command": [
                "powershell",
                "-Command",
                "whoami",
            ],
            "workspace": str(tmp_path),
        },
    )

    result = asyncio.run(
        tool.execute(request)
    )

    assert result.tool_name == "sandbox_execute"
    assert result.success is False
    assert result.error is not None