from pathlib import Path

from .base import BaseTool
from .types import ToolRequest, ToolResult


class FileReadTool(BaseTool):

    @property
    def tool_name(self) -> str:
        return "file_read"

    @property
    def tool_description(self) -> str:
        return "Safely read the contents of a text file."

    async def execute(self, request: ToolRequest) -> ToolResult:
        try:
            self.validate_arguments(request.arguments)

            file_path = Path(request.arguments["path"])

            if not file_path.exists():
                return ToolResult(
                    tool_name=self.tool_name,
                    success=False,
                    error=f"File not found: {file_path}",
                )

            if not file_path.is_file():
                return ToolResult(
                    tool_name=self.tool_name,
                    success=False,
                    error=f"Path is not a file: {file_path}",
                )

            content = file_path.read_text(
                encoding="utf-8"
            )

            return ToolResult(
                tool_name=self.tool_name,
                success=True,
                output=content,
                metadata={
                    "path": str(file_path),
                    "size_bytes": file_path.stat().st_size,
                },
            )

        except UnicodeDecodeError:
            return ToolResult(
                tool_name=self.tool_name,
                success=False,
                error="File is not a valid UTF-8 text file.",
            )

        except Exception as exc:
            return ToolResult(
                tool_name=self.tool_name,
                success=False,
                error=str(exc),
            )

    def validate_arguments(self, arguments: dict) -> None:
        if "path" not in arguments:
            raise ValueError("Missing required argument: path")

        if not arguments["path"]:
            raise ValueError("File path cannot be empty")