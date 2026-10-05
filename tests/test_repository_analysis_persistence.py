import os
import sys
from pathlib import Path

os.environ.setdefault(
    "DATABASE_URL",
    "sqlite:///./test.db",
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
API_ROOT = PROJECT_ROOT / "apps" / "api"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))


from core.repository.types import (
    RepositoryAnalysis,
    RepositoryDependency,
    RepositoryFile,
    RepositorySymbol,
)
from models.repository_analysis import (
    RepositoryAnalysis as RepositoryAnalysisModel,
)
from services.repository_analysis_service import save_repository_analysis


def test_save_repository_analysis(db_session, repository):
    result = RepositoryAnalysis(
        root_path="D:/sample-repo",
        files=[
            RepositoryFile(
                path="D:/sample-repo/main.py",
                relative_path="main.py",
                extension=".py",
                size_bytes=120,
                language="Python",
            )
        ],
        symbols=[
            RepositorySymbol(
                name="hello",
                symbol_type="function",
                file_path="D:/sample-repo/main.py",
                line_start=1,
                line_end=3,
            )
        ],
        dependencies=[
            RepositoryDependency(
                source_file="D:/sample-repo/main.py",
                target="os",
                dependency_type="import",
            )
        ],
    )

    analysis = save_repository_analysis(
        db_session,
        repository.id,
        result,
    )

    assert analysis.id is not None
    assert analysis.repository_id == repository.id
    assert analysis.file_count == 1
    assert analysis.symbol_count == 1
    assert analysis.dependency_count == 1

    assert len(analysis.files) == 1
    assert analysis.files[0].language == "Python"

    assert len(analysis.symbols) == 1
    assert analysis.symbols[0].name == "hello"

    assert len(analysis.dependencies) == 1
    assert analysis.dependencies[0].target == "os"


def test_repository_analysis_relationships(db_session, repository):
    result = RepositoryAnalysis(
        root_path="D:/sample-repo",
        files=[
            RepositoryFile(
                path="D:/sample-repo/app.py",
                relative_path="app.py",
                extension=".py",
                size_bytes=50,
                language="Python",
            ),
        ],
    )

    analysis = save_repository_analysis(
        db_session,
        repository.id,
        result,
    )

    stored = db_session.get(
        RepositoryAnalysisModel,
        analysis.id,
    )

    assert stored is not None
    assert stored.repository_id == repository.id
    assert len(stored.files) == 1