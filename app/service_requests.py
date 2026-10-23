from sqlalchemy.orm import Session

from . import models
from .schemas import ServiceRequestCreate, ServiceRequestUpdate


def create_service_request(
    db: Session,
    request_data: ServiceRequestCreate
):
    service_request = models.ServiceRequest(
        title=request_data.title,
        description=request_data.description,
        priority=request_data.priority.value,
        requester=request_data.requester,
        assigned_to=request_data.assigned_to
    )

    db.add(service_request)
    db.commit()
    db.refresh(service_request)

    return service_request


def get_service_request(
    db: Session,
    request_id: int
):
    return (
        db.query(models.ServiceRequest)
        .filter(models.ServiceRequest.id == request_id)
        .first()
    )


def get_service_requests(
    db: Session,
    status: str | None = None,
    priority: str | None = None,
    search: str | None = None
):
    query = db.query(models.ServiceRequest)

    if status:
        query = query.filter(
            models.ServiceRequest.status == status
        )

    if priority:
        query = query.filter(
            models.ServiceRequest.priority == priority
        )

    if search:
        query = query.filter(
            models.ServiceRequest.title.ilike(f"%{search}%")
        )

    return query.all()


def update_service_request(
    db: Session,
    service_request: models.ServiceRequest,
    request_data: ServiceRequestUpdate
):
    update_data = request_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        if hasattr(value, "value"):
            value = value.value

        setattr(service_request, field, value)

    db.commit()
    db.refresh(service_request)

    return service_request


def delete_service_request(
    db: Session,
    service_request: models.ServiceRequest
):
    db.delete(service_request)
    db.commit()