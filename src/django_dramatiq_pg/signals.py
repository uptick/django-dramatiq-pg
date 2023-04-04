import dramatiq
from django.apps import apps
from django.conf import settings
from django.db.backends.signals import connection_created
from django.dispatch import receiver
from dramatiq_pg import PostgresBroker

from .settings import dramatiq_settings


@receiver(connection_created)
def change_connection(sender, connection, **kwargs):
    if connection.alias != settings.DRAMATIQ_BROKER['DATABASE_ALIAS']:
        return

    # Database is changed during running tests
    if not settings.is_overridden('DATABASES'):
        connection_created.disconnect(change_connection)
        return

    app = apps.get_app_config('django_dramatiq_pg')
    app_settings = dramatiq_settings()
    database_url = app_settings.database_url()

    # For tests, you need to replace the broker
    # with new one connected to the test database
    if app.database_url != database_url:
        app.database_url = database_url
        app.broker = PostgresBroker(
            url=database_url,
            middleware=app_settings.middlewares(),
        )
        dramatiq.set_broker(app.broker)
        app.registry.bind_broker(app.broker)

    connection_created.disconnect(change_connection)
