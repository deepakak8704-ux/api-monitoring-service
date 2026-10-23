from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String

from .database import Base


def utc_now():
    return datetime.now(timezone.utc)


class ServiceRequest(Base):
    __tablename__ = "service_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default="OPEN")
    priority = Column(String, default="MEDIUM")
    requester = Column(String, nullable=False)
    assigned_to = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        default=utc_now
    )

    updated_at = Column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now
    )


class MonitoringResult(Base):
    __tablename__ = "monitoring_results"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, nullable=False)
    status_code = Column(Integer, nullable=True)
    status = Column(String, nullable=False)
    response_time_ms = Column(Float, nullable=False)
    attempt = Column(Integer, nullable=False)
    error_message = Column(String, nullable=True)

    checked_at = Column(
        DateTime(timezone=True),
        default=utc_now
    )