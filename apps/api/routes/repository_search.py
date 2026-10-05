from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models.repository import Repository
from services.repository_search_service import (
    search_dependencies,
    search_files,
    search_symbols,
)


router = APIRouter(
    prefix="/repository-search",
    tags=["Repository Search"],
)


def get_repository(
    db: Session,
    repository_id: int,
) -> Repository:
    repository = (
        db.query(Repository)
        .filter(
            Repository.id == repository_id
        )
        .first()
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    return repository


@router.get("/files")
def search_repository_files(
    repository_id: int = Query(..., gt=0),
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    get_repository(db, repository_id)

    files = search_files(
        db,
        repository_id,
        query,
    )

    return [
        {
            "id": file.id,
            "analysis_id": file.analysis_id,
            "path": file.path,
            "relative_path": file.relative_path,
            "extension": file.extension,
            "size_bytes": file.size_bytes,
            "language": file.language,
        }
        for file in files
    ]


@router.get("/symbols")
def search_repository_symbols(
    repository_id: int = Query(..., gt=0),
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    get_repository(db, repository_id)

    symbols = search_symbols(
        db,
        repository_id,
        query,
    )

    return [
        {
            "id": symbol.id,
            "analysis_id": symbol.analysis_id,
            "name": symbol.name,
            "symbol_type": symbol.symbol_type,
            "file_path": symbol.file_path,
            "line_start": symbol.line_start,
            "line_end": symbol.line_end,
        }
        for symbol in symbols
    ]


@router.get("/dependencies")
def search_repository_dependencies(
    repository_id: int = Query(..., gt=0),
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:
    get_repository(db, repository_id)

    dependencies = search_dependencies(
        db,
        repository_id,
        query,
    )

    return [
        {
            "id": dependency.id,
            "analysis_id": dependency.analysis_id,
            "source_file": dependency.source_file,
            "target": dependency.target,
            "dependency_type": dependency.dependency_type,
        }
        for dependency in dependencies
    ]

@router.get("/analyses/{analysis_id}/dependency-graph")
def repository_dependency_graph(
    analysis_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    return get_dependency_graph(
        db,
        analysis_id,
    )