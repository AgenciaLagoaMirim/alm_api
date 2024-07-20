# gitwebhook/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('git/webhook/', views.webhook, name='webhook'),
]