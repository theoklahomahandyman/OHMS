from asset.views import AssetView
from django.urls import path

urlpatterns = [
    path('', AssetView.as_view(), name='asset-list'),
    path('<int:pk>/', AssetView.as_view(), name='asset-detail'),
]
