from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RequestStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class ServiceRequestCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=5, max_length=500)
    priority: Priority = Priority.MEDIUM
    requester: str = Field(min_length=2, max_length=100)
    assigned_to: str | None = None


class ServiceRequestUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, min_length=5, max_length=500)
    status: RequestStatus | None = None
    priority: Priority | None = None
    assigned_to: str | None = None


class ServiceRequestResponse(BaseModel):
    id: int
    title: str
    description: str
    status: RequestStatus
    priority: Priority
    requester: str
    assigned_to: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

from pydantic import HttpUrl


class MonitorRequest(BaseModel):
    endpoint: HttpUrl


class MonitorResponse(BaseModel):
    id: int
    endpoint: str
    status_code: int | None
    status: str
    response_time_ms: float
    attempt: int
    error_message: str | None

class MonitoringResultResponse(BaseModel):
    id: int
    endpoint: str
    status_code: int | None
    status: str
    response_time_ms: float
    attempt: int
    error_message: str | None