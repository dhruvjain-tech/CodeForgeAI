from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    """
    Common interface for every LLM provider used by CodeForge AI.

    All providers such as Gemini, Ollama, OpenAI, Anthropic, etc.
    must follow this interface.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the unique name of the provider."""
        raise NotImplementedError

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model currently used by the provider."""
        raise NotImplementedError

    @abstractmethod
    async def is_available(self) -> bool:
        """
        Check whether the provider is currently available.

        Examples:
        - API provider: check configuration/connectivity.
        - Local provider: check whether the local service is running.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Any:
        """
        Generate a response from the LLM provider.

        Provider-specific implementations will handle the actual
        communication with Gemini, Ollama, or another LLM.
        """
        raise NotImplementedError