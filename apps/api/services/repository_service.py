from sqlalchemy.orm import Session

from models import Repository
from schemas.repository import RepositoryCreate, RepositoryUpdate


def get_all_repositories(db: Session):
    return db.query(Repository).all()


def get_repository_by_id(
    db: Session,
    repository_id: int,
):
    return (
        db.query(Repository)
        .filter(Repository.id == repository_id)
        .first()
    )


def get_repositories_by_project(
    db: Session,
    project_id: int,
):
    return (
        db.query(Repository)
        .filter(Repository.project_id == project_id)
        .all()
    )


def create_repository(
    db: Session,
    repository_data: RepositoryCreate,
):
    repository = Repository(
        project_id=repository_data.project_id,
        name=repository_data.name,
        repository_url=repository_data.repository_url,
        default_branch=repository_data.default_branch,
        local_path=repository_data.local_path,
    )

    db.add(repository)
    db.commit()
    db.refresh(repository)

    return repository


def update_repository(
    db: Session,
    repository: Repository,
    repository_data: RepositoryUpdate,
):
    if repository_data.name is not None:
        repository.name = repository_data.name

    if repository_data.repository_url is not None:
        repository.repository_url = repository_data.repository_url

    if repository_data.default_branch is not None:
        repository.default_branch = repository_data.default_branch

    if repository_data.local_path is not None:
        repository.local_path = repository_data.local_path

    if repository_data.status is not None:
        repository.status = repository_data.status

    db.commit()
    db.refresh(repository)

    return repository


def delete_repository(
    db: Session,
    repository: Repository,
):
    db.delete(repository)
    db.commit()