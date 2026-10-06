import asyncio

from core.agents.autonomous_coder import AutonomousCoder, CodeChange
from core.agents.coding_service import CodingService
from core.agents.developer import DeveloperAgent
from core.tools.runtime import create_tool_service


def test_coding_service_apply(tmp_path):
    tool_service = create_tool_service()

    coder = AutonomousCoder(tool_service)

    service = CodingService(
        developer=DeveloperAgent(),
        autonomous_coder=coder,
    )

    file_path = tmp_path / "generated.py"

    result = asyncio.run(
        service.apply(
            changes=[
                CodeChange(
                    path=str(file_path),
                    content="print('CodeForge AI')",
                )
            ],
            approved=True,
        )
    )

    assert result.success is True
    assert result.changes_applied == 1
    assert file_path.exists()