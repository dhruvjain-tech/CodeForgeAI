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

from models import Project, Repository


def create_repository(db_session):
    project = Project(
        name="API Test Project",
        description="Repository intelligence API test",
        repository_url="https://example.com/test",
    )

    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    repository = Repository(
        project_id=project.id,
        name="API Test Repository",
        repository_url="https://example.com/repository",
        default_branch="main",
        local_path="D:/sample-repo",
        status="active",
    )

    db_session.add(repository)
    db_session.commit()
    db_session.refresh(repository)

    return repository


def test_analyze_and_save_repository(
    client,
    db_session,
    tmp_path,
):
    repository = create_repository(db_session)

    source_file = tmp_path / "main.py"

    source_file.write_text(
        "def hello():\n"
        "    return 'hello'\n",
        encoding="utf-8",
    )

    response = client.post(
        "/api/v1/repository-intelligence/analyze-and-save",
        json={
            "repository_id": repository.id,
            "root_path": str(tmp_path),
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "saved"
    assert data["repository_id"] == repository.id
    assert data["analysis_id"] is not None
    assert data["file_count"] >= 1
    assert data["symbol_count"] >= 1


def test_get_analysis(
    client,
    db_session,
    tmp_path,
):
    repository = create_repository(db_session)

    source_file = tmp_path / "main.py"

    source_file.write_text(
        "def hello():\n"
        "    return 'hello'\n",
        encoding="utf-8",
    )

    save_response = client.post(
        "/api/v1/repository-intelligence/analyze-and-save",
        json={
            "repository_id": repository.id,
            "root_path": str(tmp_path),
        },
    )

    assert save_response.status_code == 200

    analysis_id = save_response.json()["analysis_id"]

    response = client.get(
        f"/api/v1/repository-intelligence/analyses/{analysis_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == analysis_id
    assert data["repository_id"] == repository.id
    assert data["file_count"] >= 1
    assert data["symbol_count"] >= 1
    assert len(data["files"]) >= 1
    assert len(data["symbols"]) >= 1


def test_get_analysis_not_found(client):
    response = client.get(
        "/api/v1/repository-intelligence/analyses/999999"
    )

    assert response.status_code == 404


def test_analyze_and_save_repository_not_found(
    client,
    tmp_path,
):
    response = client.post(
        "/api/v1/repository-intelligence/analyze-and-save",
        json={
            "repository_id": 999999,
            "root_path": str(tmp_path),
        },
    )

    assert response.status_code == 404


def test_list_repository_analyses(
    client,
    db_session,
    tmp_path,
):
    repository = create_repository(db_session)

    source_file = tmp_path / "main.py"

    source_file.write_text(
        "def hello():\n"
        "    return 'hello'\n",
        encoding="utf-8",
    )

    first_response = client.post(
        "/api/v1/repository-intelligence/analyze-and-save",
        json={
            "repository_id": repository.id,
            "root_path": str(tmp_path),
        },
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/api/v1/repository-intelligence/analyze-and-save",
        json={
            "repository_id": repository.id,
            "root_path": str(tmp_path),
        },
    )

    assert second_response.status_code == 200

    response = client.get(
        f"/api/v1/repository-intelligence/repositories/"
        f"{repository.id}/analyses"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["repository_id"] == repository.id
    assert data[1]["repository_id"] == repository.id
    assert data[0]["file_count"] >= 1
    assert data[0]["symbol_count"] >= 1


def test_get_latest_analysis(
    client,
    db_session,
    tmp_path,
):
    repository = create_repository(db_session)

    source_file = tmp_path / "main.py"

    source_file.write_text(
        "def hello():\n"
        "    return 'hello'\n",
        encoding="utf-8",
    )

    first_response = client.post(
        "/api/v1/repository-intelligence/analyze-and-save",
        json={
            "repository_id": repository.id,
            "root_path": str(tmp_path),
        },
    )

    assert first_response.status_code == 200

    first_analysis_id = first_response.json()["analysis_id"]

    second_response = client.post(
        "/api/v1/repository-intelligence/analyze-and-save",
        json={
            "repository_id": repository.id,
            "root_path": str(tmp_path),
        },
    )

    assert second_response.status_code == 200

    second_analysis_id = second_response.json()["analysis_id"]

    response = client.get(
        f"/api/v1/repository-intelligence/repositories/"
        f"{repository.id}/analyses/latest"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["repository_id"] == repository.id
    assert data["id"] == second_analysis_id
    assert data["id"] != first_analysis_id
    assert data["file_count"] >= 1
    assert data["symbol_count"] >= 1