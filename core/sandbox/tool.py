import time
from typing import Any

from core.tools.base import BaseTool
from core.tools.types import ToolRequest, ToolResult

from .manager import SandboxManager


class SandboxTool(BaseTool):

    @property
    def tool_name(self) -> str:
        return "sandbox_execute"

    @property
    def tool_description(self) -> str:
        return (
            "Execute an allowed command inside the isolated "
            "CodeForge AI Docker sandbox."
        )

    @property
    def requires_approval(self) -> bool:
        return False

    def validate_arguments(
        self,
        arguments: dict[str, Any],
    ) -> None:

        command = arguments.get("command")
        workspace = arguments.get("workspace")

        if not isinstance(command, list) or not command:
            raise ValueError(
                "Command must be a non-empty list."
            )

        if not all(
            isinstance(item, str)
            for item in command
        ):
            raise ValueError(
                "All command arguments must be strings."
            )

        if not isinstance(workspace, str) or not workspace:
            raise ValueError(
                "Workspace must be a non-empty string."
            )

    async def execute(
        self,
        request: ToolRequest,
    ) -> ToolResult:

        started = time.perf_counter()

        try:
            self.validate_arguments(
                request.arguments
            )

            command = request.arguments["command"]
            workspace = request.arguments["workspace"]

            result = SandboxManager().run(
                command=command,
                workspace=workspace,
            )

            execution_time_ms = (
                time.perf_counter() - started
            ) * 1000

            return ToolResult(
                tool_name=self.tool_name,
                success=result.success,
                output=result.stdout,
                error=(
                    result.error
                    or result.stderr
                    or None
                ),
                metadata={
                    "exit_code": result.exit_code,
                    "timed_out": result.timed_out,
                    **result.metadata,
                },
                execution_time_ms=execution_time_ms,
            )

        except Exception as exc:

            execution_time_ms = (
                time.perf_counter() - started
            ) * 1000

            return ToolResult(
                tool_name=self.tool_name,
                success=False,
                output=None,
                error=str(exc),
                metadata={
                    "exception_type":
                        type(exc).__name__,
                },
                execution_time_ms=execution_time_ms,
            )


sandbox_tool = SandboxTool()