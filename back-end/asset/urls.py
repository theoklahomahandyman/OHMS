# from asset.views import AssetView, AssetInstanceView, AllAssetInstancesView, AssetMaintenanceView
# from django.urls import path

# urlpatterns = [
#     path('', AssetView.as_view(), name='asset-list'),
#     path('<int:pk>/', AssetView.as_view(), name='asset-detail'),

#     path('instance/<int:asset_pk>/', AssetInstanceView.as_view(), name='asset-instance-list'),
#     path('instance/<int:asset_pk>/<int:instance_pk>/', AssetInstanceView.as_view(), name='asset-instance-detail'),
#     path('instance/', AllAssetInstancesView.as_view(), name='all-asset-instances'),

#     path('maintenance/<int:instance_pk>/', AssetMaintenanceView.as_view(), name='instance-maintenance-list'),
#     path('maintenance/<int:instance_pk>/<int:maintenance_pk>/', AssetMaintenanceView.as_view(), name='instance-maintenance-detail'),
# ]
