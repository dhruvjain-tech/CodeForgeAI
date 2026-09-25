def test_create_task(client):
    response = client.post(
        "/api/v1/tasks/",
        json={
            "project_id": 1,
            "repository_id": None,
            "title": "API Test Task",
            "description": "Testing Task API",
            "priority": "high",
            "assigned_agent": "Architect",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "API Test Task"
    assert data["status"] == "queued"


def test_get_task(client):
    create_response = client.post(
        "/api/v1/tasks/",
        json={
            "project_id": 1,
            "title": "GET Test Task",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/tasks/{task_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_update_task(client):
    create_response = client.post(
        "/api/v1/tasks/",
        json={
            "project_id": 1,
            "title": "Before Update",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "After Update",
            "status": "running",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "After Update"
    assert data["status"] == "running"


def test_delete_task(client):
    create_response = client.post(
        "/api/v1/tasks/",
        json={
            "project_id": 1,
            "title": "Delete Test Task",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/api/v1/tasks/{task_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/api/v1/tasks/{task_id}"
    )

    assert get_response.status_code == 404