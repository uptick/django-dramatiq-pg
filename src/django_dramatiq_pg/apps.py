import dramatiq
from dramatiq_pg import PostgresBroker

from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string


class DramatiqConfig(AppConfig):
    name = 'dramatiq'
    verbose_name = 'Dramatiq-PG Task Broker'

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
        self.broker = None

    def ready(self):
        '''
        Initialise our Broker when Django is ready.
        '''
        encoder = self.get_encoder()
        if encoder:
            dramatiq.set_encoder(encoder())

        middleware = self.get_middleware()

        self.broker = PostgresBroker(
            url=settings.DRAMATIQ_DATABASE_URL,
            middleware=middleware,
        )

        dramatiq.set_broker(self.broker)

    def get_encoder(self):
        encoder_path = getattr(settings, 'DRAMATIQ_ENCODER', None)
        if encoder_path:
            return import_string(encoder_path)
        return None

    def get_middleware(self):
        middleware_classes = getattr(settings, 'DRAMATIQ_MIDDLEWARE', None)
        if not middleware_classes:
            return None

        middleware = [
            import_string(middleware)
            for middleware in middleware_classes
        ]

        return middleware
