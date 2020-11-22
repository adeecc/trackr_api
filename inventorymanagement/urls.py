from django.urls import path

from .views import InventoryItemAPIView, InventoryItemDetailAPIView
urlpatterns = [
    path('', InventoryItemAPIView.as_view(), name='InventoryItems'),
    path('<int:id>', InventoryItemDetailAPIView.as_view(), name='InventoryItem'),
]
