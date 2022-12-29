from django.conf import settings

from .apps import DramatiqConfig

__all__ = (
    'Router',
)


class Router:
    app_label = DramatiqConfig.name

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return settings.DRAMATIQ_BROKER['DATABASE_ALIAS']
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.app_label:
            return settings.DRAMATIQ_BROKER['DATABASE_ALIAS']
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.app_label:
            return db == settings.DRAMATIQ_BROKER['DATABASE_ALIAS']
        return None
