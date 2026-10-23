def test_monitor_success(client):
    response = client.post(
        "/monitor",
        json={
            "endpoint": "https://jsonplaceholder.typicode.com/posts"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["endpoint"] == (
        "https://jsonplaceholder.typicode.com/posts"
    )

    assert data["status"] == "SUCCESS"
    assert data["status_code"] == 200
    assert data["attempt"] == 1
    assert data["response_time_ms"] >= 0


def test_monitor_failure(client):
    response = client.post(
        "/monitor",
        json={
            "endpoint": (
                "https://jsonplaceholder.typicode.com/"
                "invalid-endpoint"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "FAILED"
    assert data["status_code"] == 404
    assert data["attempt"] == 3
    assert data["error_message"] is not None


def test_get_monitoring_results(client):
    response = client.get(
        "/monitoring-results"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_monitoring_report(client):
    response = client.get(
        "/monitoring-report"
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_checks" in data
    assert "successful_checks" in data
    assert "failed_checks" in data
    assert "success_rate_percent" in data
    assert "failure_rate_percent" in data
    assert "average_response_time_ms" in data


def test_invalid_monitor_request(client):
    response = client.post(
        "/monitor",
        json={}
    )

    assert response.status_code == 422