from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", views.Users)
router.register(r"flights", views.Flights)

schema_view = get_schema_view(
    openapi.Info(
        title="Flight API",
        default_version="v1",
        description="Flight API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("status", views.status, name="status"),
    path("token", TokenObtainPairView.as_view(), name="token_get"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
