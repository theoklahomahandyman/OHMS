from order.views import OrderView, OrderCostView, OrderPictureView
from django.urls import path

urlpatterns = [
    path('orders/', OrderView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderView.as_view(), name='order-detail'),

    path('costs/', OrderCostView.as_view(), name='order-cost-create'),
    path('costs/<int:pk>/<str:type>/', OrderCostView.as_view(), name='order-cost-list'),
    path('costs/<int:pk>/<str:type>/', OrderCostView.as_view(), name='order-cost-detail'),

    path('pictures/', OrderPictureView.as_view(), name='order-picture-create'),
    path('pictures/<int:pk>/<str:type>/', OrderPictureView.as_view(), name='order-picture-list'),
    path('pictures/<int:pk>/<str:type>/', OrderPictureView.as_view(), name='order-picture-detail'),
]
