from typing import Any

from core.llm.types import LLMRequest, LLMResponse

from .base import BaseAgent


class ArchitectAgent(BaseAgent):

    @property
    def agent_name(self) -> str:
        return "architect"

    @property
    def agent_role(self) -> str:
        return "Software architecture and task planning"

    async def build_request(
        self,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> LLMRequest:

        context = context or {}

        prompt = f"""
You are the Architect Agent of CodeForge AI.

Your responsibility is to analyze a software engineering task
and create a clear implementation plan.

Task:
{task}

Project Context:
{context}

Provide:
1. Problem understanding
2. Technical approach
3. Architecture/components involved
4. Files or modules likely affected
5. Implementation steps
6. Risks and considerations
7. Testing strategy

Do not modify files.
Do not execute commands.
Return a structured engineering plan.
"""

        return LLMRequest(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        from core.llm.service import llm_service

        return await llm_service.generate(request)