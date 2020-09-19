# pylint:disable=no-member
import django_filters.rest_framework
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from flights.platform import models, serializers


@api_view(["GET"])
def status(_request):
    return Response()


class Users(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.User

    def create(self, request):
        super().create(request)
        return Response(status=201)


class Flights(viewsets.ModelViewSet):
    queryset = models.Flight.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.Flight
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = [
        "name",
        "scheduled_at",
        "departure",
        "destination",
    ]
