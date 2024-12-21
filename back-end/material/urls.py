from material.views import MaterialView
from django.urls import path

urlpatterns = [
    path('', MaterialView.as_view(), name='material-list'),
    path('<int:pk>/', MaterialView.as_view(), name='material-detail'),
]
