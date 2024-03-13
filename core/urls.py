from django.contrib import admin
from django.urls import include, path

from datadash.urls import data_dash_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/data-dash/", include(data_dash_router.urls)),
    path("api/v1/", include("djoser.urls")),
    path("api/v1/", include("djoser.urls.authtoken")),
]
