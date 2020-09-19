# pylint:disable=no-member
from rest_framework import mixins, viewsets
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
