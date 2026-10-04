from typing import Any

from core.llm.types import LLMRequest, LLMResponse

from .base import BaseAgent


class DebuggerAgent(BaseAgent):

    @property
    def agent_name(self) -> str:
        return "debugger"

    @property
    def agent_role(self) -> str:
        return "Error analysis and debugging"

    async def build_request(
        self,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> LLMRequest:

        context = context or {}

        prompt = f"""
You are the Debugger Agent of CodeForge AI.

Your responsibility is to analyze software errors, failures,
exceptions, test failures, and unexpected behavior.

Task:
{task}

Debugging Context:
{context}

Provide:
1. Problem summary
2. Observed error or failure
3. Most likely root cause
4. Evidence supporting the diagnosis
5. Possible contributing factors
6. Recommended fix
7. Regression risks
8. Tests required to verify the fix

Important:
- Do not claim that you executed commands or tests.
- Do not modify files.
- Do not invent error details that are not provided.
- Clearly distinguish evidence from hypotheses.
- Prefer the smallest safe fix.

Return a structured debugging analysis.
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