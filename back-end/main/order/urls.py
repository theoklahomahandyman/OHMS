from order.views import OrderView, OrderCostView, OrderPictureView, OrderMaterialView, OrderToolView, OrderAssetView, OrderPaymentView, OrderWorkLogView, OrderWorkerView, PublicView
from django.urls import path

urlpatterns = [
    path('', OrderView.as_view(), name='order-list'),
    path('<int:pk>/', OrderView.as_view(), name='order-detail'),

    path('public/', PublicView.as_view(), name='order-public'),

    path('image/<int:pk>/', OrderPictureView.as_view(), name='order-picture-detail'),

    path('worklog/<int:order_pk>/', OrderWorkLogView.as_view(), name='order-work-log-list'),
    path('worklog/<int:order_pk>/<int:work_log_pk>/', OrderWorkLogView.as_view(), name='order-work-log-detail'),

    path('cost/<int:order_pk>/', OrderCostView.as_view(), name='order-cost-list'),
    path('cost/<int:order_pk>/<int:cost_pk>/', OrderCostView.as_view(), name='order-cost-detail'),

    path('material/<int:order_pk>/', OrderMaterialView.as_view(), name='order-material-list'),
    path('material/<int:order_pk>/<int:material_pk>/', OrderMaterialView.as_view(), name='order-material-detail'),

    path('tool/<int:order_pk>/', OrderToolView.as_view(), name='order-tool-list'),
    path('tool/<int:order_pk>/<int:tool_pk>/', OrderToolView.as_view(), name='order-tool-detail'),

    path('asset/<int:order_pk>/', OrderAssetView.as_view(), name='order-asset-list'),
    path('asset/<int:order_pk>/<int:asset_pk>/', OrderAssetView.as_view(), name='order-asset-detail'),

    path('payment/<int:order_pk>/', OrderPaymentView.as_view(), name='order-payment-list'),
    path('payment/<int:order_pk>/<int:payment_pk>/', OrderPaymentView.as_view(), name='order-payment-detail'),

    path('worker/<int:order_pk>/', OrderWorkerView.as_view(), name='order-worker-list'),
    path('worker/<int:order_pk>/<int:worker_pk>/', OrderWorkerView.as_view(), name='order-worker-detail'),
]
