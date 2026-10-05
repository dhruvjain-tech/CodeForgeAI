from sqlalchemy.orm import Session

from models.repository_analysis import (
    RepositoryAnalysis,
    RepositoryAnalysisDependency,
    RepositoryAnalysisFile,
    RepositoryAnalysisSymbol,
)


def search_files(
    db: Session,
    repository_id: int,
    query: str,
) -> list[RepositoryAnalysisFile]:
    return (
        db.query(RepositoryAnalysisFile)
        .join(
            RepositoryAnalysis,
            RepositoryAnalysisFile.analysis_id
            == RepositoryAnalysis.id,
        )
        .filter(
            RepositoryAnalysis.repository_id == repository_id,
            RepositoryAnalysisFile.relative_path.ilike(
                f"%{query}%"
            ),
        )
        .order_by(
            RepositoryAnalysisFile.relative_path
        )
        .all()
    )


def search_symbols(
    db: Session,
    repository_id: int,
    query: str,
) -> list[RepositoryAnalysisSymbol]:
    return (
        db.query(RepositoryAnalysisSymbol)
        .join(
            RepositoryAnalysis,
            RepositoryAnalysisSymbol.analysis_id
            == RepositoryAnalysis.id,
        )
        .filter(
            RepositoryAnalysis.repository_id == repository_id,
            RepositoryAnalysisSymbol.name.ilike(
                f"%{query}%"
            ),
        )
        .order_by(
            RepositoryAnalysisSymbol.name
        )
        .all()
    )


def search_dependencies(
    db: Session,
    repository_id: int,
    query: str,
) -> list[RepositoryAnalysisDependency]:
    return (
        db.query(RepositoryAnalysisDependency)
        .join(
            RepositoryAnalysis,
            RepositoryAnalysisDependency.analysis_id
            == RepositoryAnalysis.id,
        )
        .filter(
            RepositoryAnalysis.repository_id == repository_id,
            RepositoryAnalysisDependency.target.ilike(
                f"%{query}%"
            ),
        )
        .order_by(
            RepositoryAnalysisDependency.target
        )
        .all()
    )