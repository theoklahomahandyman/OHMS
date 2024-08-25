from order.views import OrderView, OrderCostView
from django.urls import path

urlpatterns = [
    path('orders/', OrderView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderView.as_view(), name='order-detail'),

    path('costs/', OrderCostView.as_view(), name='order-cost-create'),
    path('costs/<int:pk>/<str:type>/', OrderCostView.as_view(), name='order-cost-list'),
    path('costs/<int:pk>/<str:type>/', OrderCostView.as_view(), name='order-cost-detail'),
]
