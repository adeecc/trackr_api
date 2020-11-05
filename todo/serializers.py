from rest_framework import serializers

from .models import Todo, TodoItem

class TodoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Todo
        fields = ['id', 'name', 'description', 'color',]