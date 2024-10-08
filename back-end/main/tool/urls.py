from tool.views import ToolView
from django.urls import path

urlpatterns = [
    path('', ToolView.as_view(), name='tool-list'),
    path('<int:pk>/', ToolView.as_view(), name='tool-detail'),
]
