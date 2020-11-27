from django.contrib import admin

from .models import Document, TodoItem, Todo

admin.site.register(TodoItem)
admin.site.register(Todo)
admin.site.register(Document)