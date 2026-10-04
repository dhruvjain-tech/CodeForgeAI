from typing import Any

from core.tools.service import ToolService
from core.tools.types import ToolResult


class AgentToolAccess:

    def __init__(self, tool_service: ToolService):
        self.tool_service = tool_service

    async def use_tool(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        approved: bool = False,
    ) -> ToolResult:

        return await self.tool_service.execute(
            tool_name=tool_name,
            arguments=arguments,
            metadata=metadata,
            approved=approved,
        )