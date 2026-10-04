from typing import Any

from core.llm.types import LLMRequest, LLMResponse

from .base import BaseAgent


class ReviewerAgent(BaseAgent):

    @property
    def agent_name(self) -> str:
        return "reviewer"

    @property
    def agent_role(self) -> str:
        return "Code review and quality assessment"

    async def build_request(
        self,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> LLMRequest:

        context = context or {}

        prompt = f"""
You are the Reviewer Agent of CodeForge AI.

Your responsibility is to review software implementation quality,
correctness, security, performance, maintainability, and risks.

Task:
{task}

Review Context:
{context}

Provide:
1. Implementation summary
2. Correctness assessment
3. Code quality assessment
4. Security concerns
5. Performance concerns
6. Maintainability concerns
7. Error handling assessment
8. Testing coverage concerns
9. Potential regressions
10. Recommended improvements
11. Overall review verdict

Important:
- Do not claim that you executed code or tests.
- Do not modify files.
- Do not invent implementation details that are not provided.
- Clearly distinguish confirmed issues from potential risks.
- Prioritize findings by severity.

Return a structured code review.
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