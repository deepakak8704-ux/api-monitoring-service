from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from . import models
from .api_monitor import (
    create_failure_service_request,
    monitor_api,
    save_monitoring_result,
)
from .database import Base, SessionLocal, engine
from .schemas import (
    MonitorRequest,
    MonitorResponse,
    MonitoringResultResponse,
    ServiceRequestCreate,
    ServiceRequestResponse,
    ServiceRequestUpdate,
)


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title="API Monitoring & Service Request Management System",
    description=(
        "Week 3 Python Development Internship Project - "
        "API Monitoring and Service Request Management"
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# DATABASE DEPENDENCY
# ---------------------------------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "API Monitoring & Service Request Management System",
        "status": "running",
    }


# =========================================================
# SERVICE REQUEST MANAGEMENT
# =========================================================


# ---------------------------------------------------------
# CREATE SERVICE REQUEST
# ---------------------------------------------------------

@app.post(
    "/service-requests",
    response_model=ServiceRequestResponse,
    status_code=201,
)
def create_service_request(
    request: ServiceRequestCreate,
    db: Session = Depends(get_db),
):
    service_request = models.ServiceRequest(
        title=request.title,
        description=request.description,
        priority=request.priority,
        requester=request.requester,
        assigned_to=request.assigned_to,
    )

    db.add(service_request)
    db.commit()
    db.refresh(service_request)

    return service_request


# ---------------------------------------------------------
# GET ALL SERVICE REQUESTS
# SEARCH + STATUS FILTER + PRIORITY FILTER
# ---------------------------------------------------------

@app.get(
    "/service-requests",
    response_model=list[ServiceRequestResponse],
)
def get_service_requests(
    status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(models.ServiceRequest)

    # Filter by status
    if status:
        query = query.filter(
            models.ServiceRequest.status == status
        )

    # Filter by priority
    if priority:
        query = query.filter(
            models.ServiceRequest.priority == priority
        )

    # Search title and description
    if search:
        search_pattern = f"%{search}%"

        query = query.filter(
            (models.ServiceRequest.title.ilike(search_pattern))
            | (
                models.ServiceRequest.description.ilike(
                    search_pattern
                )
            )
        )

    return query.all()


# ---------------------------------------------------------
# GET SERVICE REQUEST BY ID
# ---------------------------------------------------------

@app.get(
    "/service-requests/{request_id}",
    response_model=ServiceRequestResponse,
)
def get_service_request(
    request_id: int,
    db: Session = Depends(get_db),
):
    service_request = (
        db.query(models.ServiceRequest)
        .filter(
            models.ServiceRequest.id == request_id
        )
        .first()
    )

    if not service_request:
        raise HTTPException(
            status_code=404,
            detail="Service request not found",
        )

    return service_request


# ---------------------------------------------------------
# UPDATE SERVICE REQUEST
# ---------------------------------------------------------

@app.put(
    "/service-requests/{request_id}",
    response_model=ServiceRequestResponse,
)
def update_service_request(
    request_id: int,
    request: ServiceRequestUpdate,
    db: Session = Depends(get_db),
):
    service_request = (
        db.query(models.ServiceRequest)
        .filter(
            models.ServiceRequest.id == request_id
        )
        .first()
    )

    if not service_request:
        raise HTTPException(
            status_code=404,
            detail="Service request not found",
        )

    update_data = request.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(service_request, field, value)

    db.commit()
    db.refresh(service_request)

    return service_request


# ---------------------------------------------------------
# DELETE SERVICE REQUEST
# ---------------------------------------------------------

@app.delete(
    "/service-requests/{request_id}",
    status_code=204,
)
def delete_service_request(
    request_id: int,
    db: Session = Depends(get_db),
):
    service_request = (
        db.query(models.ServiceRequest)
        .filter(
            models.ServiceRequest.id == request_id
        )
        .first()
    )

    if not service_request:
        raise HTTPException(
            status_code=404,
            detail="Service request not found",
        )

    db.delete(service_request)
    db.commit()

    return None


# =========================================================
# API MONITORING
# =========================================================


# ---------------------------------------------------------
# MONITOR EXTERNAL API
# ---------------------------------------------------------

@app.post(
    "/monitor",
    response_model=MonitorResponse,
)
def monitor_endpoint(
    request: MonitorRequest,
    db: Session = Depends(get_db),
):
    # Step 1: Monitor the external API
    result = monitor_api(
        str(request.endpoint)
    )

    # Step 2: Save monitoring result
    saved_result = save_monitoring_result(
        db,
        result,
    )

    # Step 3: Automatically create a service request
    # when API monitoring fails
    if result["status"] == "FAILED":
        create_failure_service_request(
            db,
            result,
        )

    # Step 4: Return monitoring result
    return {
        "id": saved_result.id,
        "endpoint": saved_result.endpoint,
        "status_code": saved_result.status_code,
        "status": saved_result.status,
        "response_time_ms": saved_result.response_time_ms,
        "attempt": saved_result.attempt,
        "error_message": saved_result.error_message,
    }


# ---------------------------------------------------------
# GET MONITORING HISTORY
# ---------------------------------------------------------

@app.get(
    "/monitoring-results",
    response_model=list[MonitoringResultResponse],
)
def get_monitoring_results(
    db: Session = Depends(get_db),
):
    results = (
        db.query(models.MonitoringResult)
        .order_by(
            models.MonitoringResult.id.desc()
        )
        .all()
    )

    return results


# ---------------------------------------------------------
# MONITORING REPORT
# ---------------------------------------------------------

@app.get("/monitoring-report")
def get_monitoring_report(
    db: Session = Depends(get_db),
):
    results = (
        db.query(models.MonitoringResult)
        .order_by(
            models.MonitoringResult.id.desc()
        )
        .all()
    )

    total_checks = len(results)

    successful_checks = sum(
        1
        for result in results
        if result.status == "SUCCESS"
    )

    failed_checks = sum(
        1
        for result in results
        if result.status == "FAILED"
    )

    if total_checks > 0:

        success_rate = (
            successful_checks / total_checks
        ) * 100

        failure_rate = (
            failed_checks / total_checks
        ) * 100

        average_response_time = (
            sum(
                result.response_time_ms
                for result in results
            )
            / total_checks
        )

    else:
        success_rate = 0
        failure_rate = 0
        average_response_time = 0

    return {
        "total_checks": total_checks,
        "successful_checks": successful_checks,
        "failed_checks": failed_checks,
        "success_rate_percent": round(
            success_rate,
            2,
        ),
        "failure_rate_percent": round(
            failure_rate,
            2,
        ),
        "average_response_time_ms": round(
            average_response_time,
            2,
        ),
    }