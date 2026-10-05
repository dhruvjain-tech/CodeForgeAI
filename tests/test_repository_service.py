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

from models.repository_analysis import RepositoryAnalysis
from services.repository_analysis_service import (
    get_latest_repository_analysis,
    get_repository_analyses,
)


def test_get_repository_analyses(db_session, repository):
    analyses = get_repository_analyses(
        db_session,
        repository.id,
    )

    assert analyses == []


def test_get_latest_repository_analysis(db_session, repository):
    analysis = get_latest_repository_analysis(
        db_session,
        repository.id,
    )

    assert analysis is None