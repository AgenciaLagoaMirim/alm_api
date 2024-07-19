# gitwebhook/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("gitwebhook/", views.webhook, name="webhook"),
]
