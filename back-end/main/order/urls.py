from order.views import OrderView, OrderCostView, OrderPictureView, OrderMaterialView, OrderPaymentView
from django.urls import path

urlpatterns = [
    path('', OrderView.as_view(), name='order-list'),
    path('<int:pk>/', OrderView.as_view(), name='order-detail'),

    path('costs/<int:order_pk>/', OrderCostView.as_view(), name='order-cost-list'),
    path('costs/<int:order_pk>/<int:cost_pk>/', OrderCostView.as_view(), name='order-cost-detail'),

    path('pictures/<int:order_pk>/', OrderPictureView.as_view(), name='order-picture-list'),
    path('pictures/<int:order_pk>/<int:picture_pk>/', OrderPictureView.as_view(), name='order-picture-detail'),

    path('materials/<int:order_pk>/', OrderMaterialView.as_view(), name='order-material-list'),
    path('materials/<int:order_pk>/<int:material_pk>/', OrderMaterialView.as_view(), name='order-material-detail'),

    path('payments/<int:order_pk>/', OrderPaymentView.as_view(), name='order-payment-list'),
    path('payments/<int:order_pk>/<int:payment_pk>/', OrderPaymentView.as_view(), name='order-payment-detail'),
]
