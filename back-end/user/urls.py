from rest_framework_simplejwt.views import TokenObtainPairView
from user.views import UserView, AdminView
from django.urls import path

urlpatterns = [
    path('', UserView.as_view(), name='user'),
    path('login/', TokenObtainPairView.as_view(), name='login'),

    path('admin/', AdminView.as_view(), name='admin-list'),
    path('admin/<int:pk>/', AdminView.as_view(), name='admin-detail'),
]
