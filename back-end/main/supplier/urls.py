from supplier.views import SupplierView, SupplierNameView, SupplierAddressView, AddressView
from django.urls import path

urlpatterns = [
    path('', SupplierView.as_view(), name='supplier-list'),
    path('<int:pk>/', SupplierView.as_view(), name='supplier-detail'),
    path('name/<int:pk>/', SupplierNameView.as_view(), name='supplier-name'),

    path('addresses/<int:supplier_pk>/', SupplierAddressView.as_view(), name='supplier-address-list'),
    path('addresses/<int:supplier_pk>/<int:address_pk>/', SupplierAddressView.as_view(), name='supplier-address-detail'),
    path('address/<pk>/', AddressView.as_view(), name='supplier-address'),
]
