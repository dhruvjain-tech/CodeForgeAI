from dataclasses import dataclass, field

from .technology_decision import (
    TechnologyDecisionEngine,
    WorkloadProfile,
)
from .technology_types import TechnologyOption


@dataclass
class TechnologyRecommendation:
    category: str
    recommendation: str
    alternatives: list[str] = field(default_factory=list)
    reasoning: list[str] = field(default_factory=list)


class TechnologyAdvisor:

    def __init__(self):
        self.decision_engine = TechnologyDecisionEngine()

    def recommend(
        self,
        category: str,
        workload: str,
        requirements: list[str] | None = None,
        options: list[TechnologyOption] | None = None,
        workload_profile: WorkloadProfile | None = None,
    ) -> TechnologyRecommendation:

        requirements = requirements or []
        options = options or []

        if not options:
            return TechnologyRecommendation(
                category=category,
                recommendation="Insufficient technology options",
                reasoning=[
                    "No technology options were provided."
                ],
            )

        if workload_profile is None:
            workload_profile = self._infer_workload(
                workload
            )

        decisions = self.decision_engine.rank(
            options=options,
            workload=workload_profile,
            requirements=requirements,
        )

        if not decisions:
            return TechnologyRecommendation(
                category=category,
                recommendation="No suitable technology found",
                reasoning=[
                    "The decision engine returned no results."
                ],
            )

        best = decisions[0]

        reasoning = [
            f"Workload: {workload}",
            f"Decision score: {best.score}",
            f"Decision confidence: {best.confidence}",
        ]

        reasoning.extend(best.reasoning)

        if best.tradeoffs:
            reasoning.append(
                "Trade-offs: "
                + "; ".join(best.tradeoffs)
            )

        return TechnologyRecommendation(
            category=category,
            recommendation=best.technology,
            alternatives=[
                decision.technology
                for decision in decisions[1:]
            ],
            reasoning=reasoning,
        )

    def compare(
        self,
        category: str,
        workload: str,
        requirements: list[str] | None = None,
        options: list[TechnologyOption] | None = None,
        workload_profile: WorkloadProfile | None = None,
    ) -> list[dict]:

        requirements = requirements or []
        options = options or []

        if not options:
            return []

        if workload_profile is None:
            workload_profile = self._infer_workload(
                workload
            )

        decisions = self.decision_engine.rank(
            options=options,
            workload=workload_profile,
            requirements=requirements,
        )

        return [
            {
                "technology": decision.technology,
                "category": category,
                "score": decision.score,
                "confidence": decision.confidence,
                "strengths": decision.strengths,
                "weaknesses": decision.weaknesses,
                "tradeoffs": decision.tradeoffs,
                "reasoning": decision.reasoning,
            }
            for decision in decisions
        ]

    def explain(
        self,
        recommendation: TechnologyRecommendation,
    ) -> str:

        lines = [
            (
                "Recommended technology: "
                f"{recommendation.recommendation}"
            ),
            f"Category: {recommendation.category}",
        ]

        if recommendation.alternatives:
            lines.append(
                "Alternatives: "
                + ", ".join(
                    recommendation.alternatives
                )
            )

        if recommendation.reasoning:
            lines.append("Reasoning:")

            for reason in recommendation.reasoning:
                lines.append(
                    f"- {reason}"
                )

        return "\n".join(lines)

    def decision_profile(
        self,
        workload: str,
        requirements: list[str] | None = None,
        workload_profile: WorkloadProfile | None = None,
    ) -> WorkloadProfile:

        if workload_profile is not None:
            return workload_profile

        return self._infer_workload(
            workload
        )

    def _infer_workload(
        self,
        workload: str,
    ) -> WorkloadProfile:

        text = workload.lower()

        return WorkloadProfile(
            cpu_intensive=(
                1.0
                if any(
                    keyword in text
                    for keyword in [
                        "cpu",
                        "compute",
                        "computation",
                    ]
                )
                else 0.0
            ),
            memory_intensive=(
                1.0
                if any(
                    keyword in text
                    for keyword in [
                        "memory",
                        "ram",
                        "in-memory",
                    ]
                )
                else 0.0
            ),
            io_intensive=(
                1.0
                if any(
                    keyword in text
                    for keyword in [
                        "io",
                        "disk",
                        "storage",
                        "database",
                    ]
                )
                else 0.0
            ),
            concurrency=(
                1.0
                if any(
                    keyword in text
                    for keyword in [
                        "concurrency",
                        "concurrent",
                        "parallel",
                        "high traffic",
                    ]
                )
                else 0.0
            ),
            latency_sensitive=(
                1.0
                if any(
                    keyword in text
                    for keyword in [
                        "latency",
                        "low latency",
                        "real time",
                        "realtime",
                        "fast",
                    ]
                )
                else 0.0
            ),
        )


technology_advisor = TechnologyAdvisor()