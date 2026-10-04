from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentRequest:
    task: str
    context: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    agent_name: str
    success: bool
    output: str
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    latency_ms: float = 0.0