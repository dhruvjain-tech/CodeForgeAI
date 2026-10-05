from core.repository.technology_advisor import TechnologyOption
from core.repository.technology_decision import (
    TechnologyDecisionEngine,
    WorkloadProfile,
)


def test_concurrency_decision():

    engine = TechnologyDecisionEngine()

    result = engine.evaluate(
        TechnologyOption(
            name="PostgreSQL",
            category="database",
            strengths=["high concurrency"],
        ),
        WorkloadProfile(
            concurrency=1.0,
        ),
    )

    assert result.technology == "PostgreSQL"
    assert result.score > 0
    assert result.confidence > 0


def test_requirement_matching():

    engine = TechnologyDecisionEngine()

    result = engine.evaluate(
        TechnologyOption(
            name="PostgreSQL",
            category="database",
            strengths=["postgresql", "high concurrency"],
        ),
        WorkloadProfile(),
        requirements=["postgresql"],
    )

    assert result.score >= 2
    assert result.confidence > 0


def test_rank_options():

    engine = TechnologyDecisionEngine()

    options = [
        TechnologyOption(
            name="SQLite",
            category="database",
            strengths=["simple local storage"],
        ),
        TechnologyOption(
            name="PostgreSQL",
            category="database",
            strengths=["high concurrency"],
        ),
    ]

    results = engine.rank(
        options=options,
        workload=WorkloadProfile(
            concurrency=1.0,
        ),
    )

    assert len(results) == 2
    assert results[0].technology == "PostgreSQL"


def test_tradeoff_detection():

    engine = TechnologyDecisionEngine()

    result = engine.evaluate(
        TechnologyOption(
            name="SQLite",
            category="database",
            strengths=["simple local storage"],
            weaknesses=["high concurrency"],
        ),
        WorkloadProfile(
            concurrency=1.0,
        ),
    )

    assert result.tradeoffs
    assert result.confidence >= 0.0


def test_decision_has_confidence():

    engine = TechnologyDecisionEngine()

    result = engine.evaluate(
        TechnologyOption(
            name="PostgreSQL",
            category="database",
            strengths=["high concurrency"],
        ),
        WorkloadProfile(
            concurrency=1.0,
        ),
    )

    assert 0.0 <= result.confidence <= 1.0