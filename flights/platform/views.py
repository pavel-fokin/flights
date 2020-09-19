# pylint:disable=no-member
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from flights.platform import models, serializers


@api_view(["GET"])
def status(_request):
    return Response()


class User(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.User

    def create(self, request):
        super().create(request)
        return Response(status=201)


class FlightViewSet(viewsets.ModelViewSet):
    queryset = models.Flight.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.Flight

    def get_queryset(self):
        queryset = models.Flight.objects.all()

        flight_name = self.request.query_params.get("flight_name", None)
        if flight_name is not None:
            queryset = queryset.filter(name=flight_name)

        scheduled_at = self.request.query_params.get("scheduled_at", None)
        if scheduled_at is not None:
            queryset = queryset.filter(scheduled_at=scheduled_at)

        departure = self.request.query_params.get("departure", None)
        if departure is not None:
            queryset = queryset.filter(departure=departure)

        destination = self.request.query_params.get("destination", None)
        if destination is not None:
            queryset = queryset.filter(destination=destination)

        return queryset
