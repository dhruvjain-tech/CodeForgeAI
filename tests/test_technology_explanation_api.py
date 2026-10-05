def test_explain_recommendation(client):
    response = client.post(
        "/api/v1/technology-advisor/explain",
        json={
            "category": "database",
            "recommendation": "PostgreSQL",
            "alternatives": [
                "SQLite",
                "MongoDB",
            ],
            "reasoning": [
                "Workload: high concurrency",
                "Score: 7",
                "Matched strengths: high concurrency",
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["category"] == "database"
    assert data["recommendation"] == "PostgreSQL"
    assert "PostgreSQL" in data["explanation"]
    assert "SQLite" in data["explanation"]
    assert "high concurrency" in data["explanation"]


def test_explain_without_alternatives(client):
    response = client.post(
        "/api/v1/technology-advisor/explain",
        json={
            "category": "cache",
            "recommendation": "Redis",
            "reasoning": [
                "Workload: caching",
                "Score: 5",
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["recommendation"] == "Redis"
    assert "Redis" in data["explanation"]


def test_invalid_explanation_request(client):
    response = client.post(
        "/api/v1/technology-advisor/explain",
        json={
            "category": "database",
        },
    )

    assert response.status_code == 422