import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault(
    "DATABASE_URL",
    "sqlite:///./test.db",
)

from database import Base, get_db
from main import app
from models import Project, Repository


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


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def repository(db_session):
    project = Project(
        name="Repository Test Project",
        description="Testing repository persistence",
        repository_url="https://example.com/test",
    )

    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    repository = Repository(
        project_id=project.id,
        name="Test Repository",
        repository_url="https://example.com/test-repository",
        default_branch="main",
        local_path="D:/sample-repo",
        status="active",
    )

    db_session.add(repository)
    db_session.commit()
    db_session.refresh(repository)

    return repository