from purchase.views import PurchaseView
from django.urls import path

urlpatterns = [
    path('purchases/', PurchaseView.as_view(), name='purchase-list'),
    path('purchases/<int:pk>/', PurchaseView.as_view(), name='purchase-detail'),
]
