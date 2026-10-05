from statistics import mean

from .types import (
    BenchmarkComparison,
    BenchmarkMetric,
    BenchmarkResult,
)


class BenchmarkEngine:

    def run(
        self,
        technology: str,
        benchmark_name: str,
        measurements: dict[str, float],
        duration_ms: float,
        success: bool = True,
        error: str | None = None,
    ) -> BenchmarkResult:

        metrics = []

        for name, value in measurements.items():

            lower_is_better = name.lower() in {
                "latency",
                "latency_ms",
                "p95",
                "p99",
                "memory",
                "memory_mb",
                "cpu",
                "cpu_percent",
            }

            unit = self._infer_unit(name)

            metrics.append(
                BenchmarkMetric(
                    name=name,
                    value=float(value),
                    unit=unit,
                    lower_is_better=lower_is_better,
                )
            )

        return BenchmarkResult(
            technology=technology,
            benchmark_name=benchmark_name,
            success=success,
            duration_ms=duration_ms,
            metrics=metrics,
            error=error,
        )

    def compare(
        self,
        benchmark_name: str,
        results: list[BenchmarkResult],
    ) -> BenchmarkComparison:

        successful = [
            result
            for result in results
            if result.success
        ]

        if not successful:
            return BenchmarkComparison(
                benchmark_name=benchmark_name,
                results=results,
                reasoning=[
                    "No successful benchmark results."
                ],
            )

        metric_scores: dict[str, dict[str, float]] = {}

        for result in successful:

            for metric in result.metrics:

                metric_scores.setdefault(
                    metric.name,
                    {},
                )

                metric_scores[
                    metric.name
                ][result.technology] = metric.value

        scores: dict[str, list[float]] = {
            result.technology: []
            for result in successful
        }

        reasoning = []

        for metric_name, values in metric_scores.items():

            if len(values) < 2:
                continue

            metric_objects = [
                metric
                for result in successful
                for metric in result.metrics
                if metric.name == metric_name
            ]

            lower_is_better = (
                metric_objects[0].lower_is_better
            )

            best_value = (
                min(values.values())
                if lower_is_better
                else max(values.values())
            )

            winner = next(
                technology
                for technology, value in values.items()
                if value == best_value
            )

            scores[winner].append(1.0)

            reasoning.append(
                f"{winner} performed best for "
                f"{metric_name}."
            )

        ranked = sorted(
            scores.items(),
            key=lambda item: mean(item[1])
            if item[1]
            else 0.0,
            reverse=True,
        )

        winner = (
            ranked[0][0]
            if ranked
            else None
        )

        if winner:
            reasoning.insert(
                0,
                f"Benchmark winner: {winner}.",
            )

        return BenchmarkComparison(
            benchmark_name=benchmark_name,
            results=results,
            winner=winner,
            reasoning=reasoning,
        )

    def _infer_unit(
        self,
        metric_name: str,
    ) -> str:

        name = metric_name.lower()

        if "latency" in name:
            return "ms"

        if "memory" in name:
            return "MB"

        if "cpu" in name:
            return "%"

        if "throughput" in name:
            return "ops/s"

        if "p95" in name or "p99" in name:
            return "ms"

        return "value"


benchmark_engine = BenchmarkEngine()