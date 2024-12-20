from purchase.views import PurchaseView, PurchaseMaterialView, PurchaseNewMaterialView, PurchaseRecieptView, PurchaseToolView, PurchaseNewToolView
from django.urls import path

urlpatterns = [
    path('', PurchaseView.as_view(), name='purchase-list'),
    path('<int:pk>/', PurchaseView.as_view(), name='purchase-detail'),

    path('image/<int:pk>/', PurchaseRecieptView.as_view(), name='purchase-picture-detail'),

    path('material/<int:purchase_pk>/', PurchaseMaterialView.as_view(), name='purchase-material-list'),
    path('material/<int:purchase_pk>/<int:material_pk>/', PurchaseMaterialView.as_view(), name='purchase-material-detail'),

    path('new/material/<int:purchase_pk>/', PurchaseNewMaterialView.as_view(), name='purchase-new-material'),

    path('tool/<int:purchase_pk>/', PurchaseToolView.as_view(), name='purchase-tool-list'),
    path('tool/<int:purchase_pk>/<int:tool_pk>/', PurchaseToolView.as_view(), name='purchase-tool-detail'),

    path('new/tool/<int:purchase_pk>/', PurchaseNewToolView.as_view(), name='purchase-new-tool'),

    # path('asset/<int:purchase_pk>/', PurchaseAssetView.as_view(), name='purchase-asset-list'),
    # path('asset/<int:purchase_pk>/<int:asset_pk>/', PurchaseAssetView.as_view(), name='purchase-asset-detail'),

    # path('new/asset/<int:purchase_pk>/', PurchaseNewAssetView.as_view(), name='purchase-new-asset'),
]
