from datetime import timedelta
from django.http import response

from rest_framework import serializers

from .models import Todo, TodoItem, Document
from .tasks import send_email


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


class EmailScheduleSerializer(serializers.Serializer):
    todo_item_id = serializers.IntegerField()


    def validate(self, attrs):
        todo_item = TodoItem.objects.get(id=attrs["todo_item_id"])
        documnets = Document.objects.filter(todo_item=todo_item)
        
        todo = todo_item.todo
        deadline = todo_item.deadline
        formatted_deadline = deadline.strftime('%a, %d %b %Y %H:%M')
        todo_list = todo_item.todo_list
        username = todo_list.owner.username

        data = {}
        data["todo_item"] = todo_item.id
        data["to"] = [todo_item.todo_list.owner.email]
        data["subject"] = f"Reminder for Event: {todo} @ {formatted_deadline}"
        data["body"] = f"Dear {username},<br>You have a task scheduled at {formatted_deadline}: {todo} ({todo_list}).<br>Make sure to attend and update on the app!<br>"
            
        for document in documnets:  
            url = 'https://shiftrio.blob.core.windows.net/media/' + (document.doc.name)
            data["body"] += f"<br><br><a href={url}>Click Link to download Attachment</a><br>"

        data["body"] += f"Shiftr<br>"

        eta = deadline - timedelta(minutes=10)
        # send_email(data=data)

        send_email.apply_async(eta=eta, kwargs={'data': data})

        return data

            
