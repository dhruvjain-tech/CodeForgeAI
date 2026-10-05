from core.repository.context import RepositoryContext
from core.repository.service import RepositoryAnalysisService
from core.repository.technology_advisor import (
    TechnologyOption,
)
from core.repository.technology_integration import (
    RepositoryTechnologyAdvisor,
)


def test_full_repository_to_technology_flow(
    tmp_path,
):
    app_file = tmp_path / "app.py"

    app_file.write_text(
        "import os\n\n"
        "class Application:\n"
        "    def run(self):\n"
        "        return True\n\n"
        "def main():\n"
        "    return Application()\n",
        encoding="utf-8",
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
        workload="concurrency",
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

    assert len(context.files) == 1
    assert len(context.symbols) == 3
    assert len(context.locations) == 3


def test_repository_context_drives_requirements(
    tmp_path,
):
    app_file = tmp_path / "app.py"

    app_file.write_text(
        "def hello():\n"
        "    return 'hello'\n",
        encoding="utf-8",
    )

    analysis = RepositoryAnalysisService().analyze(
        tmp_path
    )

    context = RepositoryContext.from_analysis(
        analysis
    )

    advisor = RepositoryTechnologyAdvisor()

    requirements = advisor._derive_requirements(
        context
    )

    assert "python" in requirements
    assert "code structure" in requirements


def test_repository_technology_explanation(
    tmp_path,
):
    app_file = tmp_path / "app.py"

    app_file.write_text(
        "class Demo:\n"
        "    pass\n",
        encoding="utf-8",
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
        workload="local storage",
        options=[
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
        ],
    )

    explanation = advisor.advisor.explain(
        result
    )

    assert "Recommended technology:" in explanation
    assert result.recommendation in explanation