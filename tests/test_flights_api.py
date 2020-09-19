import random

import pytest
from django.shortcuts import reverse
from django.utils import timezone
from mimesis import Address, Datetime, Numbers
from mimesis.random import Random
from rest_framework_simplejwt.tokens import RefreshToken

from flights.platform import models


@pytest.fixture
def headers(user):
    refresh = RefreshToken.for_user(user)
    return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}


@pytest.fixture
def flight():
    return models.Flight.objects.create(
        name="Flight Name",
        number="FL 1235",
        scheduled_at=timezone.now(),
        expected_at=timezone.now(),
        departure="Stockholm",
        destination="London",
        duration=90,
        fare=345,
    )


@pytest.fixture
def flights():
    return [
        models.Flight.objects.create(
            name=f"Flight_{i}",
            number=Random().custom_code(mask="@@ ####"),
            departure=Address().city(),
            destination=Address().city(),
            scheduled_at=Datetime().datetime(),
            expected_at=Datetime().datetime(),
            duration=Numbers().integer_number(start=1, end=100),
            fare=Numbers().float_number(start=1, end=10000, precision=2),
        )
        for i in range(10)
    ]


def test_get_flights_unauth(client):
    resp = client.get(reverse("flight-list"))
    assert resp.status_code == 401


def test_get_flights_empty(client, headers):
    resp = client.get(
        reverse("flight-list"), content_type="application/json", **headers
    )

    payload = resp.json()
    assert payload["results"] == []


def test_get_flights_ok(client, headers, flight):
    resp = client.get(
        reverse("flight-list"), content_type="application/json", **headers
    )

    payload = resp.json()
    assert payload["results"][0]["name"] == flight.name
    assert payload["results"][0]["number"] == flight.number


def test_create_flight(client, headers):
    flight_name = "Flight1"
    data = {
        "name": flight_name,
        "number": "Flight Number",
        "departure": "Stockholm",
        "destination": "London",
        "scheduled_at": timezone.now(),
        "expected_at": timezone.now(),
        "fare": 112,
        "duration": 90,
    }
    resp = client.post(
        reverse("flight-list"),
        data=data,
        content_type="application/json",
        **headers,
    )

    payload = resp.json()
    created_flight = models.Flight.objects.get(name=flight_name)
    assert payload["id"] == created_flight.id


def test_partial_update_flight(client, headers, flight):
    data = {
        "departure": "Paris",
    }
    resp = client.patch(
        reverse("flight-detail", args=[flight.id]),
        data=data,
        content_type="application/json",
        **headers,
    )

    payload = resp.json()
    updated_flight = models.Flight.objects.get(id=flight.id)
    assert payload["departure"] == updated_flight.departure


def test_delete_flight(client, headers, flight):
    resp = client.delete(
        reverse("flight-detail", args=[flight.id]),
        content_type="application/json",
        **headers,
    )

    assert resp.status_code == 204
    assert not models.Flight.objects.filter(id=flight.id).exists()


def test_search_flight_by_name(client, headers, flights):
    some_flight = random.choice(flights)
    resp = client.get(
        reverse("flight-list"),
        data={"flight_name": some_flight.name},
        **headers,
    )

    assert resp.status_code == 200

    payload = resp.json()
    assert len(payload["results"]) == 1
    assert payload["results"][0]["number"] == some_flight.number


@pytest.mark.django_db
@pytest.mark.usefixtures("flights")
def test_search_specific_flight(client, headers, flight):
    assert models.Flight.objects.count() == 11

    resp = client.get(
        reverse("flight-list"),
        data={
            "scheduled_at": flight.scheduled_at,
            "departure": flight.departure,
            "destination": flight.destination,
        },
        **headers,
    )

    assert resp.status_code == 200

    payload = resp.json()
    assert len(payload["results"]) == 1
    assert payload["results"][0]["departure"] == flight.departure


def test_search_flight_pagination(client, headers, flights):
    assert models.Flight.objects.count() == 10

    resp = client.get(reverse("flight-list"), data={"limit": 5}, **headers)

    payload = resp.json()
    assert len(payload["results"]) == 5
    assert resp.status_code == 200
