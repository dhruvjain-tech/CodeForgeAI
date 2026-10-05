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

from models.repository_analysis import (
    RepositoryAnalysis,
    RepositoryAnalysisDependency,
)


def test_dependency_graph(client, db_session, repository):
    analysis = RepositoryAnalysis(
        repository_id=repository.id,
        root_path="D:/sample-repo",
        file_count=2,
        symbol_count=0,
        dependency_count=2,
    )

    db_session.add(analysis)
    db_session.commit()
    db_session.refresh(analysis)

    db_session.add_all(
        [
            RepositoryAnalysisDependency(
                analysis_id=analysis.id,
                source_file="main.py",
                target="os",
                dependency_type="import",
            ),
            RepositoryAnalysisDependency(
                analysis_id=analysis.id,
                source_file="main.py",
                target="utils.py",
                dependency_type="import",
            ),
        ]
    )

    db_session.commit()

    response = client.get(
        f"/api/v1/repository-search/analyses/"
        f"{analysis.id}/dependency-graph"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["analysis_id"] == analysis.id
    assert data["node_count"] == 1
    assert data["edge_count"] == 2
    assert len(data["edges"]) == 2