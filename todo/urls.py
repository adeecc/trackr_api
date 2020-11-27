from django.urls import path

from .views import DocumentListAPIView, TodoListAPIView, TodoDetailAPIView, TodoItemListAPIView, TodoItemDetailAPIView

urlpatterns = [
    path('', TodoListAPIView.as_view(), name='TodoList'),
    path('<int:id>', TodoDetailAPIView.as_view(), name='TodoList'),
    path('todo-items/', TodoItemListAPIView.as_view(), name='TodoItems'),
    path('todo-items/<int:id>', TodoItemDetailAPIView.as_view(), name='TodoItem'),
    path('documents/', DocumentListAPIView.as_view(), name='documents')
]
