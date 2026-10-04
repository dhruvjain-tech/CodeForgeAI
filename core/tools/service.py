from typing import Any

from .permissions import ToolPermissionManager
from .registry import ToolRegistry
from .types import ToolRequest, ToolResult


class ToolService:

    def __init__(
        self,
        registry: ToolRegistry,
        permission_manager: ToolPermissionManager,
    ):
        self.registry = registry
        self.permission_manager = permission_manager

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        approved: bool = False,
    ) -> ToolResult:

        tool = self.registry.get(tool_name)
        permission = self.permission_manager.get(tool_name)

        if not permission.allowed:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                error=f"Tool execution denied: {tool_name}",
            )

        requires_approval = (
            permission.requires_approval
            or tool.requires_approval
        )

        if requires_approval and not approved:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                error=(
                    f"Approval required before executing tool: "
                    f"{tool_name}"
                ),
            )

        request = ToolRequest(
            tool_name=tool_name,
            arguments=arguments or {},
            metadata=metadata or {},
        )

        try:
            return await tool.execute(request)

        except Exception as exc:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                error=str(exc),
            )