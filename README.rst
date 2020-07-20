==================
django_dramatiq_pg
==================

.. rubric:: ``dramatiq-pg`` integration for django

Installation
------------

1. Install with pip

   .. code-block:: sh

    $ pip install django-dramatiq-pg

2. Add to your ``INSTALLED_APPS`` list in settings.py

   .. code-block:: python

    INSTALLED_APPS = [
        ...
        'django_dramatiq_pg',
    ]

3. Configure the Database

   .. code-block:: python

    DRAMATIQ_BROKER = {
        "OPTIONS": {
            "url": "postgres:///mydb",
        },
        "MIDDLEWARE": [
            "dramatiq.middleware.TimeLimit",
            "dramatiq.middleware.Callbacks",
            "dramatiq.middleware.Retries",
        ],
    }

4. Start the worker process:

   .. code-block:: sh

    $ dramatiq django_dramatiq_pg.worker

This worker module will auto-discover any module called 'actors' in
``INSTALLED_APPS``.

Settings
--------

DRAMATIQ_BROKER
  A dict of options to pass when instantiating the broker.

DRAMATIC_BROKER['OPTIONS']
  Arguments to pass to the Broker.

DRAMATIC_BROKER['MIDDLEWARE']
  A list of middleware classes to be passed to the broker.

  These can either be import strings, or instances.

DRAMATIQ_ENCODER
  Default: None

  Import path for encoder class.

DRAMATIQ_ACTORS_MODULE
  Default: 'actors'

  Name of module use to auto-discover actors in INSTALLED_APPS.

DRAMATIQ_REGISTRY

  Import path for the task Registry instance.

  This should refer to an instance of `django_dramatiq_pg.registry.Registry`.

  This resolves the chicken/egg problem of declaring tasks before the broker is
  configured.
