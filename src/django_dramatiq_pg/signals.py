from django.db.backends.signals import connection_created
from django.dispatch import receiver


@receiver(connection_created)
def add_dramatiq_schema(sender, connection, **kwargs):
    with connection.cursor() as cursor:
        cursor.execute("SELECT set_config('search_path', current_setting('search_path') || ', dramatiq', false);")
