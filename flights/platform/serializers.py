from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as dj_exceptions
from rest_framework import serializers as rf_serializers

from flights.platform import models


class User(rf_serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "username",
            "password",
        ]

    def create(self, validated):
        password = validated.pop("password")
        user = models.User.objects.create(**validated)
        user.set_password(password)
        user.save()
        return user

    def validate_password(self, value):
        try:
            validate_password(value)
        except dj_exceptions.ValidationError as exc:
            raise rf_serializers.ValidationError(exc.messages)
        return value
