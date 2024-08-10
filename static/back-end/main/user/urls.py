from rest_framework_simplejwt.views import TokenObtainPairView
from user.views import UserView
from django.urls import path

urlpatterns = [
    path('', UserView.as_view(), name='user'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
]
