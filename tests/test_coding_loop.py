import asyncio

from core.agents.autonomous_coder import CodeChange
from core.agents.coding_loop import CodingLoop
from core.tools.runtime import create_tool_service


def test_coding_loop_writes_and_tests(tmp_path):

    test_file = tmp_path / "test_generated.py"

    test_file.write_text(
        """
def test_generated_code():
    assert 2 + 2 == 4
""",
        encoding="utf-8",
    )

    service = create_tool_service()
    loop = CodingLoop(service)

    result = asyncio.run(
        loop.execute(
            changes=[
                CodeChange(
                    path=str(tmp_path / "generated.py"),
                    content="VALUE = 42\n",
                )
            ],
            workspace=str(tmp_path),
            test_command=["pytest", "-q"],
            approved=True,
        )
    )

    assert result.success is True
    assert result.changes_applied == 1
    assert "passed" in result.test_output


def test_coding_loop_stops_when_tests_fail(tmp_path):

    test_file = tmp_path / "test_generated.py"

    test_file.write_text(
        """
def test_generated_code():
    assert 2 + 2 == 5
""",
        encoding="utf-8",
    )

    service = create_tool_service()
    loop = CodingLoop(service)

    result = asyncio.run(
        loop.execute(
            changes=[
                CodeChange(
                    path=str(tmp_path / "generated.py"),
                    content="VALUE = 42\n",
                )
            ],
            workspace=str(tmp_path),
            test_command=["pytest", "-q"],
            approved=True,
        )
    )

    assert result.success is False
    assert result.changes_applied == 1
    assert result.test_error is not None