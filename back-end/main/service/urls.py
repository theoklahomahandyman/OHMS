from service.views import ServiceView
from django.urls import path

urlpatterns = [
    path('services/', ServiceView.as_view(), name='service-list'),
    path('services/<int:pk>/', ServiceView.as_view(), name='service-detail'),
]
