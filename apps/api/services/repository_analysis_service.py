from sqlalchemy.orm import Session

from models.repository_analysis import (
    RepositoryAnalysis,
    RepositoryAnalysisDependency,
    RepositoryAnalysisFile,
    RepositoryAnalysisSymbol,
)

from core.repository.types import (
    RepositoryAnalysis as RepositoryAnalysisResult,
)


def save_repository_analysis(
    db: Session,
    repository_id: int,
    result: RepositoryAnalysisResult,
) -> RepositoryAnalysis:
    analysis = RepositoryAnalysis(
        repository_id=repository_id,
        root_path=result.root_path,
        file_count=len(result.files),
        symbol_count=len(result.symbols),
        dependency_count=len(result.dependencies),
    )

    db.add(analysis)
    db.flush()

    for file in result.files:
        analysis.files.append(
            RepositoryAnalysisFile(
                path=file.path,
                relative_path=file.relative_path,
                extension=file.extension,
                size_bytes=file.size_bytes,
                language=file.language,
            )
        )

    for symbol in result.symbols:
        analysis.symbols.append(
            RepositoryAnalysisSymbol(
                name=symbol.name,
                symbol_type=symbol.symbol_type,
                file_path=symbol.file_path,
                line_start=symbol.line_start,
                line_end=symbol.line_end,
            )
        )

    for dependency in result.dependencies:
        analysis.dependencies.append(
            RepositoryAnalysisDependency(
                source_file=dependency.source_file,
                target=dependency.target,
                dependency_type=dependency.dependency_type,
            )
        )

    db.commit()
    db.refresh(analysis)

    return analysis


def get_repository_analyses(
    db: Session,
    repository_id: int,
) -> list[RepositoryAnalysis]:
    return (
        db.query(RepositoryAnalysis)
        .filter(
            RepositoryAnalysis.repository_id == repository_id
        )
        .order_by(
            RepositoryAnalysis.created_at.desc()
        )
        .all()
    )


def get_latest_repository_analysis(
    db: Session,
    repository_id: int,
) -> RepositoryAnalysis | None:
    return (
        db.query(RepositoryAnalysis)
        .filter(
            RepositoryAnalysis.repository_id == repository_id
        )
        .order_by(
            RepositoryAnalysis.created_at.desc()
        )
        .first()
    )