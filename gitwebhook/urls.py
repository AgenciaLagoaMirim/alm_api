# gitwebhook/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("webhook/", views.webhook, name="webhook"),  # URL para o webhook
]
