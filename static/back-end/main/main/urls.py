from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('api/auth/', include('rest_framework.urls')),
    path('api/user/', include('user.urls')),
]
