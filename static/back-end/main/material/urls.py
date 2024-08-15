from material.views import MaterialView
from django.urls import path

urlpatterns = [
    path('materials/', MaterialView.as_view(), name='material-list'),
    path('materials/<int:pk>/', MaterialView.as_view(), name='material-detail'),

]