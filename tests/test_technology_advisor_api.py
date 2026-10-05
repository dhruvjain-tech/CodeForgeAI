def test_recommend_technology(client):
    response = client.post(
        "/api/v1/technology-advisor/recommend",
        json={
            "category": "database",
            "workload": "concurrency",
            "requirements": [
                "relational queries",
            ],
            "options": [
                {
                    "name": "PostgreSQL",
                    "category": "database",
                    "strengths": [
                        "high concurrency",
                        "relational queries",
                    ],
                    "weaknesses": [],
                },
                {
                    "name": "SQLite",
                    "category": "database",
                    "strengths": [
                        "simple local storage",
                    ],
                    "weaknesses": [],
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recommendation"] == "PostgreSQL"
    assert "SQLite" in data["alternatives"]
    assert len(data["reasoning"]) > 0


def test_compare_technologies(client):
    response = client.post(
        "/api/v1/technology-advisor/compare",
        json={
            "category": "database",
            "workload": "concurrency",
            "requirements": [
                "relational queries",
            ],
            "options": [
                {
                    "name": "PostgreSQL",
                    "category": "database",
                    "strengths": [
                        "high concurrency",
                        "relational queries",
                    ],
                    "weaknesses": [],
                },
                {
                    "name": "SQLite",
                    "category": "database",
                    "strengths": [
                        "simple local storage",
                    ],
                    "weaknesses": [],
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["category"] == "database"
    assert data["workload"] == "concurrency"
    assert len(data["results"]) == 2
    assert data["results"][0]["technology"] == "PostgreSQL"


def test_invalid_recommendation_request(client):
    response = client.post(
        "/api/v1/technology-advisor/recommend",
        json={
            "category": "database",
            "workload": "concurrency",
            "options": [],
        },
    )

    assert response.status_code == 422