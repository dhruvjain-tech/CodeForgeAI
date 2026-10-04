import asyncio
import time

from .base import BaseTool
from .types import ToolRequest, ToolResult


class TestRunnerTool(BaseTool):

    @property
    def tool_name(self) -> str:
        return "test_runner"

    @property
    def tool_description(self) -> str:
        return "Run the project's automated test suite."

    @property
    def requires_approval(self) -> bool:
        return True

    async def execute(self, request: ToolRequest) -> ToolResult:
        start_time = time.perf_counter()

        try:
            self.validate_arguments(request.arguments)

            test_command = request.arguments.get(
                "command",
                "python -m pytest",
            )

            working_directory = request.arguments.get(
                "working_directory",
                ".",
            )

            process = await asyncio.create_subprocess_shell(
                test_command,
                cwd=working_directory,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            output = stdout.decode(
                "utf-8",
                errors="replace",
            )

            error_output = stderr.decode(
                "utf-8",
                errors="replace",
            )

            return ToolResult(
                tool_name=self.tool_name,
                success=process.returncode == 0,
                output=output,
                error=error_output if process.returncode != 0 else None,
                metadata={
                    "command": test_command,
                    "working_directory": working_directory,
                    "return_code": process.returncode,
                },
                execution_time_ms=(
                    time.perf_counter() - start_time
                ) * 1000,
            )

        except Exception as exc:
            return ToolResult(
                tool_name=self.tool_name,
                success=False,
                error=str(exc),
                execution_time_ms=(
                    time.perf_counter() - start_time
                ) * 1000,
            )

    def validate_arguments(self, arguments: dict) -> None:
        command = arguments.get("command")

        if command is not None and not command:
            raise ValueError(
                "Test command cannot be empty"
            )