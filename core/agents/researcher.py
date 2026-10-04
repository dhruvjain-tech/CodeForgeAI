from typing import Any

from core.llm.types import LLMRequest, LLMResponse

from .base import BaseAgent


class ResearcherAgent(BaseAgent):

    @property
    def agent_name(self) -> str:
        return "researcher"

    @property
    def agent_role(self) -> str:
        return "Technical research and information analysis"

    async def build_request(
        self,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> LLMRequest:

        context = context or {}

        prompt = f"""
You are the Researcher Agent of CodeForge AI.

Your responsibility is to research and analyze the technical
requirements of a software engineering task.

Task:
{task}

Project Context:
{context}

Provide:
1. Technical requirements
2. Relevant technologies and libraries
3. Important implementation considerations
4. Potential technical risks
5. Recommended approach
6. Information the Developer Agent needs
7. Testing considerations

Do not modify files.
Do not execute commands.
Do not invent project-specific facts that are not present
in the provided context.
Return a structured technical research summary.
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