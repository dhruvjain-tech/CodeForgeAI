from .base import BaseAgent


class AgentRegistry:

    def __init__(self):
        self.agents: dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        self.agents[agent.agent_name] = agent

    def get(self, agent_name: str) -> BaseAgent:
        agent = self.agents.get(agent_name)

        if agent is None:
            raise ValueError(f"Agent not registered: {agent_name}")

        return agent

    def list_agents(self) -> list[str]:
        return list(self.agents.keys())


agent_registry = AgentRegistry()