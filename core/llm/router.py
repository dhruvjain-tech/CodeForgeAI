from .config import llm_config
from .base import LLMProvider


class LLMRouter:

    def __init__(self):
        self.providers: dict[str, LLMProvider] = {}

    def register_provider(self, provider: LLMProvider) -> None:
        self.providers[provider.provider_name] = provider

    def get_provider(self, provider_name: str | None = None) -> LLMProvider:
        name = provider_name or llm_config.default_provider

        provider = self.providers.get(name)

        if provider is None:
            raise ValueError(f"LLM provider not registered: {name}")

        return provider


llm_router = LLMRouter()