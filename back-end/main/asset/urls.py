from asset.views import AssetView, AssetMaintenanceView
from django.urls import path

urlpatterns = [
    path('', AssetView.as_view(), name='asset-list'),
    path('<int:pk>/', AssetView.as_view(), name='asset-detail'),

    path('maintenance/<int:asset_pk>/', AssetMaintenanceView.as_view(), name='asset-maintenance-list'),
    path('maintenance/<int:asset_pk>/<int:maintenance_pk>/', AssetMaintenanceView.as_view(), name='asset-maintenance-detail'),
]
