from datetime import datetime, timedelta
from django.db import models
from django.db.models.manager import BaseManager

from authentication.models import User


class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super(ColorField, self).__init__(*args, **kwargs)


class Todo(models.Model):
    # TODO: Add user specific tags
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    color = ColorField(default='#ffffff')

    def __str__(self) -> str:
        return self.name


class TodoItemManager(models.Manager):
    def create_todoitem(self, todo, todo_list, done, deadline, priority):
        todoitem = self.model(
            todo=todo,
            todo_list=todo_list,
            done=done,
            deadline=deadline,
            priority=priority,
        )

        todoitem.save()
        # username = todoitem.todo_list.owner.username
        # formatted_deadline = deadline.strftime('%a, %d %b %Y %H:%M')

        # data = {}

        # data["todo_item"] = todoitem.id
        # data["to"] = [todoitem.todo_list.owner.email]
        # data["subject"] = f"Reminder for Event: {todo} @ {formatted_deadline}"
        # data["body"] = f"Dear {username},\nYou have a task scheduled at {formatted_deadline}: {todo} ({todo_list}).\nMake sure to attend and update on the app!\nShiftr"

        # eta = deadline - timedelta(minutes=10)
        # send_email.apply_async(eta=eta, kwargs={'data': data})

        return todoitem


class TodoItem(models.Model):

    class Priority(models.TextChoices):
        LOW = 'low', ('Low')
        IMPORTANT = 'imp', ('Important')
        URGENT = 'urg', ('Urgent')

    todo = models.CharField(max_length=255)
    todo_list = models.ForeignKey(Todo, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(
        max_length=3, choices=Priority.choices, default=Priority.LOW)

    objects = TodoItemManager()

    def __str__(self) -> str:
        return self.todo


class Document(models.Model):
    doc = models.FileField(upload_to='uploads/todo/') # EXTRMEMLY UNSECURE!
    todo_item = models.ForeignKey(TodoItem, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)