from core.benchmark.decision_integration import (
    BenchmarkDecisionIntegrator,
)
from core.benchmark.engine import BenchmarkEngine
from core.repository.technology_advisor import (
    TechnologyOption,
)
from core.repository.technology_decision import (
    TechnologyDecisionEngine,
    WorkloadProfile,
)


def test_benchmark_changes_decision():

    benchmark = BenchmarkEngine()

    postgres = benchmark.run(
        technology="PostgreSQL",
        benchmark_name="database",
        measurements={
            "latency": 10,
            "throughput": 900,
        },
        duration_ms=1000,
    )

    sqlite = benchmark.run(
        technology="SQLite",
        benchmark_name="database",
        measurements={
            "latency": 30,
            "throughput": 300,
        },
        duration_ms=1000,
    )

    comparison = benchmark.compare(
        "database",
        [postgres, sqlite],
    )

    engine = TechnologyDecisionEngine()

    decisions = engine.rank(
        options=[
            TechnologyOption(
                name="PostgreSQL",
                category="database",
                strengths=["high concurrency"],
            ),
            TechnologyOption(
                name="SQLite",
                category="database",
            ),
        ],
        workload=WorkloadProfile(
            concurrency=1.0,
        ),
    )

    integrator = BenchmarkDecisionIntegrator()

    updated = integrator.apply(
        decisions,
        comparison,
    )

    assert updated[0].technology == "PostgreSQL"
    assert updated[0].score > decisions[1].score