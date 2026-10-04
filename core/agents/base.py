from abc import ABC, abstractmethod
from typing import Any

from core.llm.service import llm_service
from core.llm.types import LLMRequest, LLMResponse

from .types import AgentResult


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
    ) -> AgentResult:

        try:
            request = await self.build_request(
                task=task,
                context=context or {},
            )

            response: LLMResponse = await llm_service.generate(request)

            return AgentResult(
                agent_name=self.agent_name,
                success=True,
                output=response.content,
                metadata={
                    "provider": response.provider,
                    "model": response.model,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                    },
                },
                latency_ms=response.latency_ms,
            )

        except Exception as exc:
            return AgentResult(
                agent_name=self.agent_name,
                success=False,
                output="",
                error=str(exc),
            )

    @abstractmethod
    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        raise NotImplementedError