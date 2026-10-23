def test_create_service_request(client):
    response = client.post(
        "/service-requests",
        json={
            "title": "Test Service Request",
            "description": "Testing service request creation",
            "priority": "HIGH",
            "requester": "Test User",
            "assigned_to": "Employee01",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test Service Request"
    assert data["priority"] == "HIGH"
    assert data["status"] == "OPEN"


def test_get_service_requests(client):
    response = client.get(
        "/service-requests"
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_service_request_by_id(client):
    create_response = client.post(
        "/service-requests",
        json={
            "title": "Test Request",
            "description": "Testing GET by ID",
            "priority": "MEDIUM",
            "requester": "Test User",
            "assigned_to": "Employee01",
        },
    )

    assert create_response.status_code == 201

    request_id = create_response.json()["id"]

    response = client.get(
        f"/service-requests/{request_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == request_id


def test_get_nonexistent_service_request(client):
    response = client.get(
        "/service-requests/999999"
    )

    assert response.status_code == 404


def test_service_request_search(client):
    response = client.get(
        "/service-requests",
        params={
            "search": "Test"
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_service_request_filter_by_priority(client):
    response = client.get(
        "/service-requests",
        params={
            "priority": "HIGH"
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_service_request_filter_by_status(client):
    response = client.get(
        "/service-requests",
        params={
            "status": "OPEN"
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)