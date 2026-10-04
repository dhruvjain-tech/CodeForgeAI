from dataclasses import dataclass


@dataclass(frozen=True)
class ToolPermission:
    tool_name: str
    allowed: bool = True
    requires_approval: bool = False


class ToolPermissionManager:

    def __init__(self):
        self.permissions: dict[str, ToolPermission] = {}

    def register(
        self,
        tool_name: str,
        allowed: bool = True,
        requires_approval: bool = False,
    ) -> None:
        self.permissions[tool_name] = ToolPermission(
            tool_name=tool_name,
            allowed=allowed,
            requires_approval=requires_approval,
        )

    def get(self, tool_name: str) -> ToolPermission:
        permission = self.permissions.get(tool_name)

        if permission is None:
            raise ValueError(
                f"No permission policy found for tool: {tool_name}"
            )

        return permission

    def is_allowed(self, tool_name: str) -> bool:
        return self.get(tool_name).allowed

    def requires_approval(self, tool_name: str) -> bool:
        return self.get(tool_name).requires_approval

    def revoke(self, tool_name: str) -> None:
        permission = self.get(tool_name)

        self.permissions[tool_name] = ToolPermission(
            tool_name=tool_name,
            allowed=False,
            requires_approval=permission.requires_approval,
        )