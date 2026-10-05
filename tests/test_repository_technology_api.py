from pathlib import Path


def test_repository_recommendation_api(
    client,
    tmp_path: Path,
):
    source_file = tmp_path / "app.py"

    source_file.write_text(
        "import os\n\n"
        "class App:\n"
        "    def run(self):\n"
        "        return True\n",
        encoding="utf-8",
    )

    response = client.post(
        "/api/v1/technology-advisor/repository-recommend",
        json={
            "root_path": str(tmp_path),
            "category": "database",
            "workload": "concurrency",
            "requirements": [],
            "options": [
                {
                    "name": "PostgreSQL",
                    "category": "database",
                    "strengths": [
                        "high concurrency",
                        "python",
                    ],
                    "weaknesses": [],
                },
                {
                    "name": "SQLite",
                    "category": "database",
                    "strengths": [
                        "simple local storage",
                    ],
                    "weaknesses": [
                        "high concurrency",
                    ],
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recommendation"] == "PostgreSQL"
    assert data["repository"]["file_count"] == 1
    assert data["repository"]["symbol_count"] == 2
    assert data["repository"]["location_count"] == 2


def test_repository_recommendation_missing_path(
    client,
):
    response = client.post(
        "/api/v1/technology-advisor/repository-recommend",
        json={
            "root_path": "D:/does-not-exist",
            "category": "database",
            "workload": "concurrency",
            "options": [
                {
                    "name": "PostgreSQL",
                    "category": "database",
                    "strengths": [
                        "high concurrency",
                    ],
                    "weaknesses": [],
                }
            ],
        },
    )

    assert response.status_code == 400


def test_repository_recommendation_validation(
    client,
):
    response = client.post(
        "/api/v1/technology-advisor/repository-recommend",
        json={
            "category": "database",
            "workload": "concurrency",
            "options": [],
        },
    )

    assert response.status_code == 422