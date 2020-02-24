from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'queue_name', 'state',)
    list_filter = ('queue_name', 'state',)
