# gitwebhook/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.webhook, name="webhook"),  # Remova a parte "gitwebhook/" do caminho
]
