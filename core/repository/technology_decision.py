from dataclasses import dataclass, field

from .technology_types import TechnologyOption


@dataclass
class WorkloadProfile:
    cpu_intensive: float = 0.0
    memory_intensive: float = 0.0
    io_intensive: float = 0.0
    concurrency: float = 0.0
    latency_sensitive: float = 0.0


@dataclass
class TechnologyDecision:
    technology: str
    score: float
    confidence: float
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    tradeoffs: list[str] = field(default_factory=list)
    reasoning: list[str] = field(default_factory=list)


class TechnologyDecisionEngine:

    def evaluate(
        self,
        option: TechnologyOption,
        workload: WorkloadProfile,
        requirements: list[str] | None = None,
    ) -> TechnologyDecision:

        requirements = requirements or []

        score = 0.0
        reasoning = []
        tradeoffs = []

        strengths = [
            value.lower()
            for value in option.strengths
        ]

        weaknesses = [
            value.lower()
            for value in option.weaknesses
        ]

        for intensity, keywords, points, label in [
            (
                workload.concurrency,
                ("concurrency", "parallel", "scaling"),
                3.0,
                "concurrency",
            ),
            (
                workload.latency_sensitive,
                ("latency", "fast", "low latency"),
                3.0,
                "latency",
            ),
            (
                workload.memory_intensive,
                ("memory", "in-memory", "ram"),
                2.0,
                "memory",
            ),
            (
                workload.io_intensive,
                ("io", "storage", "disk", "database"),
                2.0,
                "io",
            ),
            (
                workload.cpu_intensive,
                ("cpu", "compute", "computation"),
                2.0,
                "cpu",
            ),
        ]:

            if intensity <= 0.7:
                continue

            matched = any(
                keyword in strength
                for keyword in keywords
                for strength in strengths
            )

            if matched:
                score += points
                reasoning.append(
                    f"{option.name} matches the "
                    f"{label}-intensive workload."
                )
            else:
                tradeoffs.append(
                    f"{option.name} does not explicitly provide "
                    f"a strong {label}-workload advantage."
                )

        for requirement in requirements:

            requirement = requirement.lower()

            if any(
                requirement in strength
                for strength in strengths
            ):
                score += 2.0

                reasoning.append(
                    f"{option.name} satisfies requirement: "
                    f"{requirement}."
                )

            if any(
                requirement in weakness
                for weakness in weaknesses
            ):
                score -= 2.0

                tradeoffs.append(
                    f"{option.name} has a weakness related to "
                    f"requirement: {requirement}."
                )

        for conflict in self._detect_workload_conflicts(
            option,
            workload,
        ):
            score -= conflict["penalty"]
            tradeoffs.append(
                conflict["message"]
            )

        for weakness in option.weaknesses:
            tradeoffs.append(
                f"Trade-off: {option.name} has weakness "
                f"'{weakness}'."
            )

        if not reasoning:
            reasoning.append(
                f"No strong workload or requirement match "
                f"was detected for {option.name}."
            )

        confidence = self._calculate_confidence(
            score,
            reasoning,
            tradeoffs,
        )

        return TechnologyDecision(
            technology=option.name,
            score=score,
            confidence=confidence,
            strengths=list(option.strengths),
            weaknesses=list(option.weaknesses),
            tradeoffs=tradeoffs,
            reasoning=reasoning,
        )

    def rank(
        self,
        options: list[TechnologyOption],
        workload: WorkloadProfile,
        requirements: list[str] | None = None,
    ) -> list[TechnologyDecision]:

        decisions = [
            self.evaluate(
                option,
                workload,
                requirements,
            )
            for option in options
        ]

        decisions.sort(
            key=lambda item: (
                item.score,
                item.confidence,
                item.technology,
            ),
            reverse=True,
        )

        return decisions

    def apply_benchmark_adjustment(
        self,
        decisions: list[TechnologyDecision],
        benchmark_scores: dict[str, float],
    ) -> list[TechnologyDecision]:

        for decision in decisions:

            benchmark_score = benchmark_scores.get(
                decision.technology
            )

            if benchmark_score is None:
                continue

            decision.score += benchmark_score

            decision.reasoning.append(
                "Benchmark performance contributed "
                f"{benchmark_score:.2f} points."
            )

            decision.confidence = min(
                1.0,
                round(
                    decision.confidence
                    + min(
                        0.20,
                        abs(benchmark_score) / 50,
                    ),
                    2,
                ),
            )

        decisions.sort(
            key=lambda item: (
                item.score,
                item.confidence,
                item.technology,
            ),
            reverse=True,
        )

        return decisions

    def _detect_workload_conflicts(
        self,
        option: TechnologyOption,
        workload: WorkloadProfile,
    ) -> list[dict]:

        weaknesses = [
            value.lower()
            for value in option.weaknesses
        ]

        conflicts = []

        checks = [
            (
                workload.concurrency,
                ("concurrency", "parallel", "scaling"),
                "high concurrency",
            ),
            (
                workload.latency_sensitive,
                ("latency", "slow"),
                "latency-sensitive",
            ),
            (
                workload.memory_intensive,
                ("memory", "ram"),
                "memory-intensive",
            ),
            (
                workload.io_intensive,
                ("io", "storage", "disk"),
                "I/O-intensive",
            ),
            (
                workload.cpu_intensive,
                ("cpu", "compute"),
                "CPU-intensive",
            ),
        ]

        for intensity, keywords, label in checks:

            if intensity <= 0.7:
                continue

            if any(
                keyword in weakness
                for keyword in keywords
                for weakness in weaknesses
            ):
                conflicts.append(
                    {
                        "penalty": 3.0,
                        "message": (
                            f"{option.name} has a weakness that "
                            f"conflicts with the {label} workload."
                        ),
                    }
                )

        return conflicts

    def _calculate_confidence(
        self,
        score: float,
        reasoning: list[str],
        tradeoffs: list[str],
    ) -> float:

        confidence = 0.5

        if score >= 6:
            confidence += 0.25
        elif score >= 3:
            confidence += 0.15
        elif score < 0:
            confidence -= 0.20

        if reasoning:
            confidence += 0.10

        if tradeoffs:
            confidence -= min(
                0.20,
                len(tradeoffs) * 0.05,
            )

        return round(
            max(
                0.0,
                min(1.0, confidence),
            ),
            2,
        )


technology_decision_engine = TechnologyDecisionEngine()