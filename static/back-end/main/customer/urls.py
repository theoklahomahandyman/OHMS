from customer.views import CustomerView
from django.urls import path

urlpatterns = [
    path('customers/', CustomerView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerView.as_view(), name='customer-detail'),
]
