from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.task import TaskCreate, TaskResponse, TaskUpdate
from services.task_service import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    get_tasks_by_project,
    update_task,
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get(
    "/",
    response_model=list[TaskResponse],
)
def get_tasks(
    db: Session = Depends(get_db),
):
    return get_all_tasks(db)


@router.get(
    "/project/{project_id}",
    response_model=list[TaskResponse],
)
def get_project_tasks(
    project_id: int,
    db: Session = Depends(get_db),
):
    return get_tasks_by_project(db, project_id)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    return create_task(db, task_data)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
)
def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return update_task(db, task, task_data)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    delete_task(db, task)

    return None