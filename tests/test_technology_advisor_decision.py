from core.repository.technology_advisor import (
    TechnologyAdvisor,
    TechnologyOption,
)
from core.repository.technology_decision import (
    WorkloadProfile,
)


def test_advisor_uses_decision_engine():
    advisor = TechnologyAdvisor()

    options = [
        TechnologyOption(
            name="PostgreSQL",
            category="database",
            strengths=[
                "high concurrency",
            ],
        ),
        TechnologyOption(
            name="SQLite",
            category="database",
            strengths=[
                "simple local storage",
            ],
        ),
    ]

    result = advisor.recommend(
        category="database",
        workload="high concurrency",
        options=options,
    )

    assert result.recommendation == "PostgreSQL"
    assert "Decision score:" in " ".join(
        result.reasoning
    )


def test_explicit_workload_profile():
    advisor = TechnologyAdvisor()

    options = [
        TechnologyOption(
            name="Redis",
            category="cache",
            strengths=[
                "low latency",
            ],
        ),
        TechnologyOption(
            name="SQLite",
            category="database",
            strengths=[
                "simple storage",
            ],
        ),
    ]

    result = advisor.recommend(
        category="cache",
        workload="custom workload",
        workload_profile=WorkloadProfile(
            latency_sensitive=0.9,
        ),
        options=options,
    )

    assert result.recommendation == "Redis"


def test_compare_returns_decision_details():
    advisor = TechnologyAdvisor()

    options = [
        TechnologyOption(
            name="PostgreSQL",
            category="database",
            strengths=[
                "high concurrency",
            ],
        ),
        TechnologyOption(
            name="SQLite",
            category="database",
        ),
    ]

    results = advisor.compare(
        category="database",
        workload="concurrency",
        options=options,
    )

    assert len(results) == 2
    assert results[0]["technology"] == "PostgreSQL"
    assert "tradeoffs" in results[0]
    assert "reasoning" in results[0]