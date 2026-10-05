def test_repository_decision_api(client, tmp_path):

    app_file = tmp_path / "app.py"

    app_file.write_text(
        "class UserService:\n"
        "    def get_users(self):\n"
        "        return []\n",
        encoding="utf-8",
    )

    response = client.post(
        "/api/v1/technology-advisor/repository-decision",
        json={
            "root_path": str(tmp_path),
            "category": "database",
            "workload": "high concurrency database",
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

    assert data["alternatives"] == ["SQLite"]

    assert data["reasoning"]


def test_repository_decision_invalid_path(client):

    response = client.post(
        "/api/v1/technology-advisor/repository-decision",
        json={
            "root_path": "D:/does-not-exist-codeforge",
            "category": "database",
            "workload": "high concurrency",
            "options": [
                {
                    "name": "PostgreSQL",
                    "category": "database",
                    "strengths": ["high concurrency"],
                }
            ],
        },
    )

    assert response.status_code == 400