from django.contrib import admin

from .models import QueuedJob


@admin.register(QueuedJob)
class QueuedJobAdmin(admin.ModelAdmin):
    list_display = (
        "message_id",
        "queue_name",
        "actor",
        "state",
    )
    list_filter = (
        "queue_name",
        "state",
    )

    def actor(self, obj):
        return obj.message["actor_name"]
