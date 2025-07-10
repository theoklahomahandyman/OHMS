from supplier.views import SupplierView, AddressView
from django.urls import path

urlpatterns = [
    path('', SupplierView.as_view(), name='supplier-list'),
    path('<int:pk>/', SupplierView.as_view(), name='supplier-detail'),

    path('address/<int:pk>/', AddressView.as_view(), name='supplier-address'),
]
