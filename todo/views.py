from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

from .models import Todo, TodoItem
from .serializers import TodoSerializer, TodoItemSerializer
from .renderers import TodoRenderer
from .permissions import IsOwner


class TodoListAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    renderer_classes = (TodoRenderer,)
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    renderer_classes = (TodoRenderer,)
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner, )
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class TodoItemListAPIView(ListCreateAPIView):
    serializer_class = TodoItemSerializer
    renderer_classes = (TodoRenderer,)
    queryset = TodoItem.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return TodoItem.objects.filter(todo_list__owner = self.request.user)

class TodoItemDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoItemSerializer
    renderer_classes = (TodoRenderer,)
    queryset = TodoItem.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(todo_list__owner = self.request.user)