from rest_framework_simplejwt.views import TokenRefreshView
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('api/auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/customer/', include('customer.urls')),
    path('api/material/', include('material.urls')),
    path('api/tool/', include('tool.urls')),
    # path('api/asset/', include('asset.urls')),
    path('api/order/', include('order.urls')),
    path('api/purchase/', include('purchase.urls')),
    path('api/service/', include('service.urls')),
    path('api/supplier/', include('supplier.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
