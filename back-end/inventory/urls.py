from inventory.views import MaterialView, ToolView
from django.urls import path

urlpatterns = [
    path('material/', MaterialView.as_view(), name='material-list'),
    path('material/<int:pk>/', MaterialView.as_view(), name='material-detail'),

    path('tool/', ToolView.as_view(), name='tool-list'),
    path('tool/<int:pk>/', ToolView.as_view(), name='tool-detail'),
]
