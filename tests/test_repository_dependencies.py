from core.repository.dependencies import DependencyAnalyzer
from core.repository.types import RepositoryFile


def test_analyzer_detects_imports(tmp_path):
    source = """
import os
import json
from pathlib import Path
from core.repository.types import RepositoryFile
"""

    path = tmp_path / "main.py"
    path.write_text(source, encoding="utf-8")

    file = RepositoryFile(
        path=str(path),
        relative_path="main.py",
        extension=".py",
        size_bytes=path.stat().st_size,
        language="Python",
    )

    dependencies = DependencyAnalyzer().analyze_file(file)

    targets = {dependency.target for dependency in dependencies}

    assert "os" in targets
    assert "json" in targets
    assert "pathlib" in targets
    assert "core.repository.types" in targets


def test_dependency_types_are_correct(tmp_path):
    source = """
import os
from pathlib import Path
"""

    path = tmp_path / "main.py"
    path.write_text(source, encoding="utf-8")

    file = RepositoryFile(
        path=str(path),
        relative_path="main.py",
        extension=".py",
        size_bytes=path.stat().st_size,
        language="Python",
    )

    dependencies = DependencyAnalyzer().analyze_file(file)

    import_dep = next(d for d in dependencies if d.target == "os")
    from_dep = next(d for d in dependencies if d.target == "pathlib")

    assert import_dep.dependency_type == "import"
    assert from_dep.dependency_type == "from_import"


def test_non_python_returns_empty(tmp_path):
    path = tmp_path / "app.ts"
    path.write_text("import React from 'react';", encoding="utf-8")

    file = RepositoryFile(
        path=str(path),
        relative_path="app.ts",
        extension=".ts",
        size_bytes=path.stat().st_size,
        language="TypeScript",
    )

    dependencies = DependencyAnalyzer().analyze_file(file)

    assert dependencies == []


def test_invalid_python_returns_empty(tmp_path):
    path = tmp_path / "broken.py"
    path.write_text("from something import", encoding="utf-8")

    file = RepositoryFile(
        path=str(path),
        relative_path="broken.py",
        extension=".py",
        size_bytes=path.stat().st_size,
        language="Python",
    )

    dependencies = DependencyAnalyzer().analyze_file(file)

    assert dependencies == []