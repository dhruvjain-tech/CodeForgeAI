import pytest

from core.tools.base import BaseTool
from core.tools.file_read import FileReadTool
from core.tools.file_search import FileSearchTool
from core.tools.file_write import FileWriteTool
from core.tools.git import GitTool
from core.tools.registry import ToolRegistry
from core.tools.terminal import TerminalTool
from core.tools.test_runner import TestRunnerTool
from core.tools.types import ToolRequest


class DummyTool(BaseTool):

    @property
    def tool_name(self) -> str:
        return "dummy"

    @property
    def tool_description(self) -> str:
        return "Dummy test tool."

    async def execute(self, request: ToolRequest):
        return None


def test_tool_registry_register_and_get():
    registry = ToolRegistry()
    tool = DummyTool()

    registry.register(tool)

    assert registry.get("dummy") is tool
    assert "dummy" in registry.list_tools()


def test_tool_registry_duplicate_registration():
    registry = ToolRegistry()
    tool = DummyTool()

    registry.register(tool)

    with pytest.raises(ValueError):
        registry.register(tool)


def test_file_read_validation():
    tool = FileReadTool()

    with pytest.raises(ValueError):
        tool.validate_arguments({})


def test_file_write_validation():
    tool = FileWriteTool()

    with pytest.raises(ValueError):
        tool.validate_arguments({"path": "test.txt"})


def test_file_search_validation():
    tool = FileSearchTool()

    with pytest.raises(ValueError):
        tool.validate_arguments({"path": "."})


def test_terminal_requires_approval():
    tool = TerminalTool()

    assert tool.requires_approval is True


def test_git_requires_approval():
    tool = GitTool()

    assert tool.requires_approval is True


def test_test_runner_requires_approval():
    tool = TestRunnerTool()

    assert tool.requires_approval is True