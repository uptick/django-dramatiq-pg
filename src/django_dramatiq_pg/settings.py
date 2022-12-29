from typing import NamedTuple, Optional

from dramatiq import Encoder, Middleware

from django.conf import settings
from django.utils.module_loading import import_string

from .registry import Registry
from .tools import make_url

__all__ = (
    'DramatiqSettings',
    'DramatiqBrokerSettings',
    'dramatiq_settings',
)


class DramatiqBrokerSettings(NamedTuple):
    MIDDLEWARE: list[str]
    DATABASE_ALIAS: str


class DramatiqSettings(NamedTuple):
    DRAMATIQ_BROKER: DramatiqBrokerSettings
    DRAMATIQ_REGISTRY: Optional[str] = None
    DRAMATIQ_ACTORS_MODULE: str = 'actors'
    DRAMATIQ_ENCODER: Optional[str] = None

    def encoder(self) -> Optional[Encoder]:
        if self.DRAMATIQ_ENCODER:
            return import_string(self.DRAMATIQ_ENCODER)()
        return None

    def middlewares(self) -> list[Middleware]:
        return [
            import_string(middleware)()
            if isinstance(middleware, str)
            else middleware
            for middleware in self.DRAMATIQ_BROKER.MIDDLEWARE
        ]

    def registry(self) -> Registry:
        if self.DRAMATIQ_REGISTRY:
            return import_string(settings.DRAMATIQ_REGISTRY)
        return Registry()

    def database_url(self) -> str:
        config = settings.DATABASES.get(self.DRAMATIQ_BROKER.DATABASE_ALIAS, None)
        if not config:
            raise ValueError(
                f'DATABASE_ALIAS={self.DRAMATIQ_BROKER.DATABASE_ALIAS} not found in DATABASES'
            )

        return make_url(**config)


def dramatiq_settings() -> DramatiqSettings:
    broker_settings = getattr(settings, 'DRAMATIQ_BROKER', None)
    if not broker_settings:
        raise ValueError('No DRAMATIQ_BROKER setting')

    if not broker_settings.get('DATABASE_ALIAS'):
        raise ValueError('No DATABASE_ALIAS setting for DRAMATIQ_BROKER')

    return DramatiqSettings(
        DRAMATIQ_BROKER=DramatiqBrokerSettings(
            DATABASE_ALIAS=broker_settings['DATABASE_ALIAS'],
            MIDDLEWARE=broker_settings.get('MIDDLEWARE', [
                'dramatiq.middleware.TimeLimit',
                'dramatiq.middleware.Callbacks',
                'dramatiq.middleware.Retries',
            ])
        ),
        DRAMATIQ_REGISTRY=getattr(settings, 'DRAMATIQ_REGISTRY', None),
        DRAMATIQ_ACTORS_MODULE=getattr(settings, 'DRAMATIQ_ACTORS_MODULE', 'actors'),
        DRAMATIQ_ENCODER=getattr(settings, 'DRAMATIQ_ENCODER', None),
    )
