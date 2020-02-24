# dramatiq-pg integration for django

## Installation

1. Install with pip

    pip install django-dramatiq-pg

2. Add to your INSTALLED_APPS list in settings.py

    INSTALLED_APPS = [
        ...
        'django_dramatiq_pg',
    ]

3. Configure the Database

    DRAMATIQ_DATABASE_URL = '...'

4. Start the worker process:

    $ dramatiq django_dramatiq_pg.worker

This worker module will auto-discover any module called 'actors' in
INSTALLED_APPS.

## Settings

This package attempts to retain backward compatibility with
``django-dramatiq`` settings. It will try to fall back to using
`DRAMATIQ_BROKER` values where possible.

DRAMATIQ_BROKER_OPTIONS:
  Required!
  A dict of options to pass when instantiating the broker.
  The middleware will be provided from the setting below, if set.

  If not set, will try ``DRAMATIQ_BROKER['OPTIONS']``.

DRAMATIQ_ENCODER:
  Default: None
  Import path for encoder class.

  This is compatible with ``django-dramatiq``

DRAMATIQ_MIDDLEWARE:
  Default: None
  List of import paths for middleware classes.

  If not set, will try ``DRAMATIQ_BROKER['MIDDLEWARE']``.

DRAMATIQ_ACTORS_MODULE:
  Default: 'actors'
  Name of module use to auto-discover actors in INSTALLED_APPS.
