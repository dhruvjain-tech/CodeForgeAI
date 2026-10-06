from dataclasses import dataclass, field
from typing import Any


@dataclass
class SandboxConfig:
    image: str = "python:3.13-slim"
    timeout_seconds: int = 30
    memory_limit: str = "512m"
    cpu_limit: float = 1.0
    pids_limit: int = 128
    network_disabled: bool = True
    read_only_root: bool = False


@dataclass
class SandboxResult:
    success: bool
    exit_code: int | None
    stdout: str
    stderr: str
    duration_ms: float
    timed_out: bool = False
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)