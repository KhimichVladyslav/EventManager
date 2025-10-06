import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from events.models import Event, EventRegistration


@pytest.mark.django_db
def get_auth_client(username="testuser", password="pass123"):
    user = User.objects.create_user(username=username, password=password)
    client = APIClient()
    resp = client.post("/api/token/", {"username": username, "password": password})
    token = resp.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, user


@pytest.mark.django_db
def test_register_for_event():
    client, user = get_auth_client()
    event = Event.objects.create(
        title="Concert",
        description="Rock show",
        date="2030-01-01T10:00:00Z",
        location="Kyiv",
        organizer=user,
    )

    resp = client.post("/api/registrations/", {"event": event.id})
    assert resp.status_code == 201
    assert EventRegistration.objects.filter(user=user, event=event).exists()


@pytest.mark.django_db
def test_register_twice_forbidden():
    client, user = get_auth_client()
    event = Event.objects.create(
        title="Concert",
        description="Rock show",
        date="2030-01-01T10:00:00Z",
        location="Kyiv",
        organizer=user,
    )
    EventRegistration.objects.create(user=user, event=event)

    resp = client.post("/api/registrations/", {"event": event.id})
    assert resp.status_code == 400
    assert "Already registered" in str(resp.data)
