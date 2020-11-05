from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from .models import Todo, TodoItem
from .serializers import TodoSerializer
from .permissions import IsOwner


class TodoListAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner, )
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
