from pathlib import Path

from .base import BaseTool
from .types import ToolRequest, ToolResult


class FileWriteTool(BaseTool):

    @property
    def tool_name(self) -> str:
        return "file_write"

    @property
    def tool_description(self) -> str:
        return "Safely create or overwrite a text file."

    @property
    def requires_approval(self) -> bool:
        return True

    async def execute(self, request: ToolRequest) -> ToolResult:
        try:
            self.validate_arguments(request.arguments)

            file_path = Path(request.arguments["path"])
            content = request.arguments["content"]

            file_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            file_path.write_text(
                content,
                encoding="utf-8",
            )

            return ToolResult(
                tool_name=self.tool_name,
                success=True,
                output=f"File written successfully: {file_path}",
                metadata={
                    "path": str(file_path),
                    "size_bytes": file_path.stat().st_size,
                },
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

        if "content" not in arguments:
            raise ValueError("Missing required argument: content")

        if not arguments["path"]:
            raise ValueError("File path cannot be empty")