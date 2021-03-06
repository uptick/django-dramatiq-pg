# Generated by Django 2.2.9 on 2020-02-16 23:57

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.CreateModel(
            name="BackgroundJob",
            fields=[
                ("message_id", models.UUIDField(primary_key=True, serialize=False)),
                ("queue_name", models.TextField(default="default")),
                (
                    "state",
                    models.TextField(
                        choices=[
                            ('queued', 'Queued'),
                            ('consumed', 'Consumed'),
                            ('rejected', 'Rejected'),
                            ('done', 'Done'),
                        ],
                        default="queued",
                    ),
                ),
                ("mtime", models.DateTimeField()),
                ("message", models.JSONField()),
                ("result", models.JSONField()),
                ("result_ttl", models.DateTimeField()),
            ],
            options={"db_table": "queue", "managed": False},
        ),
        migrations.RunSQL(
            """
CREATE SCHEMA dramatiq;

CREATE TYPE dramatiq."state" AS ENUM (
  'queued',
  'consumed',
  'rejected',
  'done'
);

CREATE TABLE dramatiq.queue(
  message_id uuid PRIMARY KEY,
  queue_name TEXT NOT NULL DEFAULT 'default',
  "state" dramatiq."state",
  mtime TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
  -- message as encoded by dramatiq.
  message JSONB,
  "result" JSONB,
  result_ttl  TIMESTAMP WITH TIME ZONE
) WITHOUT OIDS;

-- Index state and mtime together to speed up deletion. This can also speed up
-- statistics when VACUUM ANALYZE is recent enough.
CREATE INDEX ON dramatiq.queue ("state", mtime);
CREATE INDEX ON dramatiq.queue ((message->>'actor_name'));
        """
        ),
    ]
