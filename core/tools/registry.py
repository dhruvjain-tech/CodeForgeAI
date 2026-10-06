from .base import BaseTool
from core.sandbox.tool import sandbox_tool


class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, BaseTool] = {}
        self.register(sandbox_tool)

    def register(self, tool: BaseTool) -> None:
        if tool.tool_name in self.tools:
            raise ValueError(
                f"Tool already registered: {tool.tool_name}"
            )

        self.tools[tool.tool_name] = tool

    def get(self, tool_name: str) -> BaseTool:
        tool = self.tools.get(tool_name)

        if tool is None:
            raise ValueError(f"Tool not registered: {tool_name}")

        return tool

    def list_tools(self) -> list[str]:
        return list(self.tools.keys())

    def unregister(self, tool_name: str) -> None:
        if tool_name not in self.tools:
            raise ValueError(f"Tool not registered: {tool_name}")

        del self.tools[tool_name]