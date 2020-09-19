import pytest
from django.shortcuts import reverse

from flights.platform import models


@pytest.mark.django_db
def test_create_user_empty(client):

    resp = client.post(
        reverse("user-list"),
        data={},
        content_type="application/json",
    )

    assert resp.status_code == 400
    payload = resp.json()
    assert "This field is required." in payload["username"]
    assert "This field is required." in payload["password"]


@pytest.mark.django_db
def test_create_user_success(client):
    username = "another_user"

    resp = client.post(
        reverse("user-list"),
        data={"username": username, "password": "Xna2123IIO"},
        content_type="application/json",
    )

    assert resp.status_code == 201
    assert models.User.objects.filter(username=username).exists()


@pytest.mark.django_db
def test_create_existing_user(client, user):

    resp = client.post(
        reverse("user-list"),
        data={"username": user.username, "password": "Xna2123IIO"},
        content_type="application/json",
    )

    assert resp.status_code == 400
    payload = resp.json()
    assert "A user with that username already exists." in payload["username"]


@pytest.mark.django_db
def test_create_user_simple_password(client):
    resp = client.post(
        reverse("user-list"),
        data={"username": "user1", "password": "123456"},
        content_type="application/json",
    )

    assert resp.status_code == 400
    payload = resp.json()
    assert "This password is too common." in payload["password"]
