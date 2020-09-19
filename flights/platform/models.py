from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models


class User(AbstractUser):
    class Meta:
        db_table = "user"


class Flight(models.Model):
    class Meta:
        db_table = "flight"
        index_together = [
            ("departure", "destination"),
        ]

    name = models.CharField(max_length=1024, db_index=True)
    number = models.CharField(max_length=16)

    scheduled_at = models.DateTimeField(null=True, db_index=True)
    expected_at = models.DateTimeField(null=True)

    departure = models.TextField(null=True, db_index=True)
    destination = models.TextField(null=True, db_index=True)

    duration = models.IntegerField(
        validators=[validators.MinValueValidator(limit_value=1)], null=True
    )  # minutes

    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
