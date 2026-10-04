from abc import ABC, abstractmethod
from typing import Any

from .types import ToolRequest, ToolResult


class BaseTool(ABC):

    @property
    @abstractmethod
    def tool_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def tool_description(self) -> str:
        raise NotImplementedError

    @property
    def requires_approval(self) -> bool:
        return False

    @abstractmethod
    async def execute(
        self,
        request: ToolRequest,
    ) -> ToolResult:
        raise NotImplementedError

    def validate_arguments(
        self,
        arguments: dict[str, Any],
    ) -> None:
        return None