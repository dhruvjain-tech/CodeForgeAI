from typing import Any

from core.llm.types import LLMRequest, LLMResponse

from .base import BaseAgent


class DeveloperAgent(BaseAgent):

    @property
    def agent_name(self) -> str:
        return "developer"

    @property
    def agent_role(self) -> str:
        return "Software implementation and code generation"

    async def build_request(
        self,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> LLMRequest:

        context = context or {}

        prompt = f"""
You are the Developer Agent of CodeForge AI.

Your responsibility is to design the implementation for a
software engineering task.

Task:
{task}

Project Context:
{context}

Provide:
1. Implementation approach
2. Files/modules that should be created or modified
3. Required code changes
4. Dependencies or configuration required
5. Edge cases
6. Testing requirements
7. Potential implementation risks

Important:
- Do not claim that files were modified.
- Do not execute commands.
- Do not invent files or project details not provided in the context.
- Prefer maintainable, production-quality solutions.
- Clearly separate assumptions from confirmed information.

Return a structured implementation plan suitable for execution
by a future coding tool.
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