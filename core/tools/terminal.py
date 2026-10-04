import asyncio
import time

from .base import BaseTool
from .types import ToolRequest, ToolResult


class TerminalTool(BaseTool):

    @property
    def tool_name(self) -> str:
        return "terminal"

    @property
    def tool_description(self) -> str:
        return "Execute a terminal command and return its output."

    @property
    def requires_approval(self) -> bool:
        return True

    async def execute(self, request: ToolRequest) -> ToolResult:
        start_time = time.perf_counter()

        try:
            self.validate_arguments(request.arguments)

            command = request.arguments["command"]
            timeout = request.arguments.get("timeout", 30)

            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.communicate()

                return ToolResult(
                    tool_name=self.tool_name,
                    success=False,
                    error=f"Command timed out after {timeout} seconds.",
                    execution_time_ms=(
                        time.perf_counter() - start_time
                    ) * 1000,
                )

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
                    "command": command,
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
        if "command" not in arguments:
            raise ValueError("Missing required argument: command")

        if not arguments["command"]:
            raise ValueError("Terminal command cannot be empty")

        timeout = arguments.get("timeout", 30)

        if not isinstance(timeout, (int, float)):
            raise ValueError("Timeout must be a number")

        if timeout <= 0:
            raise ValueError("Timeout must be greater than zero")