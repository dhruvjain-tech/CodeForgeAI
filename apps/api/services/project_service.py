from sqlalchemy.orm import Session

from models import Project
from schemas.project import ProjectCreate, ProjectUpdate


def get_all_projects(db: Session):
    return db.query(Project).all()


def get_project_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def create_project(db: Session, project_data: ProjectCreate):
    project = Project(
        name=project_data.name,
        description=project_data.description,
        repository_url=project_data.repository_url,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return project


def update_project(
    db: Session,
    project: Project,
    project_data: ProjectUpdate,
):
    if project_data.name is not None:
        project.name = project_data.name

    if project_data.description is not None:
        project.description = project_data.description

    if project_data.repository_url is not None:
        project.repository_url = project_data.repository_url

    db.commit()
    db.refresh(project)

    return project


def delete_project(db: Session, project: Project):
    db.delete(project)
    db.commit()