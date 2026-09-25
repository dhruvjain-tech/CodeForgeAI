from sqlalchemy.orm import Session

from models import Task
from schemas.task import TaskCreate, TaskUpdate


def get_all_tasks(db: Session):
    return db.query(Task).all()


def get_task_by_id(
    db: Session,
    task_id: int,
):
    return (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )


def get_tasks_by_project(
    db: Session,
    project_id: int,
):
    return (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .all()
    )


def create_task(
    db: Session,
    task_data: TaskCreate,
):
    task = Task(
        project_id=task_data.project_id,
        repository_id=task_data.repository_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        assigned_agent=task_data.assigned_agent,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def update_task(
    db: Session,
    task: Task,
    task_data: TaskUpdate,
):
    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.priority is not None:
        task.priority = task_data.priority

    if task_data.status is not None:
        task.status = task_data.status

    if task_data.assigned_agent is not None:
        task.assigned_agent = task_data.assigned_agent

    if task_data.repository_id is not None:
        task.repository_id = task_data.repository_id

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task,
):
    db.delete(task)
    db.commit()