from purchase.views import PurchaseView, PurchaseMaterialView
from django.urls import path

urlpatterns = [
    path('purchases/', PurchaseView.as_view(), name='purchase-list'),
    path('purchases/<int:pk>/', PurchaseView.as_view(), name='purchase-detail'),

    path('materials/', PurchaseMaterialView.as_view(), name='purchase-material-create'),
    path('materials/<int:pk>/<str:type>/', PurchaseMaterialView.as_view(), name='purchase-material-list'),
    path('materials/<int:pk>/<str:type>/', PurchaseMaterialView.as_view(), name='purchase-material-detail'),
]
