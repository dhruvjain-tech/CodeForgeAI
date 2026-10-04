import asyncio
import time

from .base import BaseTool
from .types import ToolRequest, ToolResult


class GitTool(BaseTool):

    @property
    def tool_name(self) -> str:
        return "git"

    @property
    def tool_description(self) -> str:
        return "Execute safe Git operations inside a repository."

    @property
    def requires_approval(self) -> bool:
        return True

    async def execute(self, request: ToolRequest) -> ToolResult:
        start_time = time.perf_counter()

        try:
            self.validate_arguments(request.arguments)

            operation = request.arguments["operation"]
            repository = request.arguments.get("repository", ".")

            allowed_operations = {
                "status": ["git", "status", "--short"],
                "log": ["git", "log", "--oneline", "-10"],
                "branch": ["git", "branch"],
                "diff": ["git", "diff"],
            }

            command = allowed_operations.get(operation)

            if command is None:
                return ToolResult(
                    tool_name=self.tool_name,
                    success=False,
                    error=f"Unsupported Git operation: {operation}",
                )

            process = await asyncio.create_subprocess_exec(
                *command,
                cwd=repository,
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
                    "operation": operation,
                    "repository": repository,
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
        if "operation" not in arguments:
            raise ValueError(
                "Missing required argument: operation"
            )

        if not arguments["operation"]:
            raise ValueError(
                "Git operation cannot be empty"
            )