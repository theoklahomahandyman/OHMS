from customer.views import CustomerView, CustomerNameView
from django.urls import path

urlpatterns = [
    path('', CustomerView.as_view(), name='customer-list'),
    path('<int:pk>/', CustomerView.as_view(), name='customer-detail'),
    path('name/<int:pk>/', CustomerNameView.as_view(), name='customer-name'),
]
