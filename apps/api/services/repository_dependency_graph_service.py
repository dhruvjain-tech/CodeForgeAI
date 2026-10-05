from collections import defaultdict

from sqlalchemy.orm import Session

from models.repository_analysis import RepositoryAnalysisDependency


def get_dependency_graph(
    db: Session,
    analysis_id: int,
) -> dict:
    dependencies = (
        db.query(RepositoryAnalysisDependency)
        .filter(
            RepositoryAnalysisDependency.analysis_id == analysis_id
        )
        .all()
    )

    graph = defaultdict(list)

    for dependency in dependencies:
        graph[dependency.source_file].append(
            {
                "target": dependency.target,
                "dependency_type": dependency.dependency_type,
            }
        )

    return {
        "analysis_id": analysis_id,
        "nodes": list(graph.keys()),
        "edges": [
            {
                "source": dependency.source_file,
                "target": dependency.target,
                "dependency_type": dependency.dependency_type,
            }
            for dependency in dependencies
        ],
        "node_count": len(graph),
        "edge_count": len(dependencies),
    }