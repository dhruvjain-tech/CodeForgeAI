from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core.llm import LLMRequest, llm_service
from core.llm.providers import GeminiProvider
from core.llm.router import llm_router


router = APIRouter(prefix="/llm", tags=["LLM"])

llm_router.register_provider(GeminiProvider())


class LLMTestRequest(BaseModel):
    message: str
    provider: str = "gemini"


@router.post("/generate")
async def generate(request: LLMTestRequest):
    try:
        response = await llm_service.generate(
            LLMRequest(
                messages=[
                    {
                        "role": "user",
                        "content": request.message,
                    }
                ]
            ),
            provider=request.provider,
        )

        return {
            "content": response.content,
            "provider": response.provider,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            },
            "latency_ms": response.latency_ms,
            "cost": response.cost,
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=str(error),
        )