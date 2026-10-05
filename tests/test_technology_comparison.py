from core.repository.technology_advisor import (
    TechnologyAdvisor,
    TechnologyOption,
)


def test_compare_returns_ranked_options():
    advisor = TechnologyAdvisor()

    options = [
        TechnologyOption(
            name="PostgreSQL",
            category="database",
            strengths=[
                "high concurrency",
                "relational queries",
            ],
        ),
        TechnologyOption(
            name="SQLite",
            category="database",
            strengths=[
                "simple local storage",
            ],
        ),
        TechnologyOption(
            name="Redis",
            category="database",
            strengths=[
                "fast caching",
            ],
        ),
    ]

    results = advisor.compare(
        category="database",
        workload="concurrency",
        requirements=[
            "relational queries",
        ],
        options=options,
    )

    assert len(results) == 3
    assert results[0]["technology"] == "PostgreSQL"
    assert results[0]["score"] >= results[1]["score"]


def test_compare_includes_strengths_and_weaknesses():
    advisor = TechnologyAdvisor()

    options = [
        TechnologyOption(
            name="MongoDB",
            category="database",
            strengths=["flexible documents"],
            weaknesses=["relational queries"],
        ),
    ]

    results = advisor.compare(
        category="database",
        workload="documents",
        requirements=["flexible"],
        options=options,
    )

    assert len(results) == 1
    assert results[0]["strengths"] == [
        "flexible documents"
    ]
    assert results[0]["weaknesses"] == [
        "relational queries"
    ]


def test_compare_empty_options():
    advisor = TechnologyAdvisor()

    results = advisor.compare(
        category="database",
        workload="concurrency",
        options=[],
    )

    assert results == []