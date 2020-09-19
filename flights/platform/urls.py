from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", views.User)

urlpatterns = [
    path("status", views.status, name="status"),

    path(
        "token", TokenObtainPairView.as_view(), name="token_get"
    ),
    path(
        "token/refresh", TokenRefreshView.as_view(), name="token_refresh"
    ),

    path(
        "", include(router.urls)
    )
]
