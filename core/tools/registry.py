from .base import BaseTool
from .file_write import FileWriteTool
from core.sandbox.tool import sandbox_tool


class ToolRegistry:

    def __init__(
        self,
        include_file_tools: bool = False,
    ):
        self.tools: dict[str, BaseTool] = {}

        # Core sandbox tool is available by default.
        self.register(sandbox_tool)

        # File tools are opt-in so existing Phase 6 tests
        # and custom registries do not get duplicate registrations.
        if include_file_tools:
            self.register(FileWriteTool())

    def register(self, tool: BaseTool) -> None:
        if tool.tool_name in self.tools:
            raise ValueError(
                f"Tool already registered: {tool.tool_name}"
            )

        self.tools[tool.tool_name] = tool

    def get(self, tool_name: str) -> BaseTool:
        tool = self.tools.get(tool_name)

        if tool is None:
            raise ValueError(
                f"Tool not registered: {tool_name}"
            )

        return tool

    def list_tools(self) -> list[str]:
        return list(self.tools.keys())

    def unregister(self, tool_name: str) -> None:
        if tool_name not in self.tools:
            raise ValueError(
                f"Tool not registered: {tool_name}"
            )

        del self.tools[tool_name]