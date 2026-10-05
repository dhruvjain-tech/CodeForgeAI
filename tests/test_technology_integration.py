from core.repository.context import RepositoryContext
from core.repository.technology_advisor import (
    TechnologyOption,
)
from core.repository.technology_integration import (
    RepositoryTechnologyAdvisor,
)
from core.repository.technology_decision import (
    WorkloadProfile,
)
from core.repository.types import (
    RepositoryDependency,
    RepositoryFile,
    RepositorySymbol,
)


def test_repository_technology_recommendation():
    context = RepositoryContext(
        root_path="D:/test-repo",
        files=[
            RepositoryFile(
                path="D:/test-repo/app.py",
                relative_path="app.py",
                extension=".py",
                size_bytes=100,
                language="Python",
            )
        ],
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
            ),
        ],
    )

    assert result.recommendation == "PostgreSQL"


def test_repository_requirements_from_languages():
    context = RepositoryContext(
        root_path="D:/test-repo",
        files=[
            RepositoryFile(
                path="D:/test-repo/app.py",
                relative_path="app.py",
                extension=".py",
                size_bytes=100,
                language="Python",
            ),
            RepositoryFile(
                path="D:/test-repo/app.ts",
                relative_path="app.ts",
                extension=".ts",
                size_bytes=100,
                language="TypeScript",
            ),
        ],
    )

    advisor = RepositoryTechnologyAdvisor()

    requirements = advisor._derive_requirements(
        context
    )

    assert "python" in requirements
    assert "typescript" in requirements


def test_repository_requirements_from_dependencies():
    context = RepositoryContext(
        root_path="D:/test-repo",
        dependencies=[
            RepositoryDependency(
                source_file="app.py",
                target="postgresql",
                dependency_type="import",
            ),
            RepositoryDependency(
                source_file="cache.py",
                target="redis",
                dependency_type="import",
            ),
        ],
    )

    advisor = RepositoryTechnologyAdvisor()

    requirements = advisor._derive_requirements(
        context
    )

    assert "postgresql" in requirements
    assert "redis" in requirements
    assert "dependency management" in requirements


def test_repository_requirements_from_symbols():
    context = RepositoryContext(
        root_path="D:/test-repo",
        symbols=[
            RepositorySymbol(
                name="UserService",
                symbol_type="class",
                file_path="app.py",
                line_start=1,
                line_end=10,
            )
        ],
    )

    advisor = RepositoryTechnologyAdvisor()

    requirements = advisor._derive_requirements(
        context
    )

    assert "code structure" in requirements


def test_repository_workload_profile():
    context = RepositoryContext(
        root_path="D:/test-repo",
        files=[
            RepositoryFile(
                path="D:/test-repo/app.py",
                relative_path="app.py",
                extension=".py",
                size_bytes=100,
                language="Python",
            )
        ],
    )

    advisor = RepositoryTechnologyAdvisor()

    profile = advisor._derive_workload_profile(
        context,
        "high concurrency database workload",
    )

    assert isinstance(
        profile,
        WorkloadProfile,
    )

    assert profile.concurrency == 1.0
    assert profile.io_intensive == 1.0