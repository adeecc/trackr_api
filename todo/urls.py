from django.urls import path

from .views import TodoListAPIView, TodoDetailAPIView

urlpatterns = [
    path('', TodoListAPIView.as_view(), name='TodoList'),
    path('<int:id>', TodoDetailAPIView.as_view(), name='TodoList')
]
