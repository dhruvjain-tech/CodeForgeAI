from typing import Any

from .router import llm_router
from .types import LLMRequest, LLMResponse


class LLMService:

    async def generate(
        self,
        request: LLMRequest,
        provider: str | None = None,
    ) -> LLMResponse:

        llm_provider = llm_router.get_provider(provider)

        response = await llm_provider.generate(
            request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            metadata=request.metadata,
        )

        return response


llm_service = LLMService()