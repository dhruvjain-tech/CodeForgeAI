from dataclasses import dataclass, field


@dataclass
class SandboxPolicy:
    allowed_commands: set[str] = field(
        default_factory=lambda: {
            "python",
            "python3",
            "pytest",
            "pip",
            "node",
            "npm",
        }
    )

    blocked_commands: set[str] = field(
        default_factory=lambda: {
            "powershell",
            "pwsh",
            "cmd",
            "shutdown",
            "format",
            "diskpart",
        }
    )

    max_timeout_seconds: int = 120
    max_memory_limit_mb: int = 1024
    max_cpu_limit: float = 2.0
    max_pids: int = 256

    def validate(
        self,
        command: list[str],
        timeout_seconds: int,
    ) -> tuple[bool, str | None]:

        if not command:
            return False, "Command cannot be empty."

        executable = command[0].lower()

        if executable in self.blocked_commands:
            return False, (
                f"Command '{executable}' is blocked."
            )

        if executable not in self.allowed_commands:
            return False, (
                f"Command '{executable}' is not allowed."
            )

        if timeout_seconds <= 0:
            return False, "Timeout must be positive."

        if timeout_seconds > self.max_timeout_seconds:
            return False, (
                f"Timeout exceeds maximum "
                f"of {self.max_timeout_seconds} seconds."
            )

        return True, None