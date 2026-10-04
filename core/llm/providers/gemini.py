import asyncio
import os
import time
from typing import Any

from dotenv import load_dotenv
from google import genai
from pathlib import Path
from google.genai import types
from google.genai.errors import ServerError

from ..base import LLMProvider
from ..errors import (
    LLMConfigurationError,
    LLMProviderUnavailableError,
    LLMRequestError,
)
from ..types import LLMResponse, LLMUsage

load_dotenv(
    Path(__file__).resolve().parents[3] / "apps" / "api" / ".env"
)


class GeminiProvider(LLMProvider):

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self._client = None
        self.max_retries = 3

        if self.api_key:
            self._client = genai.Client(api_key=self.api_key)

    @property
    def provider_name(self) -> str:
        return "gemini"

    @property
    def model_name(self) -> str:
        return os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    async def is_available(self) -> bool:
        return self._client is not None

    async def generate(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> LLMResponse:

        if not self.api_key or not self._client:
            raise LLMConfigurationError(
                "GEMINI_API_KEY is not configured."
            )

        contents = [
            types.Content(
                role="user" if message["role"] == "user" else "model",
                parts=[
                    types.Part.from_text(
                        text=message["content"]
                    )
                ],
            )
            for message in messages
        ]

        start_time = time.perf_counter()

        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.aio.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    ),
                )

                latency_ms = (
                    time.perf_counter() - start_time
                ) * 1000

                usage = LLMUsage()

                if response.usage_metadata:
                    usage.prompt_tokens = (
                        response.usage_metadata.prompt_token_count or 0
                    )
                    usage.completion_tokens = (
                        response.usage_metadata.candidates_token_count or 0
                    )
                    usage.total_tokens = (
                        response.usage_metadata.total_token_count or 0
                    )

                return LLMResponse(
                    content=response.text or "",
                    provider=self.provider_name,
                    model=self.model_name,
                    usage=usage,
                    latency_ms=latency_ms,
                    metadata=metadata or {},
                )

            except ServerError as error:
                if attempt >= self.max_retries:
                    raise LLMProviderUnavailableError(
                        f"Gemini provider unavailable after "
                        f"{self.max_retries + 1} attempts."
                    ) from error

                wait_seconds = 2 ** attempt

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_seconds}s..."
                )

                await asyncio.sleep(wait_seconds)

            except Exception as error:
                raise LLMRequestError(
                    f"Gemini request failed: {error}"
                ) from error