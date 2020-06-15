from enum import Enum

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone


class State(str, Enum):
    QUEUED = "queued"
    CONSUMED = "consumed"
    REJECTED = "rejected"
    DONE = "done"


State.choices = tuple((state.value, state.name) for state in State)


class BackgroundJob(models.Model):
    message_id = models.UUIDField(primary_key=True)
    queue_name = models.TextField(default="default")
    state = models.CharField(max_length=16, default=State.QUEUED, choices=State.choices)
    mtime = models.DateTimeField(default=timezone.now)
    message = JSONField(blank=True, null=True)
    result = JSONField(blank=True, null=True)
    result_ttl = models.DateTimeField()

    STATUS = State

    class Meta:
        managed = False
        db_table = "queue"
        indexes = (models.Index(fields=["state", "mtime"]),)
