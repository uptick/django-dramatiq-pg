from typing import Optional

import dramatiq
from django.apps import AppConfig
from dramatiq_pg import PostgresBroker

from .registry import Registry
from .settings import dramatiq_settings

__all__ = ('DramatiqConfig',)


class DramatiqConfig(AppConfig):
    name = "django_dramatiq_pg"
    verbose_name = "Dramatiq-PG"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.broker: Optional[PostgresBroker] = None
        self.registry: Optional[Registry] = None
        self.database_url: str = ''

    def ready(self) -> None:
        """
        Initialise our Broker when Django is ready.
        """
        from . import signals  # NOQA

        settings = dramatiq_settings()

        encoder = settings.encoder()
        if encoder:
            dramatiq.set_encoder(encoder)

        self.database_url = settings.database_url()
        self.broker = PostgresBroker(
            url=self.database_url,
            middleware=settings.middlewares(),
        )
        dramatiq.set_broker(self.broker)

        self.registry = settings.registry()
        self.registry.bind_broker(self.broker)
