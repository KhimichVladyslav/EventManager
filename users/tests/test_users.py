import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register_user():
    client = APIClient()
    resp = client.post("/api/users/register/", {"username": "Slava", "email": "new@example.com", "password": "pass123"})
    assert resp.status_code == 201
    assert User.objects.filter(username="Slava").exists()


@pytest.mark.django_db
def test_me_endpoint():
    _user = User.objects.create_user(username="vlad", password="VladPro")  # noqa: F841
    client = APIClient()
    token = client.post("/api/token/", {"username": "vlad", "password": "VladPro"}).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    resp = client.get("/api/users/me/")
    assert resp.status_code == 200
    assert resp.data["username"] == "vlad"


@pytest.mark.django_db
def test_user_list_admin_only():
    _admin = User.objects.create_superuser(username="admin", password="pass123", email="a@a.com")  # noqa: F841
    client = APIClient()
    token = client.post("/api/token/", {"username": "admin", "password": "pass123"}).data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    resp = client.get("/api/users/list/")
    assert resp.status_code == 200
