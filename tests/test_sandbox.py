from core.sandbox.manager import SandboxManager
from core.sandbox.types import SandboxConfig


def test_sandbox_python_execution(tmp_path):

    manager = SandboxManager(
        SandboxConfig(
            timeout_seconds=20,
        )
    )

    result = manager.run(
        command=[
            "python",
            "-c",
            "print('CodeForge Sandbox OK')",
        ],
        workspace=str(tmp_path),
    )

    assert result.success is True
    assert "CodeForge Sandbox OK" in result.stdout


def test_sandbox_network_disabled(tmp_path):

    manager = SandboxManager(
        SandboxConfig(
            timeout_seconds=20,
            network_disabled=True,
        )
    )

    result = manager.run(
        command=[
            "python",
            "-c",
            (
                "import urllib.request; "
                "urllib.request.urlopen("
                "'https://example.com'"
                ")"
            ),
        ],
        workspace=str(tmp_path),
    )

    assert result.success is False