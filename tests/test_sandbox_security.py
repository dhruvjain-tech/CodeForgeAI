from core.sandbox.manager import SandboxManager
from core.sandbox.types import SandboxConfig


def test_blocked_command(tmp_path):

    manager = SandboxManager()

    result = manager.run(
        command=["powershell", "-Command", "whoami"],
        workspace=str(tmp_path),
    )

    assert result.success is False
    assert "blocked" in result.error.lower()


def test_unknown_command_rejected(tmp_path):

    manager = SandboxManager()

    result = manager.run(
        command=["unknown-command"],
        workspace=str(tmp_path),
    )

    assert result.success is False
    assert "not allowed" in result.error.lower()


def test_timeout_limit_rejected(tmp_path):

    manager = SandboxManager(
        SandboxConfig(
            timeout_seconds=999,
        )
    )

    result = manager.run(
        command=["python", "-c", "print('test')"],
        workspace=str(tmp_path),
    )

    assert result.success is False
    assert "maximum" in result.error.lower()