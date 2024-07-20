from django.contrib import admin
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.urls import include, path

# from djoser import views as djoser_views

from datadash.urls import data_dash_router
from sl500_dd.urls import sl500_dd_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/data-dash/", include(data_dash_router.urls)),
    path("api/v1/data-dash/sl500-dd/", include(sl500_dd_router.urls)),
    path("api/v1/", include("djoser.urls")),
    path("api/v1/", include("djoser.urls.authtoken")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("", include("gitwebhook.urls")),
]
