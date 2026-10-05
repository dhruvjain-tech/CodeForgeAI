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
        name="Search Test Project",
        description="Repository search API test",
        repository_url="https://example.com/search-test",
    )

    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    repository = Repository(
        project_id=project.id,
        name="Search Test Repository",
        repository_url="https://example.com/search-repository",
        default_branch="main",
        local_path="D:/search-test-repo",
        status="active",
    )

    db_session.add(repository)
    db_session.commit()
    db_session.refresh(repository)

    return repository


def create_analysis(
    client,
    repository,
    tmp_path,
):
    source_file = tmp_path / "main.py"

    source_file.write_text(
        "import os\n"
        "import json\n"
        "\n"
        "def hello_world():\n"
        "    return 'hello'\n"
        "\n"
        "def calculate_total():\n"
        "    return 100\n",
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

    return response.json()["analysis_id"]


def test_search_files(
    client,
    db_session,
    tmp_path,
):
    repository = create_repository(db_session)

    create_analysis(
        client,
        repository,
        tmp_path,
    )

    response = client.get(
        "/api/v1/repository-search/files",
        params={
            "repository_id": repository.id,
            "query": "main",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[0]["relative_path"] == "main.py"
    assert data[0]["language"] == "Python"


def test_search_symbols(
    client,
    db_session,
    tmp_path,
):
    repository = create_repository(db_session)

    create_analysis(
        client,
        repository,
        tmp_path,
    )

    response = client.get(
        "/api/v1/repository-search/symbols",
        params={
            "repository_id": repository.id,
            "query": "hello",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[0]["name"] == "hello_world"
    assert data[0]["symbol_type"] == "function"


def test_search_dependencies(
    client,
    db_session,
    tmp_path,
):
    repository = create_repository(db_session)

    create_analysis(
        client,
        repository,
        tmp_path,
    )

    response = client.get(
        "/api/v1/repository-search/dependencies",
        params={
            "repository_id": repository.id,
            "query": "os",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[0]["target"] == "os"
    assert data[0]["dependency_type"] == "import"


def test_search_multiple_symbols(
    client,
    db_session,
    tmp_path,
):
    repository = create_repository(db_session)

    create_analysis(
        client,
        repository,
        tmp_path,
    )

    response = client.get(
        "/api/v1/repository-search/symbols",
        params={
            "repository_id": repository.id,
            "query": "calculate",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "calculate_total"


def test_search_no_results(
    client,
    db_session,
    tmp_path,
):
    repository = create_repository(db_session)

    create_analysis(
        client,
        repository,
        tmp_path,
    )

    response = client.get(
        "/api/v1/repository-search/symbols",
        params={
            "repository_id": repository.id,
            "query": "does_not_exist",
        },
    )

    assert response.status_code == 200
    assert response.json() == []


def test_search_repository_not_found(client):
    response = client.get(
        "/api/v1/repository-search/files",
        params={
            "repository_id": 999999,
            "query": "main",
        },
    )

    assert response.status_code == 404