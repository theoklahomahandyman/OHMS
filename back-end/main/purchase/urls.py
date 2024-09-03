from purchase.views import PurchaseView, PurchaseMaterialView
from django.urls import path

urlpatterns = [
    path('', PurchaseView.as_view(), name='purchase-list'),
    path('<int:pk>/', PurchaseView.as_view(), name='purchase-detail'),

    path('material/<int:purchase_pk>/', PurchaseMaterialView.as_view(), name='purchase-material-list'),
    path('material/<int:purchase_pk>/<int:material_pk>/', PurchaseMaterialView.as_view(), name='purchase-material-detail'),
]
