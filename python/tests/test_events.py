import sys
from datetime import date
from pathlib import Path
from unittest.mock import patch

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import pytest

from app import create_app
from app.db import DatabaseError


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()



def test_get_events_returns_list(client):
    expected_events = [
        {
            "id": 1,
            "title": "Testmöte",
            "event_date": "2026-11-15",
            "start_time": "10:00:00",
            "end_time": "11:00:00",
            "description": None,
            "status": "not_done",
            "created_at": "2026-11-10T10:00:00"
        }
    ]

    with patch(
        "app.routes.events.fetch_all",
        return_value=expected_events
    ):
        response = client.get("/events")

    assert response.status_code == 200
    assert response.get_json() == expected_events


def test_get_events_returns_empty_list(client):
    with patch(
        "app.routes.events.fetch_all",
        return_value=[]
    ):
        response = client.get("/events")

    assert response.status_code == 200
    assert response.get_json() == []




def test_get_events_uses_correct_sort_order(client):
    with patch(
        "app.routes.events.fetch_all",
        return_value=[]
    ) as mock_fetch_all:
        response = client.get("/events")

    assert response.status_code == 200

    sql = mock_fetch_all.call_args.args[0]

    assert "ORDER BY event_date ASC, start_time ASC, id ASC" in sql



def test_get_events_filters_by_start_date(client):
    with patch(
        "app.routes.events.fetch_all",
        return_value=[]
    ) as mock_fetch_all:
        response = client.get("/events?start_date=2026-11-12")

    assert response.status_code == 200

    sql, params = mock_fetch_all.call_args.args

    assert "event_date >= %s" in sql
    assert params == [date(2026, 11, 12)]



def test_get_events_filters_by_end_date(client):
    with patch(
        "app.routes.events.fetch_all",
        return_value=[]
    ) as mock_fetch_all:
        response = client.get("/events?end_date=2026-11-20")

    assert response.status_code == 200

    sql, params = mock_fetch_all.call_args.args

    assert "event_date <= %s" in sql
    assert params == [date(2026, 11, 20)]



def test_get_events_filters_by_date_range(client):
    with patch(
        "app.routes.events.fetch_all",
        return_value=[]
    ) as mock_fetch_all:
        response = client.get(
            "/events?start_date=2026-11-10&end_date=2026-11-20"
        )

    assert response.status_code == 200

    sql, params = mock_fetch_all.call_args.args

    assert "event_date >= %s" in sql
    assert "event_date <= %s" in sql
    assert params == [
        date(2026, 11, 10),
        date(2026, 11, 20)
    ]



def test_get_events_rejects_invalid_date(client):
    response = client.get("/events?start_date=2026-13-01")

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Parameter start_date innehåller ett ogiltigt datum."
    }


def test_get_events_rejects_invalid_date_range(client):
    response = client.get(
        "/events?start_date=2026-11-30&end_date=2026-11-01"
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "start_date får inte vara senare än end_date."
    }

def test_get_events_handles_database_error(client):
    with patch(
        "app.routes.events.fetch_all",
        side_effect=DatabaseError("Testfel")
    ):
        response = client.get("/events")

    assert response.status_code == 503
    assert response.get_json() == {
        "error": "Databasen är tillfälligt otillgänglig."
    }

def test_get_event_returns_event(client):
    expected_event = {
        "id": 8,
        "title": "Testmöte API",
        "description": "Test av GET-endpoints",
        "event_date": "2026-11-15",
        "start_time": "10:00:00",
        "end_time": "11:00:00",
        "status": "not_done",
        "created_at": "2026-11-10T21:24:26"
    }

    with patch(
        "app.routes.events.fetch_one",
        return_value=expected_event
    ):
        response = client.get("/events/8")

    assert response.status_code == 200


def test_get_event_returns_404_when_not_found(client):
    with patch(
        "app.routes.events.fetch_one",
        return_value=None
    ):
        response = client.get("/events/999999")

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "Händelsen hittades inte."
    }


def test_get_event_handles_database_error(client):
    with patch(
        "app.routes.events.fetch_one",
        side_effect=DatabaseError("Testfel")
    ):
        response = client.get("/events/8")

    assert response.status_code == 503
    assert response.get_json() == {
        "error": "Databasen är tillfälligt otillgänglig."
    }

def test_get_events_rejects_post_method(client):
    response = client.post("/events")

    assert response.status_code == 405
    assert response.is_json
    assert response.get_json() == {
        "error": "HTTP-metoden stöds inte."
    }


def test_unknown_route_returns_json_404(client):
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert response.is_json
    assert response.get_json() == {
        "error": "Resursen hittades inte."
    }