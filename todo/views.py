from django.http import HttpResponse

from rest_framework import permissions, status, generics
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser

from .models import Todo, TodoItem, Document
from .serializers import TodoSerializer, TodoItemSerializer, DocumentSerializer, EmailScheduleSerializer
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class TodoItemListAPIView(ListCreateAPIView):
    serializer_class = TodoItemSerializer
    renderer_classes = (TodoRenderer,)
    queryset = TodoItem.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return TodoItem.objects.filter(todo_list__owner=self.request.user)


class TodoItemDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoItemSerializer
    renderer_classes = (TodoRenderer,)
    queryset = TodoItem.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(todo_list__owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class DocumentListAPIView(ListCreateAPIView):
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser]
    queryset = Document.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Document.objects.filter(todo_item__todo_list__owner=self.request.user)


class DocumentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser]
    queryset = Document.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return Document.objects.filter(todo_item__todo_list__owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class TodoItemEmailScheduleAPIView(generics.GenericAPIView):
    serializer_class = EmailScheduleSerializer
    renderer_classes = (TodoRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_200_OK)
