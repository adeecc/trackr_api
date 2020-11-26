from rest_framework import serializers

from .models import Todo, TodoItem


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = ['id', 'name', 'description', 'color', ]


class TodoItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TodoItem
        fields = ['id', 'todo', 'todo_list', 'done', 'deadline', 'priority']

    def create(self, validated_data):
        return TodoItem.objects.create_todoitem(**validated_data)