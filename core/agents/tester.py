from typing import Any

from core.llm.types import LLMRequest, LLMResponse

from .base import BaseAgent


class TesterAgent(BaseAgent):

    @property
    def agent_name(self) -> str:
        return "tester"

    @property
    def agent_role(self) -> str:
        return "Test planning and quality validation"

    async def build_request(
        self,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> LLMRequest:

        context = context or {}

        prompt = f"""
You are the Tester Agent of CodeForge AI.

Your responsibility is to design a thorough testing strategy
for a software engineering task.

Task:
{task}

Project Context:
{context}

Provide:
1. Testing objectives
2. Unit test scenarios
3. Integration test scenarios
4. API or UI test scenarios when applicable
5. Positive test cases
6. Negative test cases
7. Edge cases
8. Regression risks
9. Expected validation criteria

Important:
- Do not claim that tests were executed.
- Do not modify files.
- Do not execute commands.
- Clearly distinguish planned tests from executed tests.
- Focus on reliable, reproducible validation.

Return a structured testing plan.
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