from pathlib import Path

from .base import BaseTool
from .types import ToolRequest, ToolResult


class FileSearchTool(BaseTool):

    @property
    def tool_name(self) -> str:
        return "file_search"

    @property
    def tool_description(self) -> str:
        return "Search for text inside files within a directory."

    async def execute(self, request: ToolRequest) -> ToolResult:
        try:
            self.validate_arguments(request.arguments)

            root_path = Path(request.arguments["path"])
            query = request.arguments["query"]

            if not root_path.exists():
                return ToolResult(
                    tool_name=self.tool_name,
                    success=False,
                    error=f"Directory not found: {root_path}",
                )

            if not root_path.is_dir():
                return ToolResult(
                    tool_name=self.tool_name,
                    success=False,
                    error=f"Path is not a directory: {root_path}",
                )

            matches = []

            for file_path in root_path.rglob("*"):
                if not file_path.is_file():
                    continue

                try:
                    content = file_path.read_text(
                        encoding="utf-8"
                    )
                except (UnicodeDecodeError, PermissionError):
                    continue

                if query.lower() in content.lower():
                    matches.append(str(file_path))

            return ToolResult(
                tool_name=self.tool_name,
                success=True,
                output=matches,
                metadata={
                    "query": query,
                    "match_count": len(matches),
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

        if "query" not in arguments:
            raise ValueError("Missing required argument: query")

        if not arguments["path"]:
            raise ValueError("Search path cannot be empty")

        if not arguments["query"]:
            raise ValueError("Search query cannot be empty")