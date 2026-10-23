import time

import requests
from sqlalchemy.orm import Session

from . import models

def save_monitoring_result(
    db: Session,
    result: dict
):
    monitoring_result = models.MonitoringResult(
        endpoint=result["endpoint"],
        status_code=result["status_code"],
        status=result["status"],
        response_time_ms=result["response_time_ms"],
        attempt=result["attempt"],
        error_message=result["error_message"]
    )

    db.add(monitoring_result)
    db.commit()
    db.refresh(monitoring_result)

    return monitoring_result

def monitor_api(
    endpoint: str,
    max_retries: int = 3,
    timeout: int = 5
):
    last_error = None
    last_status_code = None
    last_response_time = 0

    for attempt in range(1, max_retries + 1):

        start_time = time.perf_counter()

        try:
            response = requests.get(
                endpoint,
                timeout=timeout
            )

            response_time = (
                time.perf_counter() - start_time
            ) * 1000

            last_response_time = response_time
            last_status_code = response.status_code

            response.raise_for_status()

            try:
                data = response.json()
            except ValueError as error:
                return {
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "status": "FAILED",
                    "response_time_ms": round(
                        response_time, 2
                    ),
                    "attempt": attempt,
                    "error_message": (
                        f"Invalid JSON response: {error}"
                    ),
                    "data": None
                }

            return {
                "endpoint": endpoint,
                "status_code": response.status_code,
                "status": "SUCCESS",
                "response_time_ms": round(
                    response_time, 2
                ),
                "attempt": attempt,
                "error_message": None,
                "data": data
            }

        except requests.exceptions.Timeout:
            last_error = "Request timed out"

        except requests.exceptions.HTTPError as error:
            last_error = str(error)

        except requests.exceptions.RequestException as error:
            last_error = str(error)

        if attempt < max_retries:
            time.sleep(1)

    return {
        "endpoint": endpoint,
        "status_code": last_status_code,
        "status": "FAILED",
        "response_time_ms": round(
            last_response_time, 2
        ),
        "attempt": max_retries,
        "error_message": last_error,
        "data": None
    }

def create_failure_service_request(
    db: Session,
    result: dict
):
    # Check whether an OPEN service request already exists
    # for this endpoint.

    existing_request = (
        db.query(models.ServiceRequest)
        .filter(
            models.ServiceRequest.status == "OPEN",
            models.ServiceRequest.title == "External API failure",
            models.ServiceRequest.description.contains(
                result["endpoint"]
            ),
        )
        .first()
    )

    # Do not create a duplicate request
    if existing_request:
        return existing_request

    # Create a new service request
    service_request = models.ServiceRequest(
        title="External API failure",
        description=(
            f"API monitoring detected a failure. "
            f"Endpoint: {result['endpoint']}. "
            f"HTTP status: {result['status_code']}. "
            f"Error: {result['error_message']}"
        ),
        status="OPEN",
        priority="HIGH",
        requester="API Monitor",
        assigned_to="Operations Team",
    )

    db.add(service_request)
    db.commit()
    db.refresh(service_request)

    return service_request