from order.views import OrderView
from django.urls import path

urlpatterns = [
    path('orders/', OrderView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderView.as_view(), name='order-detail'),

]
