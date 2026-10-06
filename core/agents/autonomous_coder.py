from dataclasses import dataclass, field
from typing import Any

from core.tools.service import ToolService


@dataclass
class CodeChange:
    path: str
    content: str


@dataclass
class AutonomousCoderResult:
    success: bool
    changes_applied: int = 0
    outputs: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class AutonomousCoder:

    def __init__(self, tool_service: ToolService):
        self.tool_service = tool_service

    async def apply_changes(
        self,
        changes: list[CodeChange],
        approved: bool = False,
    ) -> AutonomousCoderResult:

        result = AutonomousCoderResult(success=True)

        for change in changes:

            tool_result = await self.tool_service.execute(
                tool_name="file_write",
                arguments={
                    "path": change.path,
                    "content": change.content,
                },
                metadata={
                    "source": "autonomous_coder",
                    "operation": "apply_code_change",
                },
                approved=approved,
            )

            if not tool_result.success:
                result.success = False

                result.errors.append(
                    tool_result.error
                    or f"Failed to write file: {change.path}"
                )

                break

            result.changes_applied += 1

            if tool_result.output:
                result.outputs.append(
                    str(tool_result.output)
                )

        return result