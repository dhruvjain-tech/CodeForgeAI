import subprocess
import time

from .policy import SandboxPolicy
from .types import SandboxConfig, SandboxResult


class SandboxManager:

    def __init__(
        self,
        config: SandboxConfig | None = None,
        policy: SandboxPolicy | None = None,
    ):
        self.config = config or SandboxConfig()
        self.policy = policy or SandboxPolicy()

    def run(
        self,
        command: list[str],
        workspace: str,
    ) -> SandboxResult:

        valid, validation_error = self.policy.validate(
            command=command,
            timeout_seconds=self.config.timeout_seconds,
        )

        if not valid:
            return SandboxResult(
                success=False,
                exit_code=None,
                stdout="",
                stderr="",
                duration_ms=0.0,
                error=validation_error,
                metadata={
                    "blocked_by_policy": True,
                },
            )

        docker_command = [
            "docker",
            "run",
            "--rm",
            "--memory",
            self.config.memory_limit,
            "--cpus",
            str(self.config.cpu_limit),
            "--pids-limit",
            str(self.config.pids_limit),
            "--security-opt",
            "no-new-privileges",
            "--cap-drop",
            "ALL",
            "--workdir",
            "/workspace",
            "-v",
            f"{workspace}:/workspace",
        ]

        if self.config.network_disabled:
            docker_command.extend(
                [
                    "--network",
                    "none",
                ]
            )

        if self.config.read_only_root:
            docker_command.append("--read-only")

        docker_command.extend(
            [
                self.config.image,
                *command,
            ]
        )

        started = time.perf_counter()

        try:
            completed = subprocess.run(
                docker_command,
                capture_output=True,
                text=True,
                timeout=self.config.timeout_seconds,
                check=False,
            )

            duration_ms = (
                time.perf_counter() - started
            ) * 1000

            return SandboxResult(
                success=completed.returncode == 0,
                exit_code=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
                duration_ms=duration_ms,
                metadata={
                    "image": self.config.image,
                    "memory_limit": self.config.memory_limit,
                    "cpu_limit": self.config.cpu_limit,
                    "pids_limit": self.config.pids_limit,
                    "network_disabled":
                        self.config.network_disabled,
                    "workspace": workspace,
                    "blocked_by_policy": False,
                },
            )

        except subprocess.TimeoutExpired as exc:
            duration_ms = (
                time.perf_counter() - started
            ) * 1000

            stdout = exc.stdout or ""
            stderr = exc.stderr or ""

            if isinstance(stdout, bytes):
                stdout = stdout.decode(
                    "utf-8",
                    errors="replace",
                )

            if isinstance(stderr, bytes):
                stderr = stderr.decode(
                    "utf-8",
                    errors="replace",
                )

            return SandboxResult(
                success=False,
                exit_code=None,
                stdout=stdout,
                stderr=stderr,
                duration_ms=duration_ms,
                timed_out=True,
                error="Sandbox execution timed out.",
            )

        except FileNotFoundError:
            duration_ms = (
                time.perf_counter() - started
            ) * 1000

            return SandboxResult(
                success=False,
                exit_code=None,
                stdout="",
                stderr="",
                duration_ms=duration_ms,
                error=(
                    "Docker executable was not found. "
                    "Make sure Docker Desktop is installed "
                    "and running."
                ),
            )

        except Exception as exc:
            duration_ms = (
                time.perf_counter() - started
            ) * 1000

            return SandboxResult(
                success=False,
                exit_code=None,
                stdout="",
                stderr="",
                duration_ms=duration_ms,
                error=str(exc),
                metadata={
                    "exception_type": type(exc).__name__,
                },
            )


sandbox_manager = SandboxManager()