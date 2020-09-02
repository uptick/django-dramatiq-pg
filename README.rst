==================
django_dramatiq_pg
==================

.. image:: https://badge.fury.io/py/django-dramatiq-pg.svg
    :target: https://pypi.org/project/django-dramatiq-pg

.. image:: https://img.shields.io/pypi/pyversions/django-dramatiq-pg.svg
    :target: https://pypi.org/project/django-dramatiq-pg

dramatiq-pg_ integration for django_.

    .. _dramatiq-pg: https://pypi.org/project/dramatiq-pg/
    .. _django: https://pypi.org/project/Django/

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

3. Create a Registry, and register your tasks

   .. code-block:: python

     from django_dramatiq_pg.registry import Registry

     tasks = Registry()


     @tasks.actor
     def mytask():
         ...

4. Configure

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
    DRAMATIQ_REGISTRY = 'myapp.registry.tasks'

5. Start the worker process:

   .. code-block:: sh

    $ dramatiq django_dramatiq_pg.worker

This worker module will auto-discover any module called 'actors' in
``INSTALLED_APPS``.

Registry
========

In a typical `dramatiq` application, the `Broker` is configured before any
tasks are registered. However, as `Django` is in control of the intialisation
sequence, there is an issue of ordering; the `actor` decorator assumes the
broker is already configured.

To resolve this, `django_dramatiq_pg` provides a `Registry` for your tasks,
which is then bound to the `Broker` when Django initialises.

In your code, declare a `Registry` instance, and use its `.actor` method to
decorate your task functions. Then tell `django_dramatiq_pg` to use your
registry with the `DRAMATIQ_REGISTRY` setting.

If you do not specify one, `django_dramatiq_pg` will create one on start.

The registry can be accessed as the `.registry` attribute on the
`django_dramatiq_pg` App instance.

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
