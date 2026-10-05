from .types import BenchmarkComparison
from core.repository.technology_decision import (
    TechnologyDecision,
    TechnologyDecisionEngine,
)


class BenchmarkDecisionIntegrator:

    def build_scores(
        self,
        comparison: BenchmarkComparison,
    ) -> dict[str, float]:

        if not comparison.results:
            return {}

        scores = {}

        for result in comparison.results:

            if not result.success:
                scores[result.technology] = -5.0
                continue

            score = 0.0

            for metric in result.metrics:

                value = metric.value

                if value <= 0:
                    continue

                if metric.lower_is_better:
                    score += 1.0 / value
                else:
                    score += value

            scores[result.technology] = score

        if not scores:
            return {}

        maximum = max(scores.values())

        if maximum <= 0:
            return scores

        return {
            technology: round(
                (score / maximum) * 5.0,
                2,
            )
            for technology, score in scores.items()
        }

    def apply(
        self,
        decisions: list[TechnologyDecision],
        comparison: BenchmarkComparison,
    ) -> list[TechnologyDecision]:

        engine = TechnologyDecisionEngine()

        scores = self.build_scores(
            comparison
        )

        return engine.apply_benchmark_adjustment(
            decisions,
            scores,
        )


benchmark_decision_integrator = (
    BenchmarkDecisionIntegrator()
)