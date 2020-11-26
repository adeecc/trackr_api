from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .models import InventoryItem
from .serializers import InventoryItemSerializer
from .renderers import InventoryItemRenderer
from .permissions import IsOwner


class InventoryItemAPIView(ListCreateAPIView):
    serializer_class = InventoryItemSerializer
    renderer_classes = (InventoryItemRenderer,)
    queryset = InventoryItem.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class InventoryItemDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = InventoryItemSerializer
    renderer_classes = (InventoryItemRenderer,)
    queryset = InventoryItem.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner, )
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)

