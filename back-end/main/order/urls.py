from order.views import OrderView, OrderCostView, OrderPictureView, OrderMaterialView, OrderPaymentView
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

    path('materials/', OrderMaterialView.as_view(), name='order-material-create'),
    path('materials/<int:pk>/<str:type>/', OrderMaterialView.as_view(), name='order-material-list'),
    path('materials/<int:pk>/<str:type>/', OrderMaterialView.as_view(), name='order-material-detail'),

    path('payments/', OrderPaymentView.as_view(), name='order-payment-create'),
    path('payments/<int:pk>/<str:type>/', OrderPaymentView.as_view(), name='order-payment-list'),
    path('payments/<int:pk>/<str:type>/', OrderPaymentView.as_view(), name='order-payment-detail'),
]
