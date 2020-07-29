from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone


class BackgroundJob(models.Model):

    class STATUS(models.TextChoices):
        QUEUED = "queued"
        CONSUMED = "consumed"
        REJECTED = "rejected"
        DONE = "done"

    message_id = models.UUIDField(primary_key=True)
    queue_name = models.TextField(default="default")
    state = models.CharField(max_length=16, default=STATUS.QUEUED, choices=STATUS.choices)
    mtime = models.DateTimeField(default=timezone.now)
    message = JSONField(blank=True, null=True)
    result = JSONField(blank=True, null=True)
    result_ttl = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "queue"
        indexes = (models.Index(fields=["state", "mtime"]),)
