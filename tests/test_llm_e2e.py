import os

import pytest

from core.llm.providers.gemini import GeminiProvider


@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.getenv("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not configured",
)
async def test_gemini_real_generation():
    provider = GeminiProvider()

    response = await provider.generate(
        [
            {
                "role": "user",
                "content": "Reply with exactly: CodeForge AI E2E working",
            }
        ]
    )

    assert response.content.strip() == "CodeForge AI E2E working"
    assert response.provider == "gemini"
    assert response.model == "gemini-3.8-flash"
    assert response.usage.total_tokens > 0
    assert response.latency_ms > 0