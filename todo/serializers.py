from rest_framework import serializers

from .models import Todo, TodoItem, Document


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


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'doc', 'todo_item']