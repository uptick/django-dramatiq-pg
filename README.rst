==================
django_dramatiq_pg
==================

.. rubric:: integration for django

Installation
------------

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

Settings
--------

This package attempts to retain backward compatibility with ``django-dramatiq``
settings, but ingores the `BROKER` key for `DRAMATIQ_BROKER`.

See https://github.com/Bogdanp/django_dramatiq for more details.

DRAMATIQ_BROKER:
  A dict of options to pass when instantiating the broker.

DRAMATIC_BROKER['OPTIONS']:

  Arguments to pass to the Broker.

DRAMATIC_BROKER['MIDDLEWARE']:

  A list of middleware classes to be passed to the broker.
  These can either be import strings, or instances.

DRAMATIQ_ENCODER:
  Default: None
  Import path for encoder class.

  This is compatible with ``django-dramatiq``

DRAMATIQ_ACTORS_MODULE:
  Default: 'actors'
  Name of module use to auto-discover actors in INSTALLED_APPS.

