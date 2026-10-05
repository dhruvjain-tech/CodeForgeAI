from core.repository.technology_advisor import (
    TechnologyAdvisor,
    TechnologyRecommendation,
)


def test_explain_recommendation():
    advisor = TechnologyAdvisor()

    recommendation = TechnologyRecommendation(
        category="database",
        recommendation="PostgreSQL",
        alternatives=[
            "SQLite",
            "MongoDB",
        ],
        reasoning=[
            "Workload: high concurrency",
            "Score: 7",
            "Matched strengths: high concurrency",
        ],
    )

    explanation = advisor.explain(
        recommendation
    )

    assert "PostgreSQL" in explanation
    assert "database" in explanation
    assert "SQLite" in explanation
    assert "MongoDB" in explanation
    assert "high concurrency" in explanation


def test_explain_without_alternatives():
    advisor = TechnologyAdvisor()

    recommendation = TechnologyRecommendation(
        category="cache",
        recommendation="Redis",
        reasoning=[
            "Workload: caching",
            "Score: 5",
        ],
    )

    explanation = advisor.explain(
        recommendation
    )

    assert "Redis" in explanation
    assert "cache" in explanation
    assert "Alternatives:" not in explanation


def test_explain_without_reasoning():
    advisor = TechnologyAdvisor()

    recommendation = TechnologyRecommendation(
        category="database",
        recommendation="PostgreSQL",
    )

    explanation = advisor.explain(
        recommendation
    )

    assert "PostgreSQL" in explanation
    assert "database" in explanation