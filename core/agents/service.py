from typing import Any

from .architect import ArchitectAgent
from .debugger import DebuggerAgent
from .developer import DeveloperAgent
from .evaluator import EvaluatorAgent
from .registry import AgentRegistry
from .researcher import ResearcherAgent
from .reviewer import ReviewerAgent
from .tester import TesterAgent
from .types import AgentResult


class AgentService:

    def __init__(self, registry: AgentRegistry):
        self.registry = registry

    async def run(
        self,
        agent_name: str,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> AgentResult:

        agent = self.registry.get(agent_name)

        return await agent.run(
            task=task,
            context=context or {},
        )


def create_default_registry() -> AgentRegistry:
    registry = AgentRegistry()

    agents = [
        ArchitectAgent(),
        ResearcherAgent(),
        DeveloperAgent(),
        TesterAgent(),
        DebuggerAgent(),
        ReviewerAgent(),
        EvaluatorAgent(),
    ]

    for agent in agents:
        registry.register(agent)

    return registry


agent_registry = create_default_registry()
agent_service = AgentService(agent_registry)
