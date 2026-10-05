from core.benchmark.engine import BenchmarkEngine


def test_benchmark_run():

    engine = BenchmarkEngine()

    result = engine.run(
        technology="PostgreSQL",
        benchmark_name="database_read",
        measurements={
            "latency": 12,
            "throughput": 850,
            "memory": 180,
        },
        duration_ms=1200,
    )

    assert result.success is True
    assert result.technology == "PostgreSQL"
    assert len(result.metrics) == 3


def test_benchmark_comparison():

    engine = BenchmarkEngine()

    postgres = engine.run(
        technology="PostgreSQL",
        benchmark_name="database_read",
        measurements={
            "latency": 12,
            "throughput": 850,
        },
        duration_ms=1000,
    )

    sqlite = engine.run(
        technology="SQLite",
        benchmark_name="database_read",
        measurements={
            "latency": 30,
            "throughput": 300,
        },
        duration_ms=1000,
    )

    comparison = engine.compare(
        benchmark_name="database_read",
        results=[
            postgres,
            sqlite,
        ],
    )

    assert comparison.winner == "PostgreSQL"
    assert comparison.reasoning