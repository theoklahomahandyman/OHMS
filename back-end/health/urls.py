from .views import health_check
from django.urls import path

urlpatterns = [
    path('check/', health_check, name='health-check'),
]
