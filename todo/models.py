from django.db import models

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


    def __str__(self) -> str:
        return self.todo
