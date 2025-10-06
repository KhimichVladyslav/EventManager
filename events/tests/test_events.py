import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from events.models import Event


@pytest.mark.django_db
def get_auth_client(username="testuser", password="pass123"):
    """Helper to create a user, get JWT token and return authorized client."""
    user = User.objects.create_user(username=username, password=password)
    client = APIClient()
    resp = client.post("/api/token/", {"username": username, "password": password})
    token = resp.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, user


@pytest.mark.django_db
def test_create_event_authenticated():
    client, _ = get_auth_client()
    resp = client.post(
        "/api/events/",
        {
            "title": "My Event",
            "description": "Test desc",
            "date": "2030-01-01T10:00:00Z",
            "location": "Kyiv",
        },
    )
    assert resp.status_code == 201
    assert resp.data["title"] == "My Event"


@pytest.mark.django_db
def test_update_event_only_organizer_or_admin():
    client_org, organizer = get_auth_client("org", "pass123")
    event = Event.objects.create(
        title="Event",
        description="Desc",
        date="2030-01-01T10:00:00Z",
        location="Kyiv",
        organizer=organizer,
    )

    client_other, _ = get_auth_client("other", "pass123")
    resp = client_other.put(
        f"/api/events/{event.id}/",
        {
            "title": "Hello",
            "description": "x",
            "date": "2030-01-01T10:00:00Z",
            "location": "Lviv",
        },
    )
    assert resp.status_code == 403  # forbidden

    resp2 = client_org.put(
        f"/api/events/{event.id}/",
        {
            "title": "Hello",
            "description": "x",
            "date": "2030-01-01T10:00:00Z",
            "location": "Lviv",
        },
    )
    assert resp2.status_code == 200


@pytest.mark.django_db
def test_search_event():
    client, _ = get_auth_client()
    Event.objects.create(
        title="Snooker Championship",
        description="World final",
        date="2030-01-01T10:00:00Z",
        location="London",
        organizer=User.objects.create_user(username="org", password="pass"),
    )

    resp = client.get("/api/events/?search=Snooker")
    assert resp.status_code == 200
    assert resp.data["count"] == 1
