import pytest
from django.shortcuts import reverse


@pytest.mark.django_db
def test_get_token_no_user(client):
    username = "another_user"
    password = "123456"

    print(reverse("token_get"))
    resp = client.post(
        reverse("token_get"),
        data={"username": username, "password": password},
        content_type="application/json",
    )

    payload = resp.json()
    assert "access" not in payload
    assert "refresh" not in payload


def test_get_token_ok(client, user):
    resp = client.post(
        reverse("token_get"),
        data={"username": user.username, "password": user.password_},
        content_type="application/json",
    )

    payload = resp.json()
    assert "access" in payload
    assert "refresh" in payload


def test_refresh_token_ok(client, user):
    resp = client.post(
        reverse("token_get"),
        data={"username": user.username, "password": user.password_},
        content_type="application/json",
    )

    payload = resp.json()
    assert "access" in payload
    assert "refresh" in payload

    resp = client.post(
        reverse("token_refresh"),
        data={"refresh": payload["refresh"]},
        content_type="application/json",
    )

    payload = resp.json()
    assert "access" in payload
    assert "refresh" in payload
