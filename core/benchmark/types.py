from dataclasses import dataclass, field
from typing import Any


@dataclass
class BenchmarkMetric:
    name: str
    value: float
    unit: str
    lower_is_better: bool = True


@dataclass
class BenchmarkResult:
    technology: str
    benchmark_name: str
    success: bool
    duration_ms: float
    metrics: list[BenchmarkMetric] = field(
        default_factory=list
    )
    error: str | None = None
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class BenchmarkComparison:
    benchmark_name: str
    results: list[BenchmarkResult] = field(
        default_factory=list
    )
    winner: str | None = None
    reasoning: list[str] = field(
        default_factory=list
    )