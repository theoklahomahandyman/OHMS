from service.views import ServiceView
from django.urls import path

urlpatterns = [
    path('', ServiceView.as_view(), name='service-list'),
    path('<int:pk>/', ServiceView.as_view(), name='service-detail'),
]
