from typing import Any

from ..base import LLMProvider


class OllamaProvider(LLMProvider):

    @property
    def provider_name(self) -> str:
        return "ollama"

    @property
    def model_name(self) -> str:
        return "ollama"

    async def is_available(self) -> bool:
        return False

    async def generate(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Any:
        raise NotImplementedError("Ollama provider is not connected yet.")