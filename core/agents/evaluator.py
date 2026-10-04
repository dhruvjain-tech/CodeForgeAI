from typing import Any

from core.llm.types import LLMRequest, LLMResponse

from .base import BaseAgent


class EvaluatorAgent(BaseAgent):

    @property
    def agent_name(self) -> str:
        return "evaluator"

    @property
    def agent_role(self) -> str:
        return "Engineering task evaluation and outcome assessment"

    async def build_request(
        self,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> LLMRequest:

        context = context or {}

        prompt = f"""
You are the Evaluator Agent of CodeForge AI.

Your responsibility is to evaluate the outcome of a software
engineering task against its requirements and expected quality.

Task:
{task}

Evaluation Context:
{context}

Provide:
1. Task requirements
2. Completion assessment
3. Correctness assessment
4. Test results assessment
5. Code quality assessment
6. Security assessment
7. Performance assessment
8. Requirement gaps
9. Remaining risks
10. Overall score
11. Final verdict
12. Recommended next actions

Important:
- Do not claim that you executed tests or commands unless
  execution results are explicitly provided in the context.
- Do not invent missing evidence.
- Clearly distinguish verified results from assumptions.
- Evaluate objectively against the provided requirements.
- Identify both successful areas and failures.

Return a structured engineering evaluation.
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