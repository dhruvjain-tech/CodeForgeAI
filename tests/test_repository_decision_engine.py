from core.repository.context import RepositoryContext
from core.repository.technology_advisor import TechnologyOption
from core.repository.technology_integration import (
    RepositoryTechnologyAdvisor,
)
from core.repository.types import RepositoryFile


def test_repository_decision_engine_flow(
    tmp_path,
):
    app_file = tmp_path / "app.py"

    app_file.write_text(
        "class UserService:\n"
        "    def get_users(self):\n"
        "        return []\n",
        encoding="utf-8",
    )

    from core.repository.service import (
        RepositoryAnalysisService,
    )

    analysis = RepositoryAnalysisService().analyze(
        tmp_path
    )

    context = RepositoryContext.from_analysis(
        analysis
    )

    advisor = RepositoryTechnologyAdvisor()

    result = advisor.recommend(
        context=context,
        category="database",
        workload="high concurrency database",
        options=[
            TechnologyOption(
                name="PostgreSQL",
                category="database",
                strengths=[
                    "high concurrency",
                    "python",
                ],
            ),
            TechnologyOption(
                name="SQLite",
                category="database",
                strengths=[
                    "simple local storage",
                ],
                weaknesses=[
                    "high concurrency",
                ],
            ),
        ],
    )

    assert result.recommendation == "PostgreSQL"
    assert result.alternatives == ["SQLite"]
    assert result.reasoning

    reasoning_text = " ".join(
        result.reasoning
    )

    assert "Decision score:" in reasoning_text


def test_repository_decision_contains_tradeoffs(
    tmp_path,
):
    app_file = tmp_path / "app.py"

    app_file.write_text(
        "def main():\n"
        "    return True\n",
        encoding="utf-8",
    )

    from core.repository.service import (
        RepositoryAnalysisService,
    )

    analysis = RepositoryAnalysisService().analyze(
        tmp_path
    )

    context = RepositoryContext.from_analysis(
        analysis
    )

    advisor = RepositoryTechnologyAdvisor()

    result = advisor.recommend(
        context=context,
        category="database",
        workload="high concurrency",
        options=[
            TechnologyOption(
                name="SQLite",
                category="database",
                strengths=[
                    "simple local storage",
                ],
                weaknesses=[
                    "high concurrency",
                ],
            ),
            TechnologyOption(
                name="PostgreSQL",
                category="database",
                strengths=[
                    "high concurrency",
                ],
            ),
        ],
    )

    assert result.recommendation == "PostgreSQL"
    assert result.reasoning