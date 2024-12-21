from customer.views import CustomerView
from django.urls import path

urlpatterns = [
    path('', CustomerView.as_view(), name='customer-list'),
    path('<int:pk>/', CustomerView.as_view(), name='customer-detail'),
]
