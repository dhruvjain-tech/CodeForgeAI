import pytest

from core.llm.router import LLMRouter
from core.llm.types import LLMRequest, LLMResponse, LLMUsage
from core.llm.providers.gemini import GeminiProvider
from core.llm.errors import LLMConfigurationError


def test_llm_request_defaults():
    request = LLMRequest(
        messages=[
            {"role": "user", "content": "Hello"}
        ]
    )

    assert request.temperature == 0.2
    assert request.max_tokens is None
    assert request.model is None


def test_llm_response_structure():
    response = LLMResponse(
        content="CodeForge AI",
        provider="gemini",
        model="gemini-3.8-flash",
        usage=LLMUsage(
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
        ),
        latency_ms=100.0,
    )

    assert response.content == "CodeForge AI"
    assert response.provider == "gemini"
    assert response.model == "gemini-3.8-flash"
    assert response.usage.total_tokens == 15


def test_router_register_and_get_provider():
    router = LLMRouter()

    provider = GeminiProvider()
    router.register_provider(provider)

    result = router.get_provider("gemini")

    assert result is provider
    assert result.provider_name == "gemini"


def test_router_unknown_provider():
    router = LLMRouter()

    with pytest.raises(ValueError):
        router.get_provider("unknown-provider")


@pytest.mark.asyncio
async def test_gemini_missing_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    provider = GeminiProvider()

    assert await provider.is_available() is False

    with pytest.raises(LLMConfigurationError, match="GEMINI_API_KEY"):
        await provider.generate(
            [
                {"role": "user", "content": "Hello"}
            ]
        )