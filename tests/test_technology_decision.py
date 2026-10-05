from core.repository.technology_advisor import (
    TechnologyOption,
)
from core.repository.technology_decision import (
    TechnologyDecisionEngine,
    WorkloadProfile,
)


def test_concurrency_decision():
    engine = TechnologyDecisionEngine()

    option = TechnologyOption(
        name="PostgreSQL",
        category="database",
        strengths=[
            "high concurrency",
        ],
    )

    decision = engine.evaluate(
        option,
        WorkloadProfile(
            concurrency=0.9,
        ),
    )

    assert decision.score > 0
    assert decision.technology == "PostgreSQL"


def test_requirement_matching():
    engine = TechnologyDecisionEngine()

    option = TechnologyOption(
        name="Redis",
        category="cache",
        strengths=[
            "fast caching",
            "low latency",
        ],
    )

    decision = engine.evaluate(
        option,
        WorkloadProfile(
            latency_sensitive=0.9,
        ),
        requirements=[
            "fast",
        ],
    )

    assert decision.score > 0
    assert decision.reasoning


def test_rank_options():
    engine = TechnologyDecisionEngine()

    options = [
        TechnologyOption(
            name="SQLite",
            category="database",
            strengths=[
                "simple local storage",
            ],
        ),
        TechnologyOption(
            name="PostgreSQL",
            category="database",
            strengths=[
                "high concurrency",
            ],
        ),
    ]

    results = engine.rank(
        options,
        WorkloadProfile(
            concurrency=0.9,
        ),
    )

    assert len(results) == 2
    assert results[0].technology == "PostgreSQL"


def test_tradeoff_detection():
    engine = TechnologyDecisionEngine()

    option = TechnologyOption(
        name="SQLite",
        category="database",
        weaknesses=[
            "high concurrency",
        ],
    )

    decision = engine.evaluate(
        option,
        WorkloadProfile(
            concurrency=0.9,
        ),
        requirements=[
            "high concurrency",
        ],
    )

    assert decision.score < 0
    assert decision.tradeoffs