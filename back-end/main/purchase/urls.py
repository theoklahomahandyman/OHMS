from purchase.views import PurchaseView, PurchaseMaterialView, PurchaseNewMaterialView, PurchaseRecieptView
from django.urls import path

urlpatterns = [
    path('', PurchaseView.as_view(), name='purchase-list'),
    path('<int:pk>/', PurchaseView.as_view(), name='purchase-detail'),

    path('image/<int:pk>/', PurchaseRecieptView.as_view(), name='purchase-picture-detail'),

    path('material/<int:purchase_pk>/', PurchaseMaterialView.as_view(), name='purchase-material-list'),
    path('material/<int:purchase_pk>/<int:material_pk>/', PurchaseMaterialView.as_view(), name='purchase-material-detail'),

    path('new/material/<int:purchase_pk>/', PurchaseNewMaterialView.as_view(), name='purchase-new-material'),
]
