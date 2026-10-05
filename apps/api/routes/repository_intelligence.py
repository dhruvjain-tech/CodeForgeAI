from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core.repository.service import repository_analysis_service
from database import get_db
from models.repository import Repository
from models.repository_analysis import RepositoryAnalysis
from services.repository_analysis_service import (
    get_latest_repository_analysis,
    get_repository_analyses,
    save_repository_analysis,
)


router = APIRouter(
    prefix="/repository-intelligence",
    tags=["Repository Intelligence"],
)


class RepositoryAnalyzeRequest(BaseModel):
    root_path: str = Field(..., min_length=1)


class RepositoryAnalyzeAndSaveRequest(BaseModel):
    repository_id: int = Field(..., gt=0)
    root_path: str = Field(..., min_length=1)


def serialize_analysis(result: Any) -> dict[str, Any]:
    return {
        "root_path": result.root_path,
        "files": [
            {
                "path": file.path,
                "relative_path": file.relative_path,
                "extension": file.extension,
                "size_bytes": file.size_bytes,
                "language": file.language,
            }
            for file in result.files
        ],
        "symbols": [
            {
                "name": symbol.name,
                "symbol_type": symbol.symbol_type,
                "file_path": symbol.file_path,
                "line_start": symbol.line_start,
                "line_end": symbol.line_end,
                "metadata": symbol.metadata,
            }
            for symbol in result.symbols
        ],
        "dependencies": [
            {
                "source_file": dependency.source_file,
                "target": dependency.target,
                "dependency_type": dependency.dependency_type,
                "metadata": dependency.metadata,
            }
            for dependency in result.dependencies
        ],
        "metadata": result.metadata,
    }


@router.post("/analyze")
async def analyze_repository(
    request: RepositoryAnalyzeRequest,
) -> dict[str, Any]:
    try:
        result = repository_analysis_service.analyze(
            request.root_path
        )

        return serialize_analysis(result)

    except (FileNotFoundError, NotADirectoryError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post("/analyze-and-save")
async def analyze_and_save_repository(
    request: RepositoryAnalyzeAndSaveRequest,
    db: Session = Depends(get_db),
) -> dict[str, Any]:

    repository = (
        db.query(Repository)
        .filter(
            Repository.id == request.repository_id
        )
        .first()
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    try:
        result = repository_analysis_service.analyze(
            request.root_path
        )

        analysis = save_repository_analysis(
            db,
            repository.id,
            result,
        )

        return {
            "analysis_id": analysis.id,
            "repository_id": analysis.repository_id,
            "root_path": analysis.root_path,
            "file_count": analysis.file_count,
            "symbol_count": analysis.symbol_count,
            "dependency_count": analysis.dependency_count,
            "status": "saved",
        }

    except (FileNotFoundError, NotADirectoryError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("/analyses/{analysis_id}")
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:

    analysis = (
        db.query(RepositoryAnalysis)
        .filter(
            RepositoryAnalysis.id == analysis_id
        )
        .first()
    )

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Repository analysis not found",
        )

    return {
        "id": analysis.id,
        "repository_id": analysis.repository_id,
        "root_path": analysis.root_path,
        "file_count": analysis.file_count,
        "symbol_count": analysis.symbol_count,
        "dependency_count": analysis.dependency_count,
        "created_at": analysis.created_at,
        "files": [
            {
                "id": file.id,
                "path": file.path,
                "relative_path": file.relative_path,
                "extension": file.extension,
                "size_bytes": file.size_bytes,
                "language": file.language,
            }
            for file in analysis.files
        ],
        "symbols": [
            {
                "id": symbol.id,
                "name": symbol.name,
                "symbol_type": symbol.symbol_type,
                "file_path": symbol.file_path,
                "line_start": symbol.line_start,
                "line_end": symbol.line_end,
            }
            for symbol in analysis.symbols
        ],
        "dependencies": [
            {
                "id": dependency.id,
                "source_file": dependency.source_file,
                "target": dependency.target,
                "dependency_type": dependency.dependency_type,
            }
            for dependency in analysis.dependencies
        ],
    }


@router.get("/repositories/{repository_id}/analyses")
def list_repository_analyses(
    repository_id: int,
    db: Session = Depends(get_db),
) -> list[dict[str, Any]]:

    analyses = get_repository_analyses(
        db,
        repository_id,
    )

    return [
        {
            "id": analysis.id,
            "repository_id": analysis.repository_id,
            "root_path": analysis.root_path,
            "file_count": analysis.file_count,
            "symbol_count": analysis.symbol_count,
            "dependency_count": analysis.dependency_count,
            "created_at": analysis.created_at,
        }
        for analysis in analyses
    ]


@router.get("/repositories/{repository_id}/analyses/latest")
def get_latest_analysis(
    repository_id: int,
    db: Session = Depends(get_db),
) -> dict[str, Any]:

    analysis = get_latest_repository_analysis(
        db,
        repository_id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Repository analysis not found",
        )

    return {
        "id": analysis.id,
        "repository_id": analysis.repository_id,
        "root_path": analysis.root_path,
        "file_count": analysis.file_count,
        "symbol_count": analysis.symbol_count,
        "dependency_count": analysis.dependency_count,
        "created_at": analysis.created_at,
    }