from service.views import ServiceView, ServiceNameView
from django.urls import path

urlpatterns = [
    path('', ServiceView.as_view(), name='service-list'),
    path('<int:pk>/', ServiceView.as_view(), name='service-detail'),
    path('name/<int:pk>/', ServiceNameView.as_view(), name='service-name'),
]
