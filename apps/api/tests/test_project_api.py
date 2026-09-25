import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_project():
    response = client.post(
        "/api/v1/projects/",
        json={
            "name": "API Test Project",
            "description": "Created through API test",
            "repository_url": "https://example.com/api-test",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["name"] == "API Test Project"
    assert data["description"] == "Created through API test"


def test_get_project():
    create_response = client.post(
        "/api/v1/projects/",
        json={
            "name": "GET Test Project",
            "description": "Testing GET project",
            "repository_url": "https://example.com/get-test",
        },
    )

    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/projects/{project_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == project_id
    assert data["name"] == "GET Test Project"


def test_get_projects():
    client.post(
        "/api/v1/projects/",
        json={
            "name": "List Test Project",
            "description": "Testing project list",
            "repository_url": "https://example.com/list-test",
        },
    )

    response = client.get("/api/v1/projects/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "List Test Project"
    
def test_update_project():
    create_response = client.post(
        "/api/v1/projects/",
        json={
            "name": "Update Test Project",
            "description": "Before update",
            "repository_url": "https://example.com/update",
        },
    )

    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/projects/{project_id}",
        json={
            "description": "After update",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == project_id
    assert data["description"] == "After update"


def test_delete_project():
    create_response = client.post(
        "/api/v1/projects/",
        json={
            "name": "Delete Test Project",
            "description": "Testing delete",
            "repository_url": "https://example.com/delete",
        },
    )

    assert create_response.status_code == 201

    project_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/projects/{project_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/api/v1/projects/{project_id}"
    )

    assert get_response.status_code == 404