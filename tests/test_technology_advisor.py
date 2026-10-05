from core.repository.technology_advisor import (
    TechnologyAdvisor,
    TechnologyOption,
)
from core.repository.technology_decision import (
    WorkloadProfile,
)


def test_advisor_uses_decision_engine():

    advisor = TechnologyAdvisor()

    result = advisor.recommend(
        category="database",
        workload="high concurrency",
        options=[
            TechnologyOption(
                name="PostgreSQL",
                category="database",
                strengths=["high concurrency"],
            ),
            TechnologyOption(
                name="SQLite",
                category="database",
                strengths=["simple local storage"],
                weaknesses=["high concurrency"],
            ),
        ],
    )

    assert result.recommendation == "PostgreSQL"
    assert result.alternatives == ["SQLite"]
    assert result.reasoning


def test_explicit_workload_profile():

    advisor = TechnologyAdvisor()

    profile = WorkloadProfile(
        concurrency=0.95,
        latency_sensitive=0.8,
    )

    result = advisor.recommend(
        category="database",
        workload="database workload",
        options=[
            TechnologyOption(
                name="PostgreSQL",
                category="database",
                strengths=[
                    "high concurrency",
                    "low latency",
                ],
            ),
            TechnologyOption(
                name="SQLite",
                category="database",
                strengths=[
                    "simple local storage",
                ],
            ),
        ],
        workload_profile=profile,
    )

    assert result.recommendation == "PostgreSQL"


def test_compare_returns_decision_details():

    advisor = TechnologyAdvisor()

    results = advisor.compare(
        category="database",
        workload="high concurrency",
        options=[
            TechnologyOption(
                name="PostgreSQL",
                category="database",
                strengths=["high concurrency"],
            ),
            TechnologyOption(
                name="SQLite",
                category="database",
                weaknesses=["high concurrency"],
            ),
        ],
    )

    assert len(results) == 2

    assert "score" in results[0]
    assert "confidence" in results[0]
    assert "strengths" in results[0]
    assert "weaknesses" in results[0]
    assert "tradeoffs" in results[0]
    assert "reasoning" in results[0]