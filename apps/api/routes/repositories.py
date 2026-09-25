from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
    RepositoryUpdate,
)
from services.repository_service import (
    create_repository,
    delete_repository,
    get_all_repositories,
    get_repositories_by_project,
    get_repository_by_id,
    update_repository,
)

router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


@router.get(
    "/",
    response_model=list[RepositoryResponse],
)
def get_repositories(
    db: Session = Depends(get_db),
):
    return get_all_repositories(db)


@router.get(
    "/project/{project_id}",
    response_model=list[RepositoryResponse],
)
def get_project_repositories(
    project_id: int,
    db: Session = Depends(get_db),
):
    return get_repositories_by_project(db, project_id)


@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse,
)
def get_repository(
    repository_id: int,
    db: Session = Depends(get_db),
):
    repository = get_repository_by_id(
        db,
        repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found",
        )

    return repository


@router.post(
    "/",
    response_model=RepositoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_repository(
    repository_data: RepositoryCreate,
    db: Session = Depends(get_db),
):
    return create_repository(
        db,
        repository_data,
    )


@router.patch(
    "/{repository_id}",
    response_model=RepositoryResponse,
)
def update_existing_repository(
    repository_id: int,
    repository_data: RepositoryUpdate,
    db: Session = Depends(get_db),
):
    repository = get_repository_by_id(
        db,
        repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found",
        )

    return update_repository(
        db,
        repository,
        repository_data,
    )


@router.delete(
    "/{repository_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_existing_repository(
    repository_id: int,
    db: Session = Depends(get_db),
):
    repository = get_repository_by_id(
        db,
        repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Repository not found",
        )

    delete_repository(
        db,
        repository,
    )

    return None