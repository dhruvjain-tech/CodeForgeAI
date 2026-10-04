from abc import ABC, abstractmethod
from typing import Any

from core.llm.types import LLMRequest, LLMResponse


class BaseAgent(ABC):

    @property
    @abstractmethod
    def agent_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def agent_role(self) -> str:
        raise NotImplementedError

    @abstractmethod
    async def build_request(
        self,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> LLMRequest:
        raise NotImplementedError

    async def run(
        self,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> LLMResponse:

        request = await self.build_request(
            task=task,
            context=context,
        )

        return await self.generate(request)

    @abstractmethod
    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        raise NotImplementedError