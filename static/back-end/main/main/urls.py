from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('api/auth/', include('rest_framework.urls')),
    path('api/user/', include('user.urls')),
    path('api/customer/', include('customer.urls')),
    path('api/service/', include('service.urls')),
    path('api/supplier/', include('supplier.urls')),
]
