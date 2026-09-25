from models import Project, Task
from schemas.task import TaskCreate, TaskUpdate

from services.task_service import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    get_tasks_by_project,
    update_task,
)


def test_create_and_get_task(db_session):
    project = Project(
        name="Task Test Project",
        description="Testing tasks",
    )

    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    task = create_task(
        db_session,
        TaskCreate(
            project_id=project.id,
            title="Test Task",
            description="Testing CodeForge AI task",
            priority="high",
            assigned_agent="Architect",
        ),
    )

    assert task.id is not None
    assert task.title == "Test Task"
    assert task.status == "queued"
    assert task.assigned_agent == "Architect"

    tasks = get_all_tasks(db_session)

    assert len(tasks) == 1
    assert tasks[0].title == "Test Task"

    fetched_task = get_task_by_id(
        db_session,
        task.id,
    )

    assert fetched_task is not None
    assert fetched_task.id == task.id


def test_get_tasks_by_project(db_session):
    project = Project(
        name="Project Task Test",
    )

    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    create_task(
        db_session,
        TaskCreate(
            project_id=project.id,
            title="Project Task",
        ),
    )

    tasks = get_tasks_by_project(
        db_session,
        project.id,
    )

    assert len(tasks) == 1
    assert tasks[0].project_id == project.id


def test_update_and_delete_task(db_session):
    project = Project(
        name="Update Task Project",
    )

    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    task = Task(
        project_id=project.id,
        title="Before Update",
        description="Before",
        priority="medium",
        status="queued",
    )

    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    updated_task = update_task(
        db_session,
        task,
        TaskUpdate(
            title="After Update",
            status="running",
            priority="high",
        ),
    )

    assert updated_task.title == "After Update"
    assert updated_task.status == "running"
    assert updated_task.priority == "high"

    delete_task(
        db_session,
        updated_task,
    )

    deleted_task = get_task_by_id(
        db_session,
        updated_task.id,
    )

    assert deleted_task is None