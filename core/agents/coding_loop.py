from dataclasses import dataclass, field

from core.tools.service import ToolService

from .autonomous_coder import AutonomousCoder, CodeChange


@dataclass
class CodingLoopResult:
    success: bool
    changes_applied: int = 0
    test_output: str = ""
    test_error: str | None = None
    errors: list[str] = field(default_factory=list)


class CodingLoop:

    def __init__(self, tool_service: ToolService):
        self.tool_service = tool_service
        self.coder = AutonomousCoder(tool_service)

    async def execute(
        self,
        changes: list[CodeChange],
        workspace: str,
        test_command: list[str] | None = None,
        approved: bool = False,
    ) -> CodingLoopResult:

        # Step 1: Apply code changes
        code_result = await self.coder.apply_changes(
            changes=changes,
            approved=approved,
        )

        if not code_result.success:
            return CodingLoopResult(
                success=False,
                changes_applied=code_result.changes_applied,
                errors=code_result.errors,
            )

        # Step 2: Run tests inside secure sandbox
        command = test_command or [
            "pytest",
            "-q",
        ]

        test_result = await self.tool_service.execute(
            tool_name="sandbox_execute",
            arguments={
                "command": command,
                "workspace": workspace,
            },
            metadata={
                "source": "coding_loop",
                "operation": "test_code_changes",
            },
        )

        # Step 3: Handle test failure
        if not test_result.success:
            return CodingLoopResult(
                success=False,
                changes_applied=code_result.changes_applied,
                test_output=str(test_result.output or ""),
                test_error=(
                    test_result.error
                    or str(test_result.output or "")
                    or "Tests failed."
                ),
                errors=["Tests failed."],
            )

        # Step 4: Successful coding loop
        return CodingLoopResult(
            success=True,
            changes_applied=code_result.changes_applied,
            test_output=str(test_result.output or ""),
        )