from typing import Any

from .autonomous_coder import AutonomousCoder, CodeChange
from .developer import DeveloperAgent
from .types import AgentResult


class CodingService:

    def __init__(
        self,
        developer: DeveloperAgent,
        autonomous_coder: AutonomousCoder,
    ):
        self.developer = developer
        self.autonomous_coder = autonomous_coder

    async def plan(
        self,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> AgentResult:

        return await self.developer.run(
            task=task,
            context=context or {},
        )

    async def apply(
        self,
        changes: list[CodeChange],
        approved: bool = False,
    ):
        return await self.autonomous_coder.apply_changes(
            changes=changes,
            approved=approved,
        )