"""Pydantic models for the Reports app."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ReportStatus = Literal["pending", "approved", "rejected", "archived"]


class Report(BaseModel):
    """Report record."""

    model_config = ConfigDict(frozen=True)

    id: int
    internal_id: str
    title: str
    status: ReportStatus
    owner: str
    owner_email: str
    amount: float
    created_at: datetime


class ReportPublic(BaseModel):
    """Public response shape."""

    id: int
    title: str
    status: ReportStatus
    owner: str
    amount: float
    created_at: datetime

    @classmethod
    def from_internal(cls, r: Report) -> "ReportPublic":
        return cls(
            id=r.id,
            title=r.title,
            status=r.status,
            owner=r.owner,
            amount=r.amount,
            created_at=r.created_at,
        )


class ReportListResponse(BaseModel):
    """Paginated list response."""

    items: list[ReportPublic]
    total: int = Field(description="Total number of rows matching the filter")
    offset: int
    limit: int
