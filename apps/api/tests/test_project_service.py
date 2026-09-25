from models import Project
from schemas.project import ProjectUpdate

from services.project_service import (
    create_project,
    delete_project,
    get_all_projects,
    get_project_by_id,
    update_project,
)


def test_create_and_get_project(db_session):
    project = create_project(
        db_session,
        type(
            "ProjectData",
            (),
            {
                "name": "Test Project",
                "description": "Testing CodeForge AI",
                "repository_url": "https://example.com/test",
            },
        )(),
    )

    assert project.id is not None
    assert project.name == "Test Project"

    projects = get_all_projects(db_session)

    assert len(projects) == 1
    assert projects[0].name == "Test Project"

    fetched_project = get_project_by_id(
        db_session,
        project.id,
    )

    assert fetched_project is not None
    assert fetched_project.id == project.id


def test_update_and_delete_project(db_session):
    project = Project(
        name="Update Test",
        description="Before update",
        repository_url="https://example.com/update",
    )

    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    updated_project = update_project(
        db_session,
        project,
        ProjectUpdate(
            description="After update",
        ),
    )

    assert updated_project.description == "After update"

    delete_project(
        db_session,
        updated_project,
    )

    deleted_project = get_project_by_id(
        db_session,
        updated_project.id,
    )

    assert deleted_project is None