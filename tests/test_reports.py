"""Baseline tests for the Reports API. Keep these green throughout the exercise."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_list_reports_default_pagination() -> None:
    r = client.get("/reports")
    assert r.status_code == 200
    body = r.json()
    assert body["offset"] == 0
    assert body["limit"] == 20
    assert len(body["items"]) == 20
    assert body["total"] == 120


def test_list_reports_filters_by_status() -> None:
    r = client.get("/reports", params={"status": "approved", "limit": 200})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] > 0
    assert all(item["status"] == "approved" for item in body["items"])


def test_list_reports_pagination_offset() -> None:
    first = client.get("/reports", params={"limit": 5}).json()
    second = client.get("/reports", params={"limit": 5, "offset": 5}).json()
    first_ids = [it["id"] for it in first["items"]]
    second_ids = [it["id"] for it in second["items"]]
    assert set(first_ids).isdisjoint(set(second_ids))


def test_list_reports_rejects_bad_sort_field() -> None:
    r = client.get("/reports", params={"sort": "not_a_field"})
    assert r.status_code == 400
