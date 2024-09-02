from supplier.views import SupplierView, SupplierAddressView
from django.urls import path

urlpatterns = [
    path('', SupplierView.as_view(), name='supplier-list'),
    path('<int:pk>/', SupplierView.as_view(), name='supplier-detail'),

    path('addresses/', SupplierAddressView.as_view(), name='supplier-address-create'),
    path('addresses/<int:pk>/<str:type>/', SupplierAddressView.as_view(), name='supplier-address-list'),
    path('addresses/<int:pk>/<str:type>/', SupplierAddressView.as_view(), name='supplier-address-detail'),
]
