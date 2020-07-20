import dramatiq
from dramatiq_pg import PostgresBroker

from django.apps import AppConfig
from django.conf import settings
from django.utils.module_loading import import_string


class DramatiqConfig(AppConfig):
    name = "django_dramatiq_pg"
    verbose_name = "Dramatiq-PG"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.broker = None

    def ready(self):
        """
        Initialise our Broker when Django is ready.
        """
        from . import signals  # NOQA

        encoder = self.get_encoder()
        if encoder:
            dramatiq.set_encoder(encoder())

        options = self.get_broker_options()

        middleware = self.get_middleware()
        if middleware:
            options["middleware"] = middleware

        self.broker = PostgresBroker(**options)

        dramatiq.set_broker(self.broker)

        self.registry = self.get_registry()

        self.registry.bind_broker(self.broker)

    def get_encoder(self):
        encoder_path = getattr(settings, "DRAMATIQ_ENCODER", None)
        if encoder_path:
            return import_string(encoder_path)
        return None

    def get_broker_options(self):
        """This settings is _required_"""
        try:
            return settings.DRAMATIQ_BROKER["OPTIONS"]
        except KeyError:
            raise ValueError("No OPTIONS setting for DRAMATIQ_BROKER!")

    def get_middleware(self):
        try:
            middleware_config = settings.DRAMATIQ_BROKER["MIDDLEWARE"]
        except (AttributeError, KeyError):
            return None

        def resolve_class(name):
            if isinstance(name, str):
                return import_string(name)()
            return name

        middleware_list = [resolve_class(middleware) for middleware in middleware_config]

        return middleware_list

    def get_registry(self):
        """Import (or create) the Task Registry"""
        try:
            registry = import_string(settings.DRAMATIQ_REGISTRY)
        except AttributeError:
            from .registry import Registry

            registry = Registry()

        return registry
