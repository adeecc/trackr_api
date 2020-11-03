from django.contrib import admin

from .models import TodoItem, Todo

admin.site.register(TodoItem)
admin.site.register(Todo)