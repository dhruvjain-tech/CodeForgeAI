from .permissions import ToolPermissionManager
from .registry import ToolRegistry
from .service import ToolService


def create_tool_service() -> ToolService:
    registry = ToolRegistry(include_file_tools=True)

    permissions = ToolPermissionManager()

    for tool_name in registry.list_tools():
        permissions.register(
            tool_name=tool_name,
            allowed=True,
            requires_approval=False,
        )

    return ToolService(
        registry=registry,
        permission_manager=permissions,
    )


tool_service = create_tool_service()