from django.shortcuts import reverse


def test_status_ok(client):
    resp = client.get(reverse("status"))
    assert resp.status_code == 200
