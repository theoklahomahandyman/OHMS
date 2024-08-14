from supplier.views import SupplierView
from django.urls import path

urlpatterns = [
    path('suppliers/', SupplierView.as_view(), name='supplier-list'),
    path('suppliers/<int:pk>/', SupplierView.as_view(), name='supplier-detail'),
]
